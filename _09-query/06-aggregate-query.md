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

```graql
match $sh isa sheep; aggregate count;
```

[Hope you manage to stay awake for the rest of the aggregate functions!](https://www.youtube.com/watch?v=FmbmNp1RDCE){:target="_blank"}

Optionally, `count` accepts a variable as an argument.

### Sum
We use the `sum` function to get the sum of the given `long` or `double` variables in the results.

```graql
match $h isa hotel has number-of-rooms $nor; aggregate sum $nor;
```

### Maximum
We use the `max` function to get the maximum value among the given `long` or `double` variables in the results.

```graql
match (student: $st, school: $sch) isa school-enrollment; $st has gpa $gpa; aggregate max $gpa;
```

### Minimum
We use the `min` function to get the minimum value among the given `long` or `double` variables in the results.

```graql
match $b isa building has number-of-floors $nof; aggregate min $nof;
```

### Mean
We use the `mean` function to get the average value of the given `long` or `double` variables in the results.

```graql
match $call isa call has duration $d; aggregate mean $d;
```

### Median
We use the `median` function to get the median value among the given `long` or `double` variables in the results.

```graql
match $p isa person has age $a; aggregate median $a;
```

### Grouping Results
We use the `group` function, optionally followed by another aggregate function, to group the results by the given variable.

```graql
match (employer: $company, employee: $person) isa employment; aggregate group $company;
```

This query returns all instances of `employment` group by their `employer` roleplayer.

```graql
match (employer: $company, employee: $person) isa employment; aggregate group $company count;
```

This query returns the total number of instances of `employment` mapped to their corresponding `employer` roleplayer.

## Summary
An aggregate query, given a function, is used to calculate a given variable as defined in the preceded `match` clause that describes a set of data in the knowledge graph.

Next, we will learn how to [compute values over a large set of data](/docs/query/compute-query) in a knowledge graph.
