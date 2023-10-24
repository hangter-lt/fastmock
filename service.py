from flask import Flask, request, abort
import random
import xmltodict

app = Flask(__name__)

methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]

content = {}


@app.route("/<path:path>", methods=methods)
def api(path):
    uri = "/" + path
    a = content.get(uri)
    # 匹配路由参数,目前仅支持末端路由匹配
    if not a:
        uri = "/".join(uri.split("/")[:-1] + [":"])
        a = content.get(uri)
        if not a:
            abort(404)

    # 校验请求方法
    if a.method != "" and request.method not in a.method:
        abort(404)

    # 获取请求内容
    headers = dict(request.headers)
    params = dict(request.args)
    print("headers")
    print(headers)
    
    content_type = request.headers.get("Content-Type")
    match content_type:
        case "":
            params.update(dict(request.form))
            params.update(dict(request.get_json()))
        case "multipart/form-data":
            params.update(dict(request.form))
        case "application/x-www-form-urlencoded":
            params.update(dict(request.form))
        case "application/json":
            params.update(request.get_json())
        case "application/xml":
            data = request.get_data()
            data = xmltodict.parse(data)
            params.update(data)
        case _:
            # TODO: 优化,自适应参数格式 
            params.update(dict(request.form))
            params.update(dict(request.get_json()))

    print("params")
    print(params)
    
    results = []
    # 校验请求内容
    for data in a.datas:
        # 校验headers
        if not data.request.headers.items() <= headers.items():
            continue

        # 校验参数
        if data.request.params.items() <= params.items():
            results.append(data.response)


    # 响应内容
    if len(results) == 0:
        return ""
        
    result = results[random.randint(0,len(results)-1)]
    
    code = 200
    if result.code != 0:
        code = result.code

    type = {}
    if result.content_type != "":
        type = {"Content-Type": result.content_type}
    

    print("response")
    print(result.content)

    return result.content, code, type

