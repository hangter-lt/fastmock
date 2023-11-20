import sqlite3

def insertReqres(data:dict):
    conn = sqlite3.connect('mock.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
            INSERT INTO "reqres" ("uri", "method", "header", "params", "code", "content_type", "content", "result", "reason")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', 
        (
            data.get("uri"), 
            data.get("method"), 
            str(data.get("header")) if data.get("header") else "", 
            str(data.get("params")) if data.get("params") else "", 
            data.get("code"), 
            data.get("content_type"), 
            str(data.get("content")) if data.get("content") else "", 
            data.get("result"), 
            data.get("reason"), 
        )
    )
    conn.commit()
    conn.close()