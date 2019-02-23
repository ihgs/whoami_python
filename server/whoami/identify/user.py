import sqlite3
import bcrypt
from contextlib import closing

db = 'db/whoami.db'


class UserDao:

    @classmethod
    def create_table(cls):
        with closing(sqlite3.connect(db)) as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS users \
                (id INTEGER PRIMARY KEY AUTOINCREMENT, userid TEXT unique, password TEXT, roles TEXT)")
            conn.commit()

    @classmethod
    def create(cls, userid, password, roles=None):
        # pylint https://github.com/PyCQA/pylint/issues/1437
        with closing(sqlite3.connect(db)) as conn:
            c = conn.cursor()

            salt = bcrypt.gensalt(rounds=12, prefix=b'2a')
            hashed = bcrypt.hashpw(password.encode(), salt)
            sql = 'insert into users (userid, password, roles) values (?,?,?)'
            user = (userid, hashed, roles)
            c.execute(sql, user)
            conn.commit()

    @classmethod
    def identify(cls, userid, password):
        with closing(sqlite3.connect(db)) as conn:
            c = conn.cursor()
            select_sql = 'select * from users where userid=?'
            for row in c.execute(select_sql, (userid,)):
                if (bcrypt.checkpw(password.encode(), row[2])):
                    if (row[3] is not None):
                        roles = row[3].split(',')
                    return {
                        'userid': userid,
                        'roles:': roles
                    }
            return None


if __name__ == "__main__":
    print(UserDao.identify('admin', 'password'))
    print(UserDao.identify('admin', 'passworda'))
    print(UserDao.identify('adminn', 'password'))
