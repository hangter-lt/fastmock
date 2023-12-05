# 测试用mock文件
* uri: `/api/test`
* method: `GET|POST`
-----
+ params
```json
{
    "lang": "golang"
}
```
- content
```json
{
    "description": "Build simple, secure, scalable systems with Go."
}
```
-----
+ params
```
{
    "lang": "php"
}
```
- content
```
PHP是最好的语言!
```
-----
+ params
```json
{
    "lang": "python"
}
```
- content-type `application/json`
- content
```json
{
    "description": "Python is a programming language that lets you work quickly and integrate systems more effectively."
}
```