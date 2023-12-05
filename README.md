# fastmock

## 使用说明
在api目录下存放要mock的数据文件, 支持多层目录, md格式, 默认端口5000, 支持配置文件热更新
### 启动程序
`pip install --no-index --find-links=libs -r requirements.txt`  
`python main.py`

### mock文件格式
后缀.md, 文件名无要求
配置文件借助markdown格式(用markdown是为了能够更好的编写和预览,md渲染后的显示效果非常好),使用其中几个字符进行匹配操作:
1. "*": 用于匹配通用参数(uri,method)
2. "-": 用于匹配请求参数(route,headers,params)
3. "+": 用于匹配响应内容(code,content-type,content)  
原则上 `* - +` 不混用, 方便区分. 实际上支持三个符号混用
4. "``` ```": 代码块,用于匹配headers,params,content多行及代码块内容  
三个反引号后面跟着的语言类型, 例如```json, json不参数匹配, 目的用于markdown渲染时显示效果好
5. "` `": 单行代码,用于匹配uri,method,route,code,content-type单个词内容
6. "---": 行分割符,用于匹配多对请求和响应的内容  
除以上符号外,其他md语法不参与匹配,可用于注释自由填充  
示例请参考[api/example/](api/example/)内文件

### 匹配规则
headers, params使用json形式填写  
params会匹配多种来源的请求参数(url参数,body参数,json参数,xml参数)  
一组请求中的route, headers, params会与实际请求内容参与匹配, 使用宽松的匹配模式, 配置文件未指定的内容视为通过, 三项完全被实际请求内容包含视为成功, 非必填, 可随意组合  
匹配成功的组内响应内容会被响应, 若多组匹配成功, 则随机响应其中一组

## WebUI
前端项目仓库: [fastmock-web](https://github.com/hangter-lt/fastmock-web) 已集成前端资源文件到此仓库dist目录下


### 实时请求响应预览
重启项目会清空历史记录

### 在线修改mock文件

## TODO:
支持配置文件,自定义端口等  
支持动态参数  
UI支持新增删除文件  
...
