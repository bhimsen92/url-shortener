create table if not exists urls (
  url_id text not null,
  original_url text not null,
  created_at timestamp without time zone not null,
  expires_at timestamp without time zone not null,
  created_by bigint,
  redirects_count bigint default 0
);

create unique index if not exists url_id_idx on urls(url_id);

