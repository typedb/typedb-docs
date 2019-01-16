---
sidebarTitle: Aggregate
pageTitle: Aggregate Query
permalink: /docs/query/aggregate-query
---

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/java) or [Python](/docs/client-api/python)**: Executing an aggregate query is as simple as passing the Graql (string) query to the `query()` method available on the `transaction` object.
</div>

## Aggregate Values Over a Dataset
In this section, we learn how to get Grakn to calculate the `count`, `sum`, `max`, `mean`, `mean` and `median` values of a specific set of data in the knowledge graph.
To perform aggregation in Grakn, we first write a [match clause](/docs/query/match-clause) to describe the set of data and then use the `aggregate` query followed by one of the aggregate functions and the variable of interest.

### Count
We use the `count` function to get the number of the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $sh isa sheep; aggregate count;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var("sh").isa("person")
).aggregate(count());

List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

[Hope you manage to stay awake for the rest of the aggregate functions!](https://www.youtube.com/watch?v=FmbmNp1RDCE)

Optionally, `count` accepts a variable as an argument.

### Sum
We use the `sum` function to get the sum of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $h isa hotel has number-of-rooms $nor; aggregate sum $nor;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var("h").isa("hotel").has("number-of-rooms", var("nor"))
).aggregate(sum("nor"));

List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Maximum
We use the `max` function to get the maximum value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match (student: $st, school: $sch) isa school-enrollment; $st has gpa $gpa; aggregate max $gpa;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var().isa("school-enrollment").rel("student", "st").rel("school", "sch"),
  var("st").has("gpa", var("gpa"))
).aggregate(max("gpa"));

List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Minimum
We use the `min` function to get the minimum value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $b isa building has number-of-floors $nof; aggregate min $nof;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var().isa("school-enrollment").rel("student", "st").rel("school", "sch"),
  var("st").has("gpa", var("gpa"))
).aggregate(min("nof"));

List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Mean
We use the `mean` function to get the average value of the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $call isa call has duration $d; aggregate mean $d;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var("call").isa("call").has("duration", "d")
).aggregate(mean("d")).execute();

List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Median
We use the `median` function to get the median value among the specified `long` or `double` matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has age $a; aggregate median $a;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var("p").isa("person").has("age", var("a"))
).aggregate(median("a")).execute();

List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Grouping Answers
We use the `group` function, optionally followed by another aggregate function, to group the answers by the specified matched variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match (employer: $company, employee: $person) isa employment; aggregate group $company;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var().isa("employment").rel("employer", var("company"))
  .rel("employee", var("person"))
).aggregate(group("company")).execute();

List&lt;AnswerGroup&lt;ConceptMap&gt;&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;AnswerGroup&lt;ConceptMap&gt;&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query returns all instances of `employment` grouped by their `employer` roleplayer.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match (employer: $company, employee: $person) isa employment; aggregate group $company count;
```
[tab:end]

[tab:Java]
```lang-java
AggregateQuery query = Graql.match(
  var().isa("employment").rel("employer", var("company"))
  .rel("employee", var("person"))
).aggregate(group("company", count()));

List&lt;AnswerGroup&lt;Value&gt;&gt;answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;AnswerGroup&lt;Value&gt;&gt;answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query returns the total number of instances of `employment` mapped to their corresponding `employer` roleplayer.

## Summary
We use an aggregate query to calculate a certain variable as defined in the preceded `match` clause that describes a set of data in the knowledge graph.

Next, we learn how to [compute values over a large set of data](/docs/query/compute-query) in a knowledge graph.
