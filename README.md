# fastmock

## 使用说明
在api目录下存放要mock的数据文件, md格式, 默认端口5000, 支持配置文件热更新
### 启动程序
`pip install --no-index --find-links=libs -r requirements.txt`  
`python main.py`

## mock文件格式
后缀.md, 文件名无要求
配置文件借助markdown格式,使用其中几个字符进行匹配操作:
1. "*": 用于匹配通用参数(uri,method)
2. "-": 用于匹配请求参数(route,headers,params)
3. "+": 用于匹配响应参数(code,content-type,content)
4. "``````": 代码段,用于匹配headers,params,content内容
5. "``": 代码块,用于匹配uri,method,route,code,content-type内容
6. "---": 行分割符,用于匹配多对请求和响应的内容  
除以上符号外,其他md语法不参与匹配,可用于注释自由填充

例(示例请用md源代码查看,渲染后的内容会影响显示效果):
* uri `/hello/:`     // 必填, :代指路由参数占位符,有:时请求参数route必填
* method `GET|POST`  // 可选,可多个  
// ----用于分割一组请求和响应
------
+ route `apiname`    // 路由参数,可选,uri中有:时生效
+ method `GET`       // 本组请求增加method匹配,可多个
+ headers            // 请求头,可选,写入时参与匹配,json格式
```json              // 代码块语言不影响内容
{
    "ApiName": "hello"
}
```
+ params              // 请求参数,可选,写入时参数匹配,json格式
```
{
    "hello": "world"
}
```
- code `200`          // 响应码,可选,默认为200
- content-type        // 响应类型,可选,支持json,xml,text,html...
`application/json`
+ content             // 响应内容,可选,支持text,json,xml
```
{
    "hello": "world"
}
```


### 匹配规则
一组请求中的route,headers,params会与实际请求内容参与匹配,三项完全被实际请求内容包含视为成功,非必填,可随意组合  
匹配成功的组内响应内容会被响应,若多组匹配成功,则随机响应其中一组




# TODO:
增加日志  
UI
支持配置文件,自定义端口等  
支持动态参数  
...
