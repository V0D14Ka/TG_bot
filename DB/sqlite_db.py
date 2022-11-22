import sqlite3


class BotDB:
    def __init__(self, db):
        self.base = sqlite3.connect(db)
        self.cur = self.base.cursor()
        self.base.execute("CREATE TABLE IF NOT EXISTS user("
                          "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                          "user_id INTEGER NOT NULL UNIQUE,"
                          "join_date DATETIME NOT NULL DEFAULT ( ( DATETIME( 'now' ))))")
        self.base.execute("CREATE TABLE IF NOT EXISTS record("
                          "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                          "user_id INTEGER NOT NULL REFERENCES user (id) ON DELETE CASCADE,"
                          "operation BOOLEAN NOT NULL,"
                          "amount DECIMAL NOT NULL,"
                          "operation_date DATETIME NOT NULL DEFAULT ( (DATETIME('now'))),"
                          "category INTEGER NOT NULL DEFAULT 0)")
        self.base.commit()

    def add_user(self, user_id):
        self.cur.execute("INSERT INTO `user` (`user_id`) VALUES (?)", (user_id,))

    def get_user_id(self, user_id):
        result = self.cur.execute("SELECT `id` FROM `user` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def is_user_exist(self, user_id):
        result = self.cur.execute("SELECT * FROM `user` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_record(self, user_id, operation, amount):
        self.cur.execute("INSERT INTO `record` (`user_id`, `operation`, `amount`) VALUES (?, ?, ?)",
                         (self.get_user_id(user_id), operation == '+', amount))

    def get_records(self, _user_id, period="*"):
        match period:
            case "day":
                result = self.cur.execute(
                    "SELECT * FROM `record` WHERE `user_id` = ? AND `operation_date` BETWEEN datetime('now', 'start of "
                    "day') AND "
                    "datetime('now', 'localtime') ORDER BY `operation_date`",
                    (self.get_user_id(_user_id),))
                return result.fetchall()
            case "month":
                return self.cur.execute("SELECT * FROM `record` WHERE `user_id` = ? AND `operation_date` BETWEEN "
                                        "datetime('now', 'start of month') AND datetime('now', 'localtime') "
                                        "ORDER BY `operation_date`",
                                        (self.get_user_id(_user_id), )).fetchall()
            case "year":
                return self.cur.execute("SELECT * FROM `record` WHERE `user_id` = ? AND `operation_date` BETWEEN "
                                        "datetime('now', 'start of year') AND datetime('now', 'localtime') "
                                        "ORDER BY `operation_date`",
                                        (self.get_user_id(_user_id), )).fetchall()
            case _:
                return self.cur.execute("SELECT * FROM `record` WHERE `user_id` = ? ORDER BY `operation_date`",
                                        (self.get_user_id(_user_id), )).fetchall()

    def save(self):
        return self.base.commit()

    def close(self):
        self.base.close()
