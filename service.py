from flask import request, abort
import random
import xmltodict
import g
import db
import json

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
            # db.insertReqres(reqres)
            reqres.insert()
            abort(404)

    # 校验请求方法
    if a.method != "" and request.method not in a.method:
        g.logger.warn("路由: %s, 请求方法未匹配成功")
        reqres.reason = "请求方法未匹配成功"
        # db.insertReqres(reqres)
        reqres.insert()
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

    reqres.params = params
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
        # db.insertReqres(reqres)
        reqres.insert()
        return ""
        
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
    # db.insertReqres(reqres)
    reqres.insert()
    return result.content, code, type


@g.app.route("/api/mocks/<id>")
def info(id):
    reqres = db.TableReqRes()
    reqres.query_one(id)
    return json.dumps(reqres.__dict__)


