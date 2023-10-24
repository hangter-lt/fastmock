**此文件请在源码模式下参考**
# 示例mock配置
路由参数匹配

* uri: `/api/v1/hello/:`
* method: `GET`

1. 匹配/api/v1/hello/python, 响应hello, python
-----------
- route `python`
+ content
```
hello, python
```

2. 匹配/api/v1/hello/java, 响应not found
-----------
- route `java`
+ code `404`

3. 匹配/api/v1/hello/golang, 响应xml
-----------
- route `golang`
- headers
```
{
    "Accept": "application/json"
}
```
+ content-type `application/xml`
+ content
```xml
<root>
    <hello>golang</hello>
</root>
```