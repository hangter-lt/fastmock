from flask import request, abort, Response
import random
import xmltodict
import g
import db
import json
import time

methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]


@g.app.route("/<path:path>", methods=methods)
def api(path):
    reqres = db.TableReqRes()
    reqres.uri = "/" + path
    reqres.method = request.method
    reqres.header = request.headers
    reqres.result = "faild"

    uri = "/" + path
    g.logger.info("请求路由: %s", uri)
    a = g.content.get(uri)
    # 匹配路由参数,目前仅支持末端路由匹配
    if not a:
        uri = "/".join(uri.split("/")[:-1] + [":"])
        a = g.content.get(uri)
        if not a:
            g.logger.warn("路由: %s未匹配成功", '/' + path)
            reqres.reason = "路由未匹配成功"
            reqres.code = 404
            reqres.insert()
            g.list_reqres.append(reqres)
            abort(404)

    # 校验请求方法
    if a.method != "" and request.method not in a.method:
        g.logger.warn("路由: %s, 请求方法未匹配成功")
        reqres.reason = "请求方法未匹配成功"
        reqres.code = 404
        reqres.insert()
        g.list_reqres.append(reqres)
        abort(404)

    # 获取请求内容
    headers = dict(request.headers)
    params = dict(request.args)
    g.logger.info("请求头: %s\n", headers)
    
    content_type = request.headers.get("Content-Type")
    match content_type:
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
            # 自适应参数类型
            # form格式
            data = request.form
            if data := "":
                # json格式
                try:
                    data = dict(request.get_json())
                except:
                    pass
                # xml格式
                try:
                    data =  request.get_data()
                    data = xmltodict.parse(data)
                except:
                    pass
            else:
                data = dict(data)

    reqres.params = json.dumps(params)
    g.logger.info("请求参数: %s\n", params)

    results = []
    # 校验请求内容
    for data in a.datas:
        # 校验route
        if data.request.route != "":
            if path.split("/")[-1] != data.request.route:
                continue

        # 校验组内method
        if data.request.method != "":
            if request.method not in data.request.method:
                continue    
        
        # 校验headers
        if not data.request.headers.items() <= headers.items():
            continue

        # 校验参数
        if data.request.params.items() <= params.items():
            results.append(data.response)


    # 响应内容
    if len(results) == 0:
        g.logger.warn("路由: %s未匹配到内容",uri)
        reqres.reason = "未匹配到内容"
        reqres.code = 200
        reqres.insert()
        g.list_reqres.append(reqres)
        return "", 200, {}       
        
    result = results[random.randint(0,len(results)-1)]
    
    code = 200
    if result.code != 0:
        code = result.code

    type = {}
    if result.content_type != "":
        type = {"Content-Type": result.content_type}
    

    g.logger.info("响应码: %s", code)
    g.logger.info("响应类型: %s", type)
    g.logger.info("响应内容: %s\n", result.content)

    reqres.code = code
    reqres.content_type = result.content_type
    reqres.content = result.content
    reqres.result = "success"
    reqres.insert()
    g.list_reqres.append(reqres)
    return result.content, code, type

# 请求内容
@g.app.route("/api/requests/<id>", methods=["GET"])
def info(id):
    reqres = db.TableReqRes()
    reqres.query_one(id)
    return json.dumps(reqres.__dict__)

# 实时请求
@g.app.route("/api/requests", methods=["GET"])
def list():
    
    def eventStream():
        i = 0
        while True:
            if i >= len(g.list_reqres):
                time.sleep(1)
                continue
            reqres = g.list_reqres[i]
            res = {
                "id": reqres.id,
                "uri": reqres.uri,
                "method": reqres.method,
            }
            i += 1
            # 符合前端接受规范流传递
            yield "id: " + str(reqres.id) + "event: message\ndata: " + str(json.dumps(res)) + "\n\n" 
    return Response(eventStream(), mimetype="text/event-stream")

# 目录树
@g.app.route("/api/tree", methods=["GET"])
def dirTree():
    return json.dumps(g.dirTree["children"])
    
# 文件内容
@g.app.route("/api/file/<uid>", methods=["GET"])
def fileContent(uid):
    path = g.pathHash[uid]
    with open(path, 'r', encoding='UTF-8') as f:
        data = f.read()
    return Response(data, mimetype="text/plain")

# 写入文件
@g.app.route("/api/files/write", methods=["POST"])
def fileWrite():
    data = request.get_json()
    path = data.get("path")
    fileContent = data.get("file")

    path = g.pathHash[path]
    with open(path, 'w', encoding='UTF-8') as f:
        f.write(fileContent)
    
    return "success"

