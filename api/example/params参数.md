# 匹配params示例

* uri `/api/v1/params`
* method `GET|POST`

匹配参数时,params会同时匹配url,body,json,xml多个形式的参数
----------
+ params
```json
{
    "hello": "world"
}
```
- content-type `application/json`
- content
```json
{
    "result": "success"
}
```
----------
+ params
```json
{
    "hello": "word"
}
```
- code `400`
- content
```
faild
```