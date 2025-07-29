import sqlite3


class DataBase:
    def __connect_database(self, db_name: str):
        try:
            self.database = sqlite3.connect(db_name)
            self.cursor = self.database.cursor()
        except Exception as exc:
            print(f"ERROR! Can not connect to data base {exc}")

    def __init__(self, db_name: str):
        try:
            self.database = sqlite3.connect(db_name)
            self.cursor = self.database.cursor()
            self.database.close()
        except Exception as exc:
            print(f"ERROR! Can not init data base {exc}")

    def make_users_table(self, db_name: str):
        try:
            self.__connect_database(db_name)
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY UNIQUE,
            activ BLOB,
            address TEXT
            )
            ''')
            self.database.commit()
            self.database.close()
        except Exception as exc:
            print(f"ERROR! Can not make users table in data base {exc}")

    def insert_new_user(self, user_id: int, db_name: str):
        self.__connect_database(db_name)
        try:
            self.cursor.execute('INSERT INTO users (id, activ, address) VALUES (?, ?, ?)', (user_id, 0, "10.0.0.1/32"))
            self.database.commit()
        except Exception as exc:
            print(f"User already exists: {exc}")
        self.database.close()

    def get_not_activ_user(self, db_name):
        try:
            self.__connect_database(db_name)
            self.cursor.execute('SELECT id, activ FROM users WHERE activ = 0')
            not_active_users = self.cursor.fetchall()
            self.database.close()
            return not_active_users
        except Exception as exc:
            print(f"ERROR! Can not take not active users {exc}")
        finally:
            return not_active_users

    def get_used_ip(self, db_name: str):
        try:
            self.__connect_database(db_name)
            self.cursor.execute('SELECT address FROM users')
            used_ip = self.cursor.fetchall()
            self.database.close()
            used_ip_list = []
            for ip in used_ip:
                used_ip_list.append(ip[0])
            return used_ip_list
        except Exception as exc:
            print(f"ERROR! Can not take used ip {exc}")
        finally:
            return  used_ip_list
