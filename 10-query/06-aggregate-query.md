---
sidebarTitle: Aggregate
pageTitle: Aggregate Query
permalink: /docs/query/aggregate-query
---

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing a `aggregate` query, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eager-executation-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing a `aggregate` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing a `aggregate` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
</div>

## Aggregate Values Over a Dataset
In this section, we learn how to get Grakn to calculate the `count`, `sum`, `max`, `mean`, `mean` and `median` values of a specific set of data in the knowledge graph.
To perform aggregation in Grakn, we first write a [`match` clause](/docs/query/match-clause) to describe the set of data, then follow that by [`get`](/docs/query/get-query) to retrieve a distinct set of answers based on the specified variables, and lastly an aggregate function to perform on the variable of interest.

### Count
We use the `count` function to get the number of the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $sh isa sheep; get $sh; count;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("sh").isa("sheep")
).get("sh").count();
```
[tab:end]
</div>

[Hope you manage to stay awake for the rest of the aggregate functions!](https://www.youtube.com/watch?v=FmbmNp1RDCE)

Optionally, `count` accepts a variable as an argument.

### Sum
We use the `sum` function to get the sum of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $h isa hotel, has number-of-rooms $nor; get $nor; sum $nor;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("h").isa("hotel").has("number-of-rooms", var("nor"))
).get("nor").sum("nor");
```
[tab:end]
</div>

### Maximum
We use the `max` function to get the maximum value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match (student: $st, school: $sch) isa school-enrollment; $st has gpa $gpa; get $gpa; max $gpa;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var().isa("school-enrollment").rel("student", "st").rel("school", "sch"),
  var("st").has("gpa", var("gpa"))
).get("gpa").max("gpa");
```
[tab:end]
</div>

### Minimum
We use the `min` function to get the minimum value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $b isa building, has number-of-floors $nof; get $nof; min $nof;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("b").isa("building").has("number-of-floors", var("nof"))
).get("nof").min("nof");
```
[tab:end]
</div>

### Mean
We use the `mean` function to get the average value of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $call isa call, has duration $d; get $d; mean $d;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("call").isa("call").has("duration", var("d"))
).get("d").mean("d");
```
[tab:end]
</div>

### Median
We use the `median` function to get the median value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has age $a; get $a; median $a;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("p").isa("person").has("age", var("a"))
).get("a").median("a");
```
[tab:end]
</div>

### Grouping Answers
We use the `group` function, optionally followed by another aggregate function, to group the answers by the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match (employer: $c, employee: $p) isa employment; get $c; group $c;
```
[tab:end]

[tab:Java]
```java
GroupQuery query = Graql.match(
  var().isa("employment").rel("employer", var("c"))
  .rel("employee", var("p"))
).get("c", "p").group("c");
```
[tab:end]
</div>

This query returns all instances of `employment` grouped by their `employer` roleplayer.

<div class="tabs dark">

[tab:Graql]
```graql
match (employer: $c, employee: $p) isa employment; get $c; group $c; count;
```
[tab:end]

[tab:Java]
```java
GroupAggregateQuery query = Graql.match(
  var().isa("employment").rel("employer", var("c"))
  .rel("employee", var("p"))
).get("c", "p").group("c").count();
```
[tab:end]
</div>

This query returns the total number of instances of `employment` mapped to their corresponding `employer` roleplayer.

## Summary
We use an aggregate query to calculate a certain variable as defined in the preceded `match` clause that describes a set of data in the knowledge graph.

Next, we learn how to [compute values over a large set of data](/docs/query/compute-query) in a knowledge graph.
