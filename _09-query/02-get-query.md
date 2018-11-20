---
title: Get Query
keywords: graql, query, get
tags: [graql]
summary: "Retrieving data from a Grakn knowledge graph."
permalink: /docs/query/get-query
---

## Introduction
The `get` query triggers a search in the knowledge graph based on what has been described in the preceding `match` clause.

## Getting the Variables
Any variable that has been specified in the `match` clause can be returned as the answers of the `get` query. Let's look at an example of how variables can be asked for in the answer.

```graql
match
  $fr ($x, $y, $z) isa friendship;
  $x isa person has name $x-name;
  $x-name contains "John";
  $y isa person has name $y-name, has age $y-age;
  $z isa person has name $y-name, has age $z-age;
get $x-name, $y-name, $y-age, $z-name, $y-age;
```

If no variable is specified after `get`, all variables specified in the `match` clause will be returned.

## Limiting Results
To limit the number of results to be returned, we use the `limit` keyword followed by the number to limit the results to. Let's look at an example.

```graql
match $p isa person; limit 1; get;
```

This query returns only one random instance of type `person`.

## Ordering Results
To order the results by a particular variable, we use the `order` keyword followed by the variable we would like the results to be ordered by. A second argument determines of the order must be `asc` (ascending) or `desc` (descending). Let's look an example.

```graql
match $p isa person has age $age; order by $age asc; get;
```

This query returns all instances of type `person` ordered by their `age`.

Important: placing `order by` before and after the `limit` makes a big difference. `order by` followed by `limit` results in a global ordering of the instances, whereas `limit` coming before `order by` returns the ordered arbitrary number of instances.

## Offsetting Results
Often used in conjunction with `limit` and `order`, we use the `offset` keyword followed by the number we would like the results to be offset by. This is commonly used to return a desired range of the results. Let's look at an example.

```graql
match $p isa person has age $age; order by $age; limit 10; offset 100; get;
```

This query returns 10 instances of type `person` starting from the 100th youngest person.

## Summary
A `get` query is used to extract knowledge out of the knowledge graph by describing the desired result in the preceding `match` clause. We use the modifiers `limit`, `order by` and `offset` to retireve an optionally ordered subset of the matched instances.

Next, we will learn how to [insert data](/docs/query/insert-query) into a Grakn knowledge graph.