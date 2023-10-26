import handle
import service
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 全局队列

class MyHandler(FileSystemEventHandler):
    # 监控文件变动, 文件path加入到队列, 加入时判断队列最后一位是不是当前路径
    # 通过另一个全局变量记录队列最后一位
    def on_modified(self, event):
        if not event.is_directory:
            print("文件发生了改变！")

# 启动一个线程从队列取数据

if __name__ == "__main__":
    for filename in handle.findAllFile("./api"):
        with open(filename, 'r', encoding='UTF-8') as f:
            a = handle.parsefile(f.readlines())
            service.content[a.uri] = a
    

    path = "./api"  # 监视当前目录
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()


    service.app.run()

