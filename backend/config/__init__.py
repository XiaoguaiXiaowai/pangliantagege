import pymysql

# Mock mysqlclient version to bypass Django check (needs to be >= 2.2.1 for Django 4.2+)
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()
