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
To perform aggregation in Grakn, we first write a [match clause](/docs/query/match-clause) to describe the set of data and then use the `aggregate` query followed by one of the aggregate functions and the variable of interest.

### Count
We use the `count` function to get the number of the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $sce isa school-course-enrollment, has score $sco;
  $sco > 7.0;
aggregate count;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("sce").isa("school-course-enrollment").has("score", var("sco")),
  var("sco").val(gt(7.0))
).aggregate(count());
```
[tab:end]
</div>

Optionally, `count` accepts a variable as an argument.

### Sum
We use the `sum` function to get the sum of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name $orn;
  $orn == "Medicely";
  ($org) isa employment, has salary $sal;
aggregate sum $sal;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("org").isa("organisation").has("name", var("orn")),
  var("orn").val("Medicely"),
  var().rel("org").isa("employment").has("salary", var("sal"))
).aggregate(sum("sal"));
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
aggregate max $ran;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("sch").isa("school").has("ranking", var("ran"))
).aggregate(max("ran"));
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
aggregate min $sal;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var().rel(var("per")).isa("marriage"),
  var().rel(var("per")).isa("employment").has("salary", var("sal"))
).aggregate(min("sal"));
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
aggregate mean $sal;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("emp").isa("employment").has("salary", var("sal"))
).aggregate(mean("sal"));
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
  $orn == "Facelook";
  (employer: $org, employee: $per) isa employment;
  ($per) isa school-course-enrollment has score $sco;
aggregate median $sco;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("org").isa("organisation").has("name", var("orn")),
  var("orn").val("Facelook"),
  var().rel("employer", var("org")).rel("employee", var("per")).isa("employment"),
  var().rel(var("per")).isa("school-course-enrollment").has("score", var("sco"))
).aggregate(median("sco"));
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
  $scc isa school-course, has title $tit;
  (student: $per, enrolled-course: $scc) isa school-course-enrollment;
aggregate group $tit;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("per").isa("person"),
  var("scc").isa("school-course").has("title", var("tit")),
  var().rel("student", var("per")).rel("enrolled-course", var("scc")).isa("school-course-enrollment")
).aggregate(group("tit"));
```
[tab:end]
</div>

This query returns all instances of `person` grouped by the `title` of their `school-course`.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $per isa person;
  $scc isa school-course, has title $tit;
  (student: $per, enrolled-course: $scc) isa school-course-enrollment;
aggregate group $tit count;
```
[tab:end]

[tab:Java]
```java
AggregateQuery query = Graql.match(
  var("per").isa("person"),
  var("scc").isa("school-course").has("title", var("tit")),
  var().rel("student", var("per")).rel("enrolled-course", var("scc")).isa("school-course-enrollment")
).aggregate(group("tit", count()));
```
[tab:end]
</div>

This query returns the total count of `person`s grouped by the `title` of their `school-course`.

## Summary
We use an aggregate query to calculate a certain variable as defined in the preceded `match` clause that describes a set of data in the knowledge graph.

Next, we learn how to [compute values over a large set of data](/docs/query/compute-query) in a knowledge graph.
