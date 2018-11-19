---
title: Compute Query
keywords: graql, compute, match
tags: [graql]
summary: "Computing values over a large set of data in a Grakn knowledge graph."
permalink: /docs/query/compute-query
---

## Introduction
In this section, we will learn how to use `compute` queries in a Grakn knowledge graph to:
- calculate statistical values over a large set of data,
- find the shortest path between two instances of data,
- find the most important instance in the entire knowledge graph or a subset of it, and
- identify clusters of interconnected instances or those that are tightly linked within a network.

In a dedicated section, we will learn more about the significance and use cases of [Distributed Analaytics]() in a Grakn knowledge graph.

## Computing Statistics
Computing simple statistics, such as the mean and standard deviations of small datasets, is an easy task given isolated instances. But what about when the knowledge graph becomes so large that it has to be distributed across many machines? What if the values to be calculated correspond to many different types?

That's when the `compute` query and its statistical functions come into play. The compute query uses an intelligent algorithm to traverse the knowledge graph using multiple threads in parallel.

### Count
We use the `count` function to get the total number of instances of a given type.

```graql
compute count in person;
```

To count all instances of any type in the entire knowledge graph, we run the query as follows.

```graql
compute count;
```

### Sum
We use the `sum` function to get the sum of the given `long` or `double` attribute among all instances of a given type.

```graql
compute sum of number-of-rooms, in hotel;
```

### Maximum
We use the `max` function to get the maximum value among the given `long` or `double` attribute among all instances of a given type.

```graql
compute max of gpa, in school-enrollment;
```

### Minimum
We use the `min` function to get the minimum value among the given `long` or `double` attribute among all instances of a given type.

```graql
compute max of number-of-floors, in building;
```

### Mean
We use the `mean` function to get the average value of the given `long` or `double` attribute among all instances of a given time.

```graql
compute mean of duration, in call;
```

### Median
We use the `median` function to get the median value of the given `long` or `double` attribute among all instances of a given type.

```graql
compute median of age, in person;
```

### Standard Deviation
We use the `std` function to get the standard deviation value of the given `long` or `double` attribute among all instances of a given type.

```graql
compute std of score, in examination;
```

### Compute vs. Aggregate
Aggregate queries run single-threaded on a single machine, whereas compute queries run in parallel across multiple machines.

Aggregate queries can run on a specific set of data described by a match clause, whereas compute queries are meant for large sets of data filtered by types.

## Computing Shortest Path
We can use the compute query to find the shortest path between two instances in a Grakn knowledge graph. Let's look at an example.

```graql
compute path from V24819, to V93012;
```
As the answer to this query, we would get a list of ids starting with `V24819` and ending with `V93012`, with ids that connect them coming it between.

### Specifying a whitelist
When looking for the shortest path, we may need to constraint the shortest path to only include certain types. In other words, when given a whitelist of types, Grakn ignores any other path that leads to a type not included in the list. To do this, we use the `in` keyword followed by the list of allowed types. Let's look at an example.

```graql
compute path from V24819, to V93012, in [person, car, company, employment];
```

Given that `V24819` is the id of a `person` and `V93012` is the id of a `car`, we are asking for the shortest path between the given `car` and `person` through an `employment` relationship with the `company`. Any other indirect association between the given person and car will be ignored when looking for the shortest path.

Note that when specifying the whitelist, the types of the `from` and `to` instances must always be included.

## Finding the most interesting instances
The centrality of an instance can be an indicator of significance. The most interconnected of instances in a knowledge graph are those that are expected to be the most interesting in their domain. Graql uses two methods for computing centrality - Degree and K-core.

### Computing centrality using degree
The degree of an instance is the number of other instances directly connected to it. To compute the centrality of an entire knowledge graph using the degree of the instances, we run the following query.

```graql
compute centrality using degree;
```

This returns a map of instances ordered ascendingly by degree. Instances with the degree of 0 will be excluded from the results.

#### In a subgraph
Depending on the domain that the knowledge graph represents, we may want to compute centrality on the types that indicate the importance of the instances. To do so, we use the `in` keyword followed by a list of the types that indicate importance. Let's look at an example that recognises companies with the highest number of employees as the most important.

```graql
compute centrality in [company, employee, employment], using degree;
```

This returns an ascendingly ordered map that contains instances of `company`, `employee` and `employment` each mapped with their degree.


#### Of a given type
Consider the example above. What we are really interested in is the company with the most number of employees, but we're also getting the employee and employment instances in the results. What if we only want to get the centrality of a given type based on its relationship with other types without getting irrelevant instances in the results. To do this, we use the `of` keyword. Let's look at an example.

```graql
compute centrality of company in [company, employment], using degree;
```

### Computing centrality using k-core
Coreness isa measure that helps identify tightly interlinked sets of instances within the knowledge graph. Given value `k`, k-core makes the maximal subgraph where every instance has at least degree `k`.

To compute the coreness centrality of any `k` value higher than 1, we run the following query.

```graql
compute centrality using k-core;
```

This returns a map representing a list of all `id`s for each `k` value found in the knowledge graph.

#### Specifying minimum k value
To compute coreness with a given minimum `k` value we use of the `where` keyword followed by an assignment of `min-k`. For example, we would like to obtain subgraphs where every contained instance has at least a degree of 5, we would write the query as follows.

```graql
compute centrality using k-core, where min-k = 5;
```

## Computing clusters
<<To be added>