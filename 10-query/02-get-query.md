---
pageTitle: Get Query
keywords: graql, get query, retrieval, modifier
longTailKeywords: grakn retrieve data, grakn read data, graql get query, graql modifiers, graql offset, graql sort, graql limit
Summary: Get (retrieval) queries and modifiers in Grakn.
---

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a `get` query, is as simple as calling the [`withTx().execute()`](../03-client-api/01-java.md#client-api-method-eagerly-execute-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a `get` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a `get` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#client-api-title-transaction) object.
</div>

## Retrieve Concept Types and Their Instances
The `get` query triggers a search in the knowledge graph based on what has been described in the preceding `match` clause.

## Get the Variables
Any variable that has been specified in the `match` clause can be returned as the answers of the `get` query. Let's look at an example of how variables can be asked for in the answer.

<div class="tabs dark">

[tab:Graql]
```graql
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
GraqlGet query = Graql.match(
  var("fr").isa("friendship").rel("x").rel("y"),
  var("x").isa("person").has("full-name", var("x-fn")),
  var("x-fn").contains("Miriam"),
  var("y").isa("person").has("full-name", var("y-fn")).has("phone-number", var("y-pn"))
).get("x-fn", "y-fn", "y-pn");
```
[tab:end]</div>

If no variable is specified after `get`, all variables specified in the `match` clause are returned.

## Limit the Answers
We can chose to limit the number of answers in the results. To do this, we use the `limit` keyword followed by the desired number of answers.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person; get; limit 1;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("p").isa("person")
).get().limit(1);
```
[tab:end]</div>

This query returns only one single (and random) instance of type `person`.

## Order the Answers
To order the answers by a particular variable, we use the `order` keyword followed by the variable by which we would like the results to be ordered. A second argument, `asc` (ascending) or `desc` (descending), determines the sorting method.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $fn; get; sort $fn asc;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("p").isa("person").has("full-name", var("fn"))
).get().sort("fn", ASC);
```
[tab:end]
</div>

This query returns all instances of the `person` (entity) type ordered by their `full-name`.

<div class="note">
[Important]
Placing `order` before and after the `limit` makes a big difference. `order` followed by `limit` results in a global ordering of the instances, whereas `limit` coming before `order` returns the ordered arbitrary number of instances.
</div>

## Offset the Answers
Often used in conjunction with `limit`, we use the `offset` keyword followed by the number we would like the answers to be offset by. This is commonly used to return a desired range of the answers.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $fn; get; sort $fn; offset 100; limit 10;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("p").isa("person").has("full-name", var("fn"))
).get().sort("fn").offset(6).limit(10);
```
[tab:end]
</div>

This returns 10 instances of the `person` (entity) type starting from the 6th person ordered by their `full-name`.

## Summary
A `get` query is used to extract information out of the knowledge graph by describing the desired result in the preceding `match` clause. We use the modifiers `limit`, `order` and `offset` to retrieve an optionally ordered subset of the matched instances.

Next, we learn how to [insert data](../10-query/03-insert-query.md) into a Grakn knowledge graph.