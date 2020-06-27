from db import DBMixin
from datetime import datetime, timedelta


class Urls(DBMixin):
    @classmethod
    def get_original_url(cls, url_id):
        query = "select original_url, expires_at from urls where url_id = %s"
        results = cls.get(query, (url_id,))
        rows = [
            {"original_url": result[0], "expires_at": result[1]}
            for result in results
        ]
        assert len(rows) <= 1
        return rows

    @classmethod
    def store_url(cls, original_url, url_id, created_by=None):
        query = """insert into urls (original_url, url_id, created_by, created_at, expires_at)
         values (%s, %s, %s, %s, %s)"""
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(days=2)
        results = cls.post(
            query, original_url, url_id, created_by, created_at, expires_at
        )
        return results
