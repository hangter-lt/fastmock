import queue

# 全局队列,变动的文件
queue_update_files = queue.SimpleQueue()
queue_delete_files = queue.SimpleQueue()

# 记录队列末尾值
queue_end = ""

# content
content = {}
