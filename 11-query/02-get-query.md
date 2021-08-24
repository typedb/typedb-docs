---
pageTitle: Get Query
keywords: typeql, get query, retrieval, modifier
longTailKeywords: typedb retrieve data, typedb read data, typeql get query, typeql modifiers, typeql offset, typeql sort, typeql limit
Summary: Get (retrieval) queries and modifiers in TypeDB.
---

## Retrieve Concept Types and Their Instances
The `get` query triggers a search in the knowledge graph based on what has been described in the preceding `match` clause. To try the following examples with one of the TypeDB clients, follows these [Clients Guide](#clients-guide).

## Get the Variables
Any variable that has been specified in the `match` clause can be returned as the answers of the `get` query. Let's look at an example of how variables can be asked for in the answer.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
  $fr ($x, $y) isa friendship;
  $x isa person, has full-name $x-fn;
  $x-fn contains "Miriam";
  $y isa person, has full-name $y-fn, has phone-number $y-pn;
get $x-fn, $y-fn, $y-pn;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("fr").rel("x").rel("y").isa("friendship"),
  var("x").isa("person").has("full-name", var("x-fn")),
  var("x-fn").contains("Miriam"),
  var("y").isa("person").has("full-name", var("y-fn")).has("phone-number", var("y-pn"))
).get("x-fn", "y-fn", "y-pn");
```
[tab:end]</div>

If the `get` clause is omitted, all variables specified in the `match` clause are returned.

## Limit the Answers
We can chose to limit the number of answers in the results. To do this, we use the `limit` keyword followed by the desired number of answers.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person; get $p; limit 1;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Limited query = TypeQL.match(
  var("p").isa("person")
).get("p").limit(1);
```
[tab:end]</div>

This query returns only one single (and random) instance of type `person`.

## Sort the Answers
To sort the answers by a particular variable, we use the `sort` keyword followed by the variable by which we would like the results to be sorted. A second argument, `asc` (ascending) or `desc` (descending), determines the sorting method.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has full-name $fn; get $fn; sort $fn asc;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Sorted query = TypeQL.match(
  var("p").isa("person").has("full-name", var("fn"))
).get("fn").sort("fn", ASC);
```
[tab:end]
</div>

This query returns all instances of the `person` (entity) type sorted by their `full-name`.

## Offset the Answers
Often used in conjunction with `limit`, we use the `offset` keyword followed by the number we would like the answers to be offset by. This is commonly used to return a desired range of the answers.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has full-name $fn; get $fn; sort $fn; offset 6; limit 10;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Limited query = TypeQL.match(
  var("p").isa("person").has("full-name", var("fn"))
).get("fn").sort("fn").offset(6).limit(10);
```
[tab:end]
</div>

This returns 10 instances of the `person` (entity) type starting from the 6th person sorted by their `full-name`.


## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../04-client-api/01-java.md)**: Executing a `get` query, is as simple as calling the [`query().match()`](../04-client-api/01-java.md) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../04-client-api/03-nodejs.md)**: Executing a `get` query, is as simple as passing the TypeQL(string) query to the `query().match()` function available on the [`transaction`](../04-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../04-client-api/02-python.md)**: Executing a `get` query, is as simple as passing the TypeQL(string) query to the `query().match()` method available on the [`transaction`](../04-client-api/02-python.md#transaction) object.
</div>

## Summary
A `get` query is used to extract information out of the knowledge graph by describing the desired result in the preceding `match` clause. We use the modifiers `limit`, `sort` and `offset` to retrieve an optionally sorted subset of the matched instances.

Next, we learn how to [insert data](../11-query/03-insert-query.md) into a TypeDB knowledge graph.

