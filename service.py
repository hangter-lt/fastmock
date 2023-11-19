from flask import Flask, request, abort
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import random
import xmltodict
import g


methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"]


class MyHandler(FileSystemEventHandler):
    # 监控文件变动, 文件path加入到队列, 加入时判断队列最后一位是不是当前路径
    # 通过另一个全局变量记录队列最后一位
    def on_created(self, event):
        if not event.is_directory:
            if event.src_path != g.queue_end:
                g.logger.info("检测到接口创建: %s", event.src_path)
                g.queue_files.put(event.src_path)
                g.queue_end = event.src_path

    def on_modified(self, event):
        if not event.is_directory:
            if event.src_path != g.queue_end:
                g.logger.info("检测到接口文件更新: %s", event.src_path)
                g.queue_files.put(event.src_path)
                g.queue_end = event.src_path


@g.app.route("/<path:path>", methods=methods)
def api(path):
    uri = "/" + path
    g.logger.info("请求路由: %s", uri)
    a = g.content.get(uri)
    # 匹配路由参数,目前仅支持末端路由匹配
    if not a:
        uri = "/".join(uri.split("/")[:-1] + [":"])
        a = g.content.get(uri)
        if not a:
            g.logger.warn("路由: %s匹配失败", '/' + path)
            abort(404)

    # 校验请求方法
    if a.method != "" and request.method not in a.method:
        g.logger.warn("路由: %s, 请求方法未匹配成功")
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
            # TODO: 优化,自适应参数格式 
            params.update(dict(request.form))
            try:
                params.update(dict(request.get_json()))
            except:
                pass

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

    return result.content, code, type

