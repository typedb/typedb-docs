---
title: Aggregate Query
keywords: graql, query, aggregate
tags: [graql]
summary: "Aggregating values from a set of data in a Grakn knowledge graph."
permalink: /docs/query/aggregate-query
---

## Introduction
In this section, we will learn how to get Grakn to calculate the `count`, `sum`, `max`, `mean`, `mean` and `median` values of a specific set of data in the knowledge graph.

## The Aggregate Query
To perform aggregation in Grakn, we first write a [match clause](/docs/query/match-clause) to describe the set of data and then use the `aggregate` query followed by one of the aggregate functions and the variable of interest.

### Count
We use the `count` function to get the number of answers found in the match.

<div class="tabs">

[tab:Graql]
```graql
match $sh isa sheep; aggregate count;
```
[tab:end]

[tab:Java]
```java
List&lt;Value&gt; answer = queryBuilder.match(
  var("sh").isa("person")
).aggregate(count()).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match $sh isa sheep; aggregate count;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match $sh isa sheep; aggregate count;")
```
[tab:end]
</div>

[Hope you manage to stay awake for the rest of the aggregate functions!](https://www.youtube.com/watch?v=FmbmNp1RDCE){:target="_blank"}

Optionally, `count` accepts a variable as an argument.

### Sum
We use the `sum` function to get the sum of the given `long` or `double` variables in the results.

<div class="tabs">

[tab:Graql]
```graql
match $h isa hotel has number-of-rooms $nor; aggregate sum $nor;
```
[tab:end]

[tab:Java]
```java
List&lt;Value&gt; answer = queryBuilder.match(
  var("h").isa("hotel").has("number-of-rooms", var("nor"))
).aggregate(sum("nor")).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match $h isa hotel has number-of-rooms $nor; aggregate sum $nor;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match $h isa hotel has number-of-rooms $nor; aggregate sum $nor;")
```
[tab:end]
</div>

### Maximum
We use the `max` function to get the maximum value among the given `long` or `double` variables in the results.


<div class="tabs">

[tab:Graql]
```graql
match (student: $st, school: $sch) isa school-enrollment; $st has gpa $gpa; aggregate max $gpa;
```
[tab:end]

[tab:Java]
```java
List&lt;Value&gt; answer = queryBuilder.match(
  var().isa("school-enrollment").rel("student", "st").rel("school", "sch"),
  var("st").has("gpa", var("gpa"))
).aggregate(max("gpa")).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match (student: $st, school: $sch) isa school-enrollment; $st has gpa $gpa; aggregate max $gpa;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match (student: $st, school: $sch) isa school-enrollment; $st has gpa $gpa; aggregate max $gpa;")
```
[tab:end]
</div>

### Minimum
We use the `min` function to get the minimum value among the given `long` or `double` variables in the results.

<div class="tabs">

[tab:Graql]
```graql
match $b isa building has number-of-floors $nof; aggregate min $nof;
```
[tab:end]

[tab:Java]
```java
List&lt;Value&gt; answer = queryBuilder.match(
  var("b").isa("building").has("number-of-floors", "nof")
).aggregate(min("nof")).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match $b isa building has number-of-floors $nof; aggregate min $nof;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match $b isa building has number-of-floors $nof; aggregate min $nof;")
```
[tab:end]
</div>

### Mean
We use the `mean` function to get the average value of the given `long` or `double` variables in the results.

<div class="tabs">

[tab:Graql]
```graql
match $call isa call has duration $d; aggregate mean $d;
```
[tab:end]

[tab:Java]
```java
List&lt;Value&gt; answer = queryBuilder.match(
  var("call").isa("call").has("duration", "d")
).aggregate(mean("d")).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match $call isa call has duration $d; aggregate mean $d;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match $call isa call has duration $d; aggregate mean $d;")
```
[tab:end]
</div>

### Median
We use the `median` function to get the median value among the given `long` or `double` variables in the results.

<div class="tabs">

[tab:Graql]
```graql
match $p isa person has age $a; aggregate median $a;
```
[tab:end]

[tab:Java]
```java
List&lt;Value&gt; answer = queryBuilder.match(
  var("p").isa("person").has("age", var("a"))
).aggregate(median("a")).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match $p isa person has age $a; aggregate median $a;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match $p isa person has age $a; aggregate median $a;")
```
[tab:end]
</div>

### Grouping Results
We use the `group` function, optionally followed by another aggregate function, to group the results by the given variable.

<div class="tabs">

[tab:Graql]
```graql
match (employer: $company, employee: $person) isa employment; aggregate group $company;
```
[tab:end]

[tab:Java]
```java
List&lt;AnswerGroup&lt;ConceptMap&gt;&gt; answer = queryBuilder.match(
  var().isa("employment").rel("employer", var("company")).rel("employee", var("person"))
).aggregate(group("company")).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match (employer: $company, employee: $person) isa employment; aggregate group $company;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match (employer: $company, employee: $person) isa employment; aggregate group $company;")
```
[tab:end]
</div>

This query returns all instances of `employment` group by their `employer` roleplayer.

<div class="tabs">

[tab:Graql]
```graql
match (employer: $company, employee: $person) isa employment; aggregate group $company count;
```
[tab:end]

[tab:Java]
```java
List<AnswerGroup&lt;Value&gt;> answer = queryBuilder.match(
  var().isa("employment").rel("employer", var("company")).rel("employee", var("person"))
).aggregate(group("company", count())).execute();
```
[tab:end]

[tab:Javascript]
```javascript
const answer = await transaction.query("match (employer: $company, employee: $person) isa employment; aggregate group $company count;");
```
[tab:end]

[tab:Python]
```python
answer = transaction.query("match (employer: $company, employee: $person) isa employment; aggregate group $company count;")
```
[tab:end]
</div>

This query returns the total number of instances of `employment` mapped to their corresponding `employer` roleplayer.

## Summary
An aggregate query, given a function, is used to calculate a given variable as defined in the preceded `match` clause that describes a set of data in the knowledge graph.

Next, we will learn how to [compute values over a large set of data](/docs/query/compute-query) in a knowledge graph.
