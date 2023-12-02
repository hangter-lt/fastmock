import os
import re
import json
import time
import g
from watchdog.events import FileSystemEventHandler
import uuid


patternValue = f"`(.+?)`"
patternJson = r"""(?<=[}\]"'])\s*,\s*(?!\s*[{["'])"""

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.md'):
                fullname = os.path.join(root, f)
                yield fullname

class Api():

    def __init__(self) -> None:
        self.uri = ""
        self.method = ""
        self.datas = []

    class Data():
        def __init__(self) -> None:
            self.request = self.Request()
            self.response = self.Response()
        
        class Request():
            def __init__(self) -> None:
                self.route = ""
                self.method = ""
                self.headers = {}
                self.params = {}

        class Response():
            def __init__(self) -> None:
                self.code = 0
                self.contentType = ""
                self.content = ""

# 解析文件内容
def parsefile(lines):
    a = Api()
    for i in range(len(lines)):
        # match uri
        if lines[i].startswith("* uri"):
            res = re.findall(patternValue, lines[i])
            if len(res) == 0:
                while i<len(lines):
                    res = re.findall(patternValue, lines[i])
                    if len(res) == 0:
                        i += 1
                    else:
                        a.uri = res[0]
                        break
            else:
                a.uri = res[0]

        # match method
        if lines[i].startswith("* method"):
            res = re.findall(patternValue, lines[i])
            if len(res) == 0:
                while i<len(lines):
                    res = re.findall(patternValue, lines[i])
                    if len(res) == 0:
                        i += 1
                    else:
                        a.method = res[0]
                        break
            else:
                a.method = res[0]
 
        # match req and res
        if lines[i].startswith("---"):
            i += 1
            data = a.Data()
            request = data.request
            response = data.response
            while i<len(lines):
                # match req route
                if lines[i].startswith("+ route"):
                    res = re.findall(patternValue, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(patternValue, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                request.route = res[0]
                                break
                    else:
                        request.route = res[0] 

                # match req method
                if lines[i].startswith("+ method"):
                    res = re.findall(patternValue, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(patternValue, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                request.method = res[0]
                                break
                    else:
                        request.method = res[0] 
    
                # match req headers
                if lines[i].startswith("+ headers"):
                    i += 1
                    if lines[i].startswith("```"):
                        i += 1
                        con = ""
                        while i<len(lines):
                            if lines[i].startswith("```"):
                                i += 1
                                break
                            con += lines[i]
                            i += 1
                        if len(con) != "":
                            con = re.sub(patternJson, "", con, 0)
                            con = json.loads(con, strict=False)
                            request.headers = con

                # match req params
                if lines[i].startswith("+ params"):
                    i += 1
                    if lines[i].startswith("```"):
                        i += 1
                        con = ""
                        while i<len(lines):
                            if lines[i].startswith("```"):
                                i += 1
                                break
                            con += lines[i]
                            i += 1
                        if len(con) != "":
                            con = re.sub(patternJson, "", con, 0)
                            con = json.loads(con, strict=False)
                            request.params = con

                # match res code
                if lines[i].startswith("- code"):
                    res = re.findall(patternValue, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(patternValue, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                response.code = int(res[0])
                                break
                    else:
                        response.code = int(res[0]) 
 
                # match res content-type
                if lines[i].startswith("- content-type"):  
                    res = re.findall(patternValue, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(patternValue, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                response.contentType = res[0]
                                break
                    else:
                        response.contentType = res[0] 
 
                # match res data
                if lines[i].startswith("- content") and not lines[i].startswith("- content-"):
                    i += 1
                    if lines[i].startswith("```"):
                        i += 1
                        con = ""
                        while i<len(lines):
                            if lines[i].startswith("```"):
                                i += 1
                                break
                            con += lines[i]
                            i += 1
                        if len(con) != "":
                            con = re.sub(patternJson, "", con, 0)
                            # con = json.loads(con, strict=False)
                            response.content = con
                # match next
                if  i == len(lines) or lines[i].startswith("---"):
                    break
            
                i += 1
            data.request = request
            data.response = response 
            a.datas.append(data)
    return a

def updatefile():
    while True:
        # 更新
        if g.queueFiles.empty():
            g.queueEnd = ""
        filename = g.queueFiles.get()
        with open(filename, 'r', encoding='UTF-8') as f:
            a = parsefile(f.readlines())
            g.content[a.uri] = a
            g.logger.info("接口文件: %s已更新", filename)
        
        time.sleep(1)

class MyHandler(FileSystemEventHandler):
    # 监控文件变动, 文件path加入到队列, 加入时判断队列最后一位是不是当前路径
    # 通过另一个全局变量记录队列最后一位
    def on_created(self, event):
        g.dirTree = getDirTree("./api")
        if not event.is_directory:
            if event.src_path != g.queueEnd:
                g.logger.info("检测到接口创建: %s", event.src_path)
                g.queueFiles.put(event.src_path)
                g.queueEnd = event.src_path

    def on_modified(self, event):
        if not event.is_directory:
            if event.src_path != g.queueEnd:
                g.logger.info("检测到接口文件更新: %s", event.src_path)
                g.queueFiles.put(event.src_path)
                g.queueEnd = event.src_path

    def on_moved(self, event):
        g.dirTree = getDirTree("./api")
    
    def on_deleted(self, event):
        g.dirTree = getDirTree("./api")

# 生成目录树
def getDirTree(rootPath):
    """
    Return the directory tree for the given root path.
    """
    # Get the name of the current directory
    name = os.path.basename(rootPath)

    uid = str(uuid.uuid1()).replace("-", "")
    g.pathHash[uid] = rootPath
    # Create a dictionary to store the directory tree
    dirTree = {'title': name, 'key': uid, "type": "dir"}

    # Get the list of all items in the directory
    items = os.listdir(rootPath)

    # Create a list to store the items in the directory
    dirItems = []

    # Loop through the items
    for item in items:
        # Get the full path of the item
        itemPath = os.path.join(rootPath, item)

        # If the item is a directory, recursively get the directory tree
        if os.path.isdir(itemPath):
            dirItems.append(getDirTree(itemPath))
        # If the item is a file, add the file name to the list of items
        else:
            if item.endswith('.md'):
                uid = str(uuid.uuid1()).replace("-", "")
                g.pathHash[uid] = itemPath
                dirItems.append({'title': item, 'key': uid, "type": "file"})

    # Add the list of items to the directory tree dictionary
    dirTree['children'] = dirItems

    # Return the directory tree
    return dirTree