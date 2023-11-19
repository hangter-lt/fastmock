import threading
import handle
import service
import logging
import g

if __name__ == "__main__":
    path = "./api"

    g.logger.info("解析接口文件开始")
    for filename in handle.findAllFile(path):
        with open(filename, 'r', encoding='UTF-8') as f:
            a = handle.parsefile(f.readlines())
            g.content[a.uri] = a
            g.logger.info("接口文件: %s已更新", filename)
    g.logger.info("解析接口文件完成")

    # 监视配置文件增删改
    event_handler = service.MyHandler()
    observer = service.Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    # 启动一个线程处理队列
    t = threading.Thread(target=handle.updatefile)
    t.start()

    g.logger.info("mock接口已启动")
    g.app.run()

