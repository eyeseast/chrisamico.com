---
title: Setting defaults in Datasette's canned queries
summary: Two SQL functions give us a better starting point
---

One of [Datasette's](https://datasette.io/) best features is [canned queries](https://docs.datasette.io/en/stable/sql_queries.html#canned-queries).

A canned query lets me create a stable URL for a SQL query. If I'm working on a project with reporters where we're asking questions of the data we've collected, we can encode those questions as SQL and bookmark the answers. If it's a database that's being updated -- [wildfires, for example](https://github.com/eyeseast/wildfires-2025) -- I can refer back to the same URL to see what's changed.

Using [named parameters](https://docs.datasette.io/en/stable/sql_queries.html#canned-query-parameters) has another cool effect: It creates a form field I can use to filter that view. But this comes with a drawback.

Let's say I want to quickly see all the fires in one state. I might write a canned query like this:

```sql
SELECT
    *
FROM
    `fires`
where
    attr_POOState = :state;
```

When I load the URL for that query, I'll have no results, because the generated query filters on `where attr_POOState = ""` and nothing matches that. In this case, I might not know that states are written like `US-CA`, and so I might spend time filling in junk values like `california` and `ca` and `US-ca`.

The trick is using two functions -- `coalesce` and `nullif` -- to set a default value if the input is blank.

```sql
SELECT
    *
FROM
    `fires`
where
    attr_POOState = coalesce(NULLIF(:state, ''), 'US-CA')
```

Now the default view loads California wildfires, and it gives the user a clue about the specific formatting in this dataset.
