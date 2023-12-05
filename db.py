import sqlite3
import time

class TableReqRes:
    uri = ""
    method = ""
    header = ""
    params = ""
    code = 0
    contentType = ""
    content = ""
    result = ""
    reason = ""
    time = int(time.time() * 1000)

    def insert(self):
        conn = sqlite3.connect("mock.db")
        cursor = conn.cursor()

        cursor.execute(
            """
                INSERT INTO "reqres" ("uri", "method", "header", "params", "code", "content_type", "content", "result", "reason", "time")
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                self.uri,
                self.method,
                str(self.header),
                str(self.params),
                self.code,
                self.contentType,
                str(self.content),
                self.result,
                self.reason,
                self.time,
            ),
        )
        conn.commit()
        conn.close()

        self.id = cursor.lastrowid

    def queryOne(self, id):
        self.id = id
        conn = sqlite3.connect("mock.db")
        cursor = conn.cursor()

        data = cursor.execute(
            """
                SELECT uri, method, header, params, code, content_type, content, result, reason, time 
                FROM reqres 
                WHERE id = ?;""",
            (str(self.id),),
        )

        data = data.fetchone()
        if data is not None:
            self.uri = data[0]
            self.method = data[1]
            self.header = data[2]
            self.params = data[3]
            self.code = data[4]
            self.contentType = data[5]
            self.content = data[6]
            self.result = data[7]
            self.reason = data[8]
            self.time = data[9]

        conn.close()
