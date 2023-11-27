import g
import sqlite3

def init_DB():
    
    conn = sqlite3.connect('mock.db')
    cursor = conn.cursor()

    # 清空数据表
    cursor.execute("DROP TABLE IF EXISTS REQRES;")

    # 创建请求响应表
    cursor.execute('''
        CREATE TABLE "reqres" (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "uri" text,
            "method" TEXT,
            "header" TEXT,
            "params" TEXT,
            "code" integer,
            "content_type" TEXT,
            "content" TEXT,
            "result" TEXT,
            "reason" TEXT,
            "time" INTEGER                  
        ); 
    ''')
    conn.commit()
    conn.close()
