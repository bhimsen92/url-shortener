# Designing a URL Shortening service like TinyURL

Implementation is based on the article from educative's system design course.
[TinyURL](https://www.educative.io/courses/grokking-the-system-design-interview/m2ygV4E81AR)

> Apart from educative, I am thankfull to all the authors of countless articles that I went through
> to understand flask,redis,postgres and sharding. I am listing down some of the articles here:

1. [pgDash article of sharding](https://pgdash.io/blog/postgres-11-sharding.html).
2. Oriely: [Postgres Up and Running](https://www.oreilly.com/library/view/postgresql-up-and/9781491963401/).
3. [Snowflake](https://github.com/twitter-archive/snowflake/tree/snowflake-2010) from Twitter.
4. [Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) from Miguel Grinberg.

This application still needs improvment, especially sharding the db. I am still trying to understand
how logical/physical sharding is done and handled at the application level. I will update the repository as I learn more.

High Level Application Design
[picture here]

## Components

### Snowflake

Snowflake service is based on twitter snowflake service. Snowflake service generates unique ids by combining
timestamp,machine identifier and a counter in a 64 bit number.

The intuition is simple: date and time when converted to secods/milliseconds is readily available as a unique number. It is a monotincally increasing, never repeating number. But it is not enough if we have to deal with
multiple machines as 2 machines can generate same timestamp when requested at the same time. So to avoid that
we can append a machine id to the timestamp. But still we have a problem, if the service receives 100s requests in a given second/millisecond, timestamp+machine_id is not going to give us a unique number. So to avoid that, we need to append a counter to timestamp+machine_id string.

Now we don't want to this string to be big. The generated string which is a number should fit inside a 64 bit number. So we can slice up 64 bit number into 3 parts and assign each part to timestamp, machine id and counter.

First 41 bits is for timestamp, this gives 69 years(2^41 seconds) worth of time before it overflows. Next 10 buts is for machine id. This gives us opportunity to extend the snowflake service to 2^10 instances. The rest
can be given to counter(2^13). So within a microsecond, the service can handle up to 2^13 requests.

The python code for the above logic can be found [here](snowflake/id_generator.py)

### Postgres

Application makes use of partition techniques made available in postgres:12 release. Right now it partitions
the `urls` table by hash and distributes this into 2 shards. In my opinion partition by hash does not seem to help in the long run. May be there is a way to readjust the shards when we add more db instances. If no such provision exists then we may have to create 100s machines upfront to support the partition by hash.

Other way would be to logically shard the tables and scale it when the need arises. This has to be handled at the application level in my opinion as we have to maintain the shard metadata somewhere. I don't know how to achieve this at the moment. I will update the repo when understand how this can be achieved in the future.

Steps for setting up postgres can be found [here](scripts/db_urls.sql)

### Webserver

App serve is a simple flask application.

### How to run it.

```
1. Install docker and docker-compose on your machine.

-- start db instances.
2. docker-compose up master shard1 shard2

3. Follow the steps described [here](scripts/db_urls.sql) to setup the db.

4. cd snowflake && docker build -t url_shortener/snowflake .

5. cd web-server && docker build -t url_shortener/web-server .

-- start snowflake and web-server apps.
6. docker-compose up snowflake web-server
```
