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
            self.cursor.execute('INSERT INTO users (id, activ, address) VALUES (?, ?, ?)', (user_id, 0, ""))
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

    def add_used_ip(self, db_name: str, user_ip: str, user_id: int):
        self.__connect_database(db_name)
        try:
            self.cursor.execute(f"UPDATE users SET address = '{user_ip}' WHERE id = {str(user_id)}")
            self.cursor.execute(f"UPDATE users SET activ = 1 WHERE id = {str(user_id)}")
            self.database.commit()
        except Exception as exc:
            print(f"ERROR!Can not add ip address to user {user_id}: {exc}")

    def is_activ(self, db_name: str, user_id: int):
        self.__connect_database(db_name)
        try:
            self.cursor.execute(f"SELECT activ FROM users WHERE id = {user_id}")
            flag = self.cursor.fetchall()
            flag2 = flag[0]
            print(f"Flag: {flag}")
            print(f"Flag2: {flag2}")
            print(f"Flag3: {flag2[0]}")
            if flag2[0] == 1:
                return True
            return False
        except Exception as exc:
            print(f"ERROR!Can not take info about user id({user_id}: {exc})")

