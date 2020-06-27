# Designing a URL Shortening service like TinyURL

Implementation is based on the article from educative's system design course.
[TinyURL](https://www.educative.io/courses/grokking-the-system-design-interview/m2ygV4E81AR)

> Apart from educative, I am thankfull to all the authors of countless articles that I went through
> to understand topics of flask,redis,postgres and sharding. I am listing down some of the articles
> which helped me clear many of my doubts.

1. [pgDash article of sharding](https://pgdash.io/blog/postgres-11-sharding.html).
2. Oriely: [Postgres Up and Running](https://www.oreilly.com/library/view/postgresql-up-and/9781491963401/).
3. [Snowflake](https://github.com/twitter-archive/snowflake/tree/snowflake-2010) from Twitter.
4. [Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) from Miguel Grinberg.

This application still needs improvment, especially at sharding the db. I am still trying to understand
how logical/physical sharding is done and handled at the application level. I will update the repository as I learn more.

High Level Application Design
[picture here]

Components

## Snowflake

## Postgres

Steps for setting up postgres can be found [here](scripts/db_urls.sql)

## Webserver

## How to run it.
