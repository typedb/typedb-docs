---
sidebarTitle: Get
pageTitle: Get Query
permalink: /docs/query/get-query
---

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing a `get` query, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eager-executation-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing a `get` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing a `get` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
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
GetQuery query = Graql.match(
  var("fr").isa("friendship").rel("x").rel("y"),
  var("x").isa("person").has("full-name", var("x-fn")),
  var("x-fn").val(contains("Miriam")),
  var("y").isa("person").has("full-name", var("y-fn")).has("phone-number", var("y-pn"))
).get(var("x-fn"), var("y-fn"), var("y-pn"));
```
[tab:end]</div>

If no variable is specified after `get`, all variables specified in the `match` clause are returned.

## Limit the Answers
We can chose to limit the number of answers in the results. To do this, we use the `limit` keyword followed by the desired number of answers.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person; limit 1; get;
```
[tab:end]

[tab:Java]
```java
GetQuery query = Graql.match(
  var("p").isa("person")
).limit(1).get();
```
[tab:end]</div>

This query returns only one single (and random) instance of type `person`.

## Order the Answers
To order the answers by a particular variable, we use the `order` keyword followed by the variable by which we would like the results to be ordered. A second argument, `asc` (ascending) or `desc` (descending), determines the sorting method.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $fn; order by $fn asc; get;
```
[tab:end]

[tab:Java]
```java
GetQuery query = Graql.match(
  var("p").isa("person").has("full-name", var("fn"))
).orderBy("fn", Order.asc).get();
```
[tab:end]
</div>

This query returns all instances of the `person` (entity) type ordered by their `full-name`.

<div class="note">
[Important]
Placing `order by` before and after the `limit` makes a big difference. `order by` followed by `limit` results in a global ordering of the instances, whereas `limit` coming before `order by` returns the ordered arbitrary number of instances.
</div>

## Offset the Answers
Often used in conjunction with `limit`, we use the `offset` keyword followed by the number we would like the answers to be offset by. This is commonly used to return a desired range of the answers.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $fn; order by $fn; offset 100; limit 10; get;
```
[tab:end]

[tab:Java]
```java
GetQuery query = Graql.match(
  var("p").isa("person").has("full-name", var("fn"))
).orderBy("fn").offset(6).limit(10).get();
```
[tab:end]
</div>

This returns 10 instances of the `person` (entity) type starting from the 6th person ordered by their `full-name`.

## Summary
A `get` query is used to extract information out of the knowledge graph by describing the desired result in the preceding `match` clause. We use the modifiers `limit`, `order by` and `offset` to retrieve an optionally ordered subset of the matched instances.

Next, we learn how to [insert data](/docs/query/insert-query) into a Grakn knowledge graph.