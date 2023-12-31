import queue
import logging
from flask import Flask
from flask.logging import default_handler

# 存放申请释放eventsource连接的jihe
closeSets = set()

# 全局列表,存储请求响应内容reqres
listReqres = []

# api配置文件目录树
dirTree = {}
pathHash = {}

# 全局队列,变动的文件
queueFiles = queue.SimpleQueue()

# 记录队列末尾值
queueEnd = ""

# api内容
content = {}

# 日志配置
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter(fmt="%(asctime)s - %(levelname)4s - %(message)s", datefmt="%X")
)
fh = logging.FileHandler(filename="api.log", mode="w")
fh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(levelname)4s - %(message)s", datefmt="%Y/%m/%d %X"
    )
)
flt = logging.Filter("api")

# app
app = Flask(__name__, static_folder="dist")
app.debug = False
app.logger.setLevel(logging.DEBUG)
app.logger.removeHandler(default_handler)
app.logger.addHandler(sh)
app.logger.addHandler(fh)
app.logger.name = "api"
app.logger.addFilter(flt)

logger = app.logger
