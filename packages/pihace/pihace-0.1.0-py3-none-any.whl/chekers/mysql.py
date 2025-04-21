from mysql.connector import connect, Error
from ..base_checker import BaseChecker

class MySQL(BaseChecker):
    def __init__(self, dsn):
        self.dsn = dsn

    def check(self):
        try:
            conn = connect(option_files=None, **self._parse_dsn())
            conn.close()
            return True
        except Error as e:
            return (False, str(e))
        except Exception:
            return (False, "pihace: log are unavailable")

    def _parse_dsn(self):
        # Very basic DSN parser: "mysql://user:pass@host/db"
        import re
        match = re.match(r'mysql://(.*?):(.*?)@(.*?)/(.*)', self.dsn)
        if not match:
            raise ValueError("Invalid DSN format")

        user, password, host, database = match.groups()
        return {
            "user": user,
            "password": password,
            "host": host,
            "database": database
        }
