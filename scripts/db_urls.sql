-- on all db instances execute following command.
create extension postgres_fdw;

-- on master db server setup shard instances.
create server shard1 foreign data wrapper postgres_fdw
options (host 'shard1', port '5432', dbname 'url_shortener_db');

create server shard2 foreign data wrapper postgres_fdw
options (host 'shard2', port '5432', dbname 'url_shortener_db');

-- create user mapping between master and shards.
create user mapping for postgres server shard1
options (user 'postgres', password 'postgres');

create user mapping for postgres server shard2
options (user 'postgres', password 'postgres');

-- create urls table on shard1 and shard2 instances. It should be an exact replica of the table on master -
-- instance.
create table if not exists urls_shard_1 (
  url_id text not null,
  original_url text not null,
  created_at timestamp without time zone not null,
  expires_at timestamp without time zone not null,
  created_by bigint,
  redirects_count bigint default 0
);
create unique index if not exists url_id_idx on urls_shard_1(url_id);

create table if not exists urls_shard_2 (
  url_id text not null,
  original_url text not null,
  created_at timestamp without time zone not null,
  expires_at timestamp without time zone not null,
  created_by bigint,
  redirects_count bigint default 0
);
create unique index if not exists url_id_idx on urls_shard_2(url_id);

-- on master db server.
create table if not exists urls (
  url_id text not null,
  original_url text not null,
  created_at timestamp without time zone not null,
  expires_at timestamp without time zone not null,
  created_by bigint,
  redirects_count bigint default 0
) partition by hash(url_id);

-- now link the partitions as a foriegn table in your master server.
create foreign table urls_shard_1 partition of urls
for values with (modulus 2, remainder 0)
server shard1;

create foreign table urls_shard_2
partition of urls
for values with (modulus 2, remainder 1)
server shard2;