from db import DBMixin


class Urls(DBMixin):
    def get_original_url(self, url_id):
        query = "select original_url, expires_at from urls where url_id = %s"
        results = self.get(query, (url_id,))
        rows = [
            {"original_url": result.original_url, "expires_at": result.expires_at}
            for result in results
        ]
        assert len(rows) == 1
        return rows

    def store_url(self, original_url, url_id, created_by=None):
        query = """
        insert into urls (original_url, url_id, created_by)
        values (%s, %s, %s)
      """
        results = self.post(query, (original_url, url_id, created_by,))
        return results
