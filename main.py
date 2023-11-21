import threading
import handle
import init
import g
from watchdog.observers import Observer


if __name__ == "__main__":
    path = "./api"

    init.init_DB()

    g.logger.info("解析接口文件开始")
    for filename in handle.findAllFile(path):
        with open(filename, 'r', encoding='UTF-8') as f:
            a = handle.parsefile(f.readlines())
            g.content[a.uri] = a
            g.logger.info("api: %s", a.uri)
    g.logger.info("解析接口文件完成")

    # 监视配置文件增删改
    event_handler = handle.MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    # 启动一个线程处理队列
    t = threading.Thread(target=handle.updatefile)
    t.start()

    g.logger.info("mock接口启动")
    g.app.run()

