import queue
import logging
from flask import Flask
from flask.logging import default_handler 

# 全局队列,变动的文件
queue_files = queue.SimpleQueue()

# 记录队列末尾值
queue_end = ""

# content
content = {}


# 日志配置
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter(
    fmt="%(asctime)s - %(levelname)4s - %(message)s",
    datefmt="%X"
    ))
fh = logging.FileHandler(filename="api.log",mode='w')
fh.setFormatter(logging.Formatter(
    fmt="%(asctime)s - %(levelname)4s - %(message)s",
    datefmt="%Y/%m/%d %X"
    ))
flt = logging.Filter("api")

# app
app = Flask(__name__)
app.debug = True
app.logger.removeHandler (default_handler)
app.logger.addHandler(sh)
app.logger.addHandler(fh)
app.logger.name = "api"
app.logger.addFilter(flt)

logger = app.logger