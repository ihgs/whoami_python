if __name__ == "__main__":
    import sys
    from os.path import join, dirname

    sys.path.append(join(dirname(__file__), '..'))
    from whoami.identify.user import UserDao
    UserDao.create_table()
    UserDao.create('admin', 'password', 'admin')
    