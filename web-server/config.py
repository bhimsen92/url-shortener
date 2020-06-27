import os


class Config:
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "postgres")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("PORT", 5432)
    db_name = os.environ.get("DB_NAME", "url_shortener_db")
    snowflake_host = os.environ.get("SNOWFLAKE_HOST", "localhost")
    snowflake_port = os.environ.get("SNOWFLAKE_PORT", 5000)
