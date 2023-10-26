import handle
import service
import g

if __name__ == "__main__":
    for filename in handle.findAllFile("./api"):
        with open(filename, 'r', encoding='UTF-8') as f:
            a = handle.parsefile(f.readlines())
            g.content[a.uri] = a
    

    # 监视配置文件增删改
    path = "./api"
    event_handler = service.MyHandler()
    observer = service.Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    # TODO: 启动一个线程处理队列

    service.app.run()

