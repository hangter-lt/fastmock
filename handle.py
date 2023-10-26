import os
import re
import json


pattern_value = f"`(.+?)`"
pattern_json_comma = r"""(?<=[}\]"'])\s*,\s*(?!\s*[{["'])"""

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
                self.headers = {}
                self.params = {}

        class Response():
            def __init__(self) -> None:
                self.code = 0
                self.content_type = ""
                self.content = ""

# 解析文件内容
def parsefile(lines):
    a = Api()
    for i in range(len(lines)):
        # match uri
        if lines[i].startswith("* uri"):
            res = re.findall(pattern_value, lines[i])
            if len(res) == 0:
                while i<len(lines):
                    res = re.findall(pattern_value, lines[i])
                    if len(res) == 0:
                        i += 1
                    else:
                        a.uri = res[0]
                        break
            else:
                a.uri = res[0]

        # match method
        if lines[i].startswith("* method"):
            res = re.findall(pattern_value, lines[i])
            if len(res) == 0:
                while i<len(lines):
                    res = re.findall(pattern_value, lines[i])
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
                    res = re.findall(pattern_value, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(pattern_value, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                request.route = res[0]
                                break
                    else:
                        request.route = res[0] 
    
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
                            con = re.sub(pattern_json_comma, "", con, 0)
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
                            con = re.sub(pattern_json_comma, "", con, 0)
                            con = json.loads(con, strict=False)
                            request.params = con

                # match res code
                if lines[i].startswith("- code"):
                    res = re.findall(pattern_value, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(pattern_value, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                response.code = int(res[0])
                                break
                    else:
                        response.code = int(res[0]) 
 
                # match res content-type
                if lines[i].startswith("- content-type"):  
                    res = re.findall(pattern_value, lines[i])
                    if len(res) == 0:
                        while i<len(lines):
                            res = re.findall(pattern_value, lines[i])
                            if len(res) == 0:
                                i += 1
                            else:
                                response.content_type = res[0]
                                break
                    else:
                        response.content_type = res[0] 
 
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
                            con = re.sub(pattern_json_comma, "", con, 0)
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
