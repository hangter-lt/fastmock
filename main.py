import threading
import handle
import service
import g

if __name__ == "__main__":
    path = "./api"

    for filename in handle.findAllFile(path):
        with open(filename, 'r', encoding='UTF-8') as f:
            a = handle.parsefile(f.readlines())
            g.content[a.uri] = a
    

    # 监视配置文件增删改
    event_handler = service.MyHandler()
    observer = service.Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    # 启动一个线程处理队列
    t = threading.Thread(target=handle.updatefile)
    t.start()

    service.app.run()

