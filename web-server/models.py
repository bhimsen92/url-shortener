from db import DBMixin


class Urls(DBMixin):
    @classmethod
    def get_original_url(cls, url_id):
        query = "select original_url, expires_at from urls where url_id = %s"
        results = cls.get(query, (url_id,))
        rows = [
            {"original_url": result.original_url, "expires_at": result.expires_at}
            for result in results
        ]
        assert len(rows) <= 1
        return rows

    @classmethod
    def store_url(cls, original_url, url_id, created_by=None):
        query = """insert into urls (original_url, url_id, created_by) values (%s, %s, %s)"""
        results = cls.post(query, (original_url, url_id, created_by,))
        return results
