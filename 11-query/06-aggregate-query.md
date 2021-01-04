---
pageTitle: Aggregate Query
keywords: graql, aggregate query, calculation, statistics
longTailKeywords: grakn aggregate data, graql aggregate query, graql statistics
Summary: Statistical queries in Grakn.
---

## Aggregate Values Over a Dataset
In this section, we learn how to get Grakn to calculate the `count`, `sum`, `max`, `mean`, `mean` and `median` values of a specific set of data in the knowledge graph.
To perform aggregation in Grakn, we first write a [`match` clause](../11-query/01-match-clause.md) to describe the set of data, then follow that by [`get`](../11-query/02-get-query.md) to retrieve a distinct set of answers based on the specified variables, and lastly an aggregate function to perform on the variable of interest.

To try the following examples with one of the Grakn clients, follows these [Clients Guide](#clients-guide).

### Count
We use the `count` function to get the number of the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $sce isa school-course-enrollment, has score $sco;
  $sco > 7.0;
get $sco; count;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Aggregate query = Graql.match(
  var("sce").isa("school-course-enrollment").has("score", var("sco")),
  var("sco").gt(7.0)
).get("sce").count();
```
[tab:end]
</div>

<div class="note">
[Note]
When more than one variable follows the `get` keyword, the `count` function is applied on the unique set of the retrieved variables. This is also the case, when no variable follows `get`, which actually means all matched variables are included.
</div>

### Sum
We use the `sum` function to get the sum of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name $orn;
  $orn "Medicely";
  ($org) isa employment, has salary $sal;
get $sal; sum $sal;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Aggregate query = Graql.match(
  var("org").isa("organisation").has("name", var("orn")),
  var("orn").eq("Medicely"),
  var().rel("org").isa("employment").has("salary", var("sal"))
).get("sal").sum("sal");
```
[tab:end]
</div>

### Maximum
We use the `max` function to get the maximum value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $sch isa school, has ranking $ran;
get $ran; max $ran;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Aggregate query = Graql.match(
  var("sch").isa("school").has("ranking", var("ran"))
).get("ran").max("ran");
```
[tab:end]
</div>

### Minimum
We use the `min` function to get the minimum value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  ($per) isa marriage;
  ($per) isa employment, has salary $sal;
get $sal; min $sal;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Aggregate query = Graql.match(
  var().rel(var("per")).isa("marriage"),
  var().rel(var("per")).isa("employment").has("salary", var("sal"))
).get("sal").min("sal");
```
[tab:end]
</div>

### Mean
We use the `mean` function to get the average value of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $emp isa employment, has salary $sal;
get $sal; mean $sal;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Aggregate query = Graql.match(
  var("emp").isa("employment").has("salary", var("sal"))
).get("sal").mean("sal");
```
[tab:end]
</div>

### Median
We use the `median` function to get the median value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name $orn;
  $orn "Facelook";
  (employer: $org, employee: $per) isa employment;
  ($per) isa school-course-enrollment, has score $sco;
get $sco; median $sco;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Aggregate query = Graql.match(
  var("org").isa("organisation").has("name", var("orn")),
  var("orn").eq("Facelook"),
  var().rel("employer", var("org")).rel("employee", var("per")).isa("employment"),
  var().rel(var("per")).isa("school-course-enrollment").has("score", var("sco"))
).get("sco").median("sco");
```
[tab:end]
</div>

### Grouping Answers
We use the `group` function, optionally followed by another aggregate function, to group the answers by the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $per isa person;
  $scc isa school-course, has title $title;
  (student: $per, enrolled-course: $scc) isa school-course-enrollment;
get $scc, $title; group $title;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Group query = Graql.match(
  var("per").isa("person"),
  var("scc").isa("school-course").has("title", var("title")),
  var().rel("student", var("per")).rel("enrolled-course", var("scc")).isa("school-course-enrollment")
).get("scc", "title").group("title");
```
[tab:end]
</div>

This query returns all instances of `person` grouped by the `title` of their `school-course`.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $per isa person;
  $scc isa school-course, has title $title;
  (student: $per, enrolled-course: $scc) isa school-course-enrollment;
get $scc, $title; group $title; count;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Unfiltered.Group.Aggregate query = Graql.match(
  var("per").isa("person"),
  var("scc").isa("school-course").has("title", var("title")),
  var().rel("student", var("per")).rel("enrolled-course", var("scc")).isa("school-course-enrollment")
).get("scc", "title").group("title").count();
```
[tab:end]
</div>

This query returns the total count of `person`s grouped by the `title` of their `school-course`.

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a `aggregate` query, is as simple as calling the [`execute()`](../03-client-api/01-java.md#eagerly-execute-a-graql-query) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a `aggregate` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a `aggregate` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
We use an aggregate query to calculate a certain variable as defined in the preceded `match` clause that describes a set of data in the knowledge graph.

Next, we learn how to [compute values over a large set of data](../11-query/07-compute-query.md) in a knowledge graph.
