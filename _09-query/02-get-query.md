---
sidebarTitle: Get
pageTitle: Get Query
permalink: /docs/query/get-query
---

## Retrieve Concept Types and Their Instances
The `get` query triggers a search in the knowledge graph based on what has been described in the preceding `match` clause.

## Get the Variables
Any variable that has been specified in the `match` clause can be returned as the answers of the `get` query. Let's look at an example of how variables can be asked for in the answer.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match
  $fr ($x, $y, $z) isa friendship;
  $x isa person has name $x-name;
  $x-name contains "John";
  $y isa person has name $y-name, has age $y-age;
  $z isa person has name $y-name, has age $z-age;
get $x-name, $y-name, $y-age, $z-name, $y-age;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("fr").isa("friendship").rel("x").rel("y").rel("z"),
  var("x").isa("person").has("name", var("x-name")),
  var("x-name").val(Predicates.contains("John")),
  var("y").isa("person").has("name", var("y-name")).has("age", var("y-age")),
  var("z").isa("person").has("name", var("z-name")).has("age", var("z-age")),
).get(var("x-name"), var("y-name"), var("y-age"), var("z-name"), var("z-age"));

List&lt;ConceptMap&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 Stream&lt;ConceptMap&gt; answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $fr ($x, $y, $z) isa friendship; $x isa person has name $x-name; $x-name contains "John"; $y isa person has name $y-name, has age $y-age; $z isa person has name $y-name, has age $z-age; get $x-name, $y-name, $y-age, $z-name, $y-age;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $fr ($x, $y, $z) isa friendship; $x isa person has name $x-name; $x-name contains "John"; $y isa person has name $y-name, has age $y-age; $z isa person has name $y-name, has age $z-age; get $x-name, $y-name, $y-age, $z-name, $y-age;')
```
[tab:end]
</div>

If no variable is specified after `get`, all variables specified in the `match` clause will be returned.

## Limit the Answers
We can chose to limit the number of answers in the results. To do this, we use the `limit` keyword followed by the desired number of answers.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person; limit 1; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("p").isa("person")
).limit(1).get();

List&lt;ConceptMap&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 Stream&lt;ConceptMap&gt; answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $p isa person; limit 1; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $p isa person; limit 1; get;")
```
[tab:end]
</div>

This query returns only one single (and random) instance of type `person`.

## Order the Answers
To order the answers by a particular variable, we use the `order` keyword followed by the variable by which we would like the results to be ordered. A second argument, `asc` (ascending) or `desc` (descending), determines the sorting method.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has age $age; order by $age asc; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("p").isa("person")
).limit(1).get();

List&lt;ConceptMap&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 Stream&lt;ConceptMap&gt; answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $p isa person has age $age; order by $age asc; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $p isa person has age $age; order by $age asc; get;")
```
[tab:end]

</div>

This query returns all instances of the `person` (entity) type ordered by their `age`.

<div class="note">
[Important]
Placing `order by` before and after the `limit` makes a big difference. `order by` followed by `limit` results in a global ordering of the instances, whereas `limit` coming before `order by` returns the ordered arbitrary number of instances.
</div>

## Offset the Answers
Often used in conjunction with `limit`, we use the `offset` keyword followed by the number we would like the answers to be offset by. This is commonly used to return a desired range of the answers.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has age $age; order by $age; offset 100; limit 10; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("p").isa("person").has("age", var("age"))
).orderBy(var("age")).offset(100).limit(10).get();

List&lt;ConceptMap&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 Stream&lt;ConceptMap&gt; answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $p isa person has age $age; order by $age; offset 100; limit 10; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $p isa person has age $age; order by $age; offset 100; limit 10; get;")
```
[tab:end]

</div>

This returns 10 instances of the `person` (entity) type starting from the 100th person ordered by their `age`.

## Summary
A `get` query is used to extract information out of the knowledge graph by describing the desired result in the preceding `match` clause. We use the modifiers `limit`, `order by` and `offset` to retrieve an optionally ordered subset of the matched instances.

Next, we will learn how to [insert data](/docs/query/insert-query) into a Grakn knowledge graph.