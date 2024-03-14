from flask import request, abort, Response, render_template
import random
import xmltodict
import g
import db
import json
import time
import consts
import os
import shutil

methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]


@g.app.route("/<path:path>", methods=methods)
def api(path):
    if consts.ROUTEPRE in path:
        abort(404)

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
            g.logger.warn("路由: %s未匹配成功", "/" + path)
            reqres.reason = "路由未匹配成功"
            reqres.code = 404
            reqres.insert()
            g.listReqres.append(reqres)
            abort(404)

    # 校验请求方法
    if a.method != "" and request.method not in a.method:
        g.logger.warn("路由: %s, 请求方法未匹配成功")
        reqres.reason = "请求方法未匹配成功"
        reqres.code = 404
        reqres.insert()
        g.listReqres.append(reqres)
        abort(404)

    # 获取请求内容
    headers = dict(request.headers)
    params = dict(request.args)
    g.logger.info("请求头: %s\n", headers)

    contentType = request.headers.get("Content-Type")
    match contentType:
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
                    data = request.get_data()
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
        g.logger.warn("路由: %s未匹配到内容", uri)
        reqres.reason = "未匹配到内容"
        reqres.code = 200
        reqres.insert()
        g.listReqres.append(reqres)
        return "", 200, {}

    result = results[random.randint(0, len(results) - 1)]

    code = 200
    if result.code != 0:
        code = result.code

    type = {}
    if result.contentType != "":
        type = {"Content-Type": result.contentType}

    g.logger.info("响应码: %s", code)
    g.logger.info("响应类型: %s", type)
    g.logger.info("响应内容: %s\n", result.content)

    reqres.code = code
    reqres.contentType = result.contentType
    reqres.content = result.content
    reqres.result = "success"
    reqres.insert()
    g.listReqres.append(reqres)
    return result.content, code, type


# 请求内容
@g.app.route("/" + consts.ROUTEPRE + "/request/<id>", methods=["GET"])
def info(id):
    reqres = db.TableReqRes()
    reqres.queryOne(id)
    return json.dumps(reqres.__dict__)


# 实时请求
@g.app.route("/" + consts.ROUTEPRE + "/requests", methods=["GET"])
def list():
    linkId = request.args.get("link_id")
    if linkId is None:
        return abort(400)

    def eventStream(linkId):
        i = 0
        while True:
            # 关闭连接
            if linkId in g.closeSets:
                g.closeSets.remove(linkId)
                break

            if i >= len(g.listReqres):
                time.sleep(1)
                continue
            reqres = g.listReqres[i]
            res = {
                "id": reqres.id,
                "uri": reqres.uri,
                "method": reqres.method,
            }
            i += 1
            # 符合前端接受规范流传递
            yield "id: " + str(reqres.id) + "event: message\ndata: " + str(
                json.dumps(res)
            ) + "\n\n"

    return Response(eventStream(linkId), mimetype="text/event-stream")


# 目录树
@g.app.route("/" + consts.ROUTEPRE + "/tree", methods=["GET"])
def dirTree():
    return json.dumps(g.dirTree["children"])


# 文件内容
@g.app.route("/" + consts.ROUTEPRE + "/file/<uid>", methods=["GET"])
def fileContent(uid):
    path = g.pathHash[uid]
    with open(path, "r", encoding="UTF-8") as f:
        data = f.read()
    return Response(data, mimetype="text/plain")


# 写入文件
@g.app.route("/" + consts.ROUTEPRE + "/files/write", methods=["POST"])
def fileWrite():
    data = request.get_json()
    path = data.get("path")
    fileContent = data.get("file")

    path = g.pathHash[path]
    with open(path, "w", encoding="UTF-8") as f:
        f.write(fileContent)

    return "success"


# 首页
@g.app.route("/")
def index():
    # return render_template("index.html")
    return g.app.send_static_file("index.html")


# 静态资源
@g.app.route("/" + consts.ROUTEPRE + "/<path>")
def assets(path):
    return g.app.send_static_file(consts.ROUTEPRE + "/" + path)


# 请求关闭连接
@g.app.route("/" + consts.ROUTEPRE + "/requests/close", methods=["GET"])
def closeEvent():
    linkId = request.args.get("link_id")
    g.closeSets.add(linkId)
    return "success close"

# 增加配置文件或目录
@g.app.route("/" + consts.ROUTEPRE + "/files/add", methods=["POST"])
def addFileFolder():
    data = request.get_json()
    name = data.get("name")
    is_dir = data.get("is_dir")
    key = data.get("key")

    if key == "":
        path = "./api" + "/" + name
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        path = g.pathHash[key] + "/" + name
        if is_dir:
            if not os.path.exists(path):
                os.makedirs(path)
        else:
            file = open(path, "w")
            file.close()

    return ""


# 删除文件或目录
@g.app.route("/" + consts.ROUTEPRE + "/files/remove", methods=["POST"])
def removeFileFolder():
    data = request.get_json()
    key = data.get("key")

    path = g.pathHash[key]

    if os.path.isdir(path):
        shutil.rmtree(path) 
    else:
        os.remove(path)
    return ""

# 重命名
@g.app.route("/" + consts.ROUTEPRE + "/files/rename", methods=["POST"])
def renameFileFolder():
    data = request.get_json()
    key = data.get("key")
    name = data.get("name")

    path = g.pathHash[key]
    path = path.split("/")
    path[-1] = name
    path = "/".join(path)

    os.rename(g.pathHash[key], path)
    return ""
