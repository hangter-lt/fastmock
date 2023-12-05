# 匹配header示例

* uri `/api/v1/header`
* method `GET|POST|DELETE`
---------
+ headers
```json
{
    "ApiName": "query"
}
```
+ params
```json
{
    "id": 1
}
```
- code `200`
- content-type `application/json`
- content
```json
{
    "hello": "world"
}
```
------------
+ headers
```json
{
    "ApiName": "delete"
}
```
+ params
```json
{
    "id": 1
}
``` 
- code `200`
------------
+ headers
```json
{
    "ApiName": "update"
}
```
+ params
```json
{
    "id": 1,
    "hello": "world"
}
``` 
- content
```
success
```
------------
+ headers
```json
{
    "ApiName": "update"
}
```
- code `400`