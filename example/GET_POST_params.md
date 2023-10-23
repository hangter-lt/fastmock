**此文件请在源码模式下参考**
# 示例mock配置
路由参数匹配

* uri: `/api/v1/hello/world`
* method: `GET|POST`

1. 匹配/api/v1/hello/world 参数id=1 响应hello, world
-----------
- params
```java
{
    "id": 1
}
```
+ value
```
hello, world
```

2. 匹配/api/v1/hello/world 参数id=2, 响应json
-----------
- params
```json
{
    "id": 2
}
```
- headers
```
{
    "Accept": "application/json"
}
```
+ content-type `application/json`
+ value 
```json
{
    "hello": "world"
}
```