---
sidebarTitle: Compute
pageTitle: Compute Query
permalink: /docs/query/compute-query
---

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/java) or [Python](/docs/client-api/python)**: Executing a compute query is as simple as passing the Graql (string) query to the `query()` method available on the `transaction` object.
</div>

## Computing Distributed Analytics Over a Large Dataset
In this section, we learn how to use the `compute` queries in a Grakn knowledge graph to:
- calculate statistical values over a large set of data,
- find the shortest path between two instances of data,
- find the most important instance in the entire knowledge graph or a subset of it, and
- identify clusters of interconnected instances or those that are tightly linked within a network.

<!-- In a dedicated section, we learn more about the significance and use cases of [Distributed Analaytics]() in a Grakn knowledge graph. -->

## Compute Statistics
Computing simple statistics, such as the mean and standard deviations of small datasets, is an easy task given isolated instances. But what about when the knowledge graph becomes so large that it has to be distributed across many machines? What if the values to be calculated correspond to many different types?

That's when the `compute` query and its statistical functions come into play. The compute query uses an intelligent algorithm to traverse the knowledge graph using multiple threads in parallel.

### Count
We use the `count` function to get the number of instances of a specified type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute count in person;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.COUNT).in("person")
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

To count all instances of all types in the entire knowledge graph, we run the query as follows.

```lang-graql
compute count;
```

### Sum
We use the `sum` function to get the sum of the specified `long` or `double` attribute among all instances of a given type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute sum of number-of-rooms, in hotel;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.SUM).of("number-of-rooms").in("hotel")
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

### Maximum
We use the `max` function to get the maximum value among the specified `long` or `double` attribute among all instances of a given type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute max of gpa, in school-enrollment;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.MAX).of("gpa").in("school-enrollment");
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

### Minimum
We use the `min` function to get the minimum value among the specified `long` or `double` attribute among all instances of a given type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute max of number-of-floors, in building;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.MAX).of("number-of-floors").in("building");
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

### Mean
We use the `mean` function to get the average value of the specified `long` or `double` attribute among all instances of a given time.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute mean of duration, in call;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.MEAN).of("duration").in("call");
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

### Median
We use the `median` function to get the median value of the specified `long` or `double` attribute among all instances of a given type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute median of age, in person;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.MEDIAN).of("age").in("person");
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

### Standard Deviation
We use the `std` function to get the standard deviation value of the specified `long` or `double` attribute among all instances of a given type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute std of score, in examination;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.STD).of("score").in("examination");
List&lt;Value&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;Value&gt; answer = transaction.execute(query.toString());  -->
[tab:end]
</div>

### Statistical Compute vs. Aggregate
Aggregate queries run single-threaded on a single machine, whereas compute queries run in parallel across multiple machines.

Aggregate queries can run on a specific set of data described by a match clause, whereas compute queries are meant for large sets of data optionally filtered by a concept type.

## Compute the Shortest Path
We can use the compute query to find the shortest path between two instances of data.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute path from V24819, to V93012;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.PATH).from(ConceptId.of("V24819")).to(ConceptId.of("V93012"));
List&lt;ConceptList&gt; answer = query.withTx(transaction).execute();

```
<!-- List&lt;ConceptList&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

As the answer to this query, we would get a list of ids starting with `V24819` and ending with `V93012`. In between come the ids that connect the two.

### Specify a whitelist
When looking for the shortest path, we may need to constraint the shortest path to only include certain types. In other words, when given a whitelist of types, Grakn ignores any other path that leads to a type not included in the list. To do this, we use the `in` keyword followed by the list of allowed types.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute path from V24819, to V93012, in [person, car, company, employment];
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.PATH).from(ConceptId.of("V24819")).to(ConceptId.of("V93012")).in("person","car", "company", "employment");
List&lt;ConceptList&gt; answer = query.withTx(transaction).execute();

```
<!-- List&lt;ConceptList&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

Given that `V24819` is the id of a `person` and `V93012` is the id of a `car`, we are asking for the shortest path between the given `car` and `person` through an `employment` relationship with the `company`. Any other indirect association between the given person and car is ignored when looking for the shortest path.

<div class="note">
[Note]
When specifying the whitelist, the types of the `from` and `to` instances must always be included.
</div>

## Find the Most Interesting Instances
The centrality of an instance can be an indicator of its significance. The most interconnected of instances in a Grakn knowledge graph are those that are expected to be the most interesting in their domain. Graql uses two methods for computing centrality - Degree and K-core.

### Compute centrality using degree
The degree of an instance is the number of other instances directly connected to it. To compute the centrality of an entire Grakn knowledge graph using the degree of instances, we run the following query.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute centrality using degree;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.CENTRALITY).using(GraqlSyntax.Compute.Algorithm.DEGREE);
List&lt;ConceptSetMeasure&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query returns a map of instances ordered ascendingly by degree. Instances with the degree of 0 are excluded from the answers.

#### In a subgraph
Depending on the domain that the knowledge graph represents, we may want to compute the centrality on specific types. To do so, we use the `in` keyword followed by a list of the types that indicate importance. Let's look at an example that recognises companies with the highest number of employees as the most important.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute centrality in [company, employee, employment], using degree;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.CENTRALITY).in("company", "employee", "employment").using(GraqlSyntax.Compute.Algorithm.DEGREE);
List&lt;ConceptSetMeasure&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query returns a map of instances ordered ascendingly by degree. The instances included in the answers are those of types `company`, `employee` and `employment`.

#### Of a given type
Consider the example above. What we are really interested in is the company with the most number of employees, but we are also getting the employee and employment instances in the answers. What if we only want to get the centrality of a given type based on its relationship with other types without getting irrelevant answers. To do this, we use the `of` keyword.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute centrality of company in [company, employment], using degree;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.CENTRALITY).
of("company").in("company", "employment")
.using(GraqlSyntax.Compute.Algorithm.DEGREE);

List&lt;ConceptSetMeasure&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Compute centrality using k-core
Coreness is a measure that helps identify tightly interlinked sets of instances within the knowledge graph. Given value `k`, k-core makes the maximal subgraph where every instance has at least [degree](#compute-centrality-using-degree) `k`.

To compute centrality using coreness with the `k` value of at least 2, we run the following query.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute centrality using k-core;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.CENTRALITY).using(GraqlSyntax.Compute.Algorithm.K_CORE);
List&lt;ConceptSetMeasure&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query returns a map representing a list of all `id`s for each `k` value found in the knowledge graph.

#### Specify the minimum k value
To compute centrality using coreness with a given minimum `k` value, we use of the `where` keyword followed by an assignment of `min-k`. For example, if we were to compute centrality where every contained instance had at least a degree of 5, we would write the query as follows.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute centrality using k-core, where min-k = 5;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery query = Graql.compute(GraqlSyntax.Compute.Method.CENTRALITY)
.using(GraqlSyntax.Compute.Algorithm.K_CORE)
.where(GraqlSyntax.Compute.Argument.min_k(5));

List&lt;ConceptSetMeasure&gt; answer = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

## Identify Clusters
Clusters in a Grakn knowledge graph are disjoint groups of instances that represent interconnected subsets of the entire knowledge graph. There are two ways to identify clusters in Grakn - using Connected Component and using K-Core.

### Compute clusters using connected component
The connected component algorithm retrieves clusters regardless of how tightly the instances in each cluster are connected. Let's look at an example.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute cluster in [person, employment, organisation], using connected-component;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery&lt;ConceptSet&gt; query = Graql.compute(GraqlSyntax.Compute.Method.CLUSTER).
in("person", "employment", "organisation").
using(GraqlSyntax.Compute.Algorithm.CONNECTED_COMPONENT);

List&lt;ConceptSet&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query retrieves the set of concept IDs that belong to clusters which include instances of `person`, `employment` and `organisation` concept types.

### Retrieve the cluster that contains a given instance
We can retrieve a cluster that contains a given instance, by using the `where` keyword.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute cluster in [person, employment, organisation], using connected-component, where contains=V12488;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery&lt;ConceptSet&gt; query = Graql.compute(GraqlSyntax.Compute.Method.CLUSTER).
in("person", "employment", "organisation").
using(GraqlSyntax.Compute.Algorithm.CONNECTED_COMPONENT).
where(GraqlSyntax.Compute.Argument.contains(ConceptId.of("V12488")));

List&lt;ConceptSet&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

### Compute clusters using k-core
Coreness is a measure that helps identify tightly interlinked sets of instances within the knowledge graph. Given value `k`, k-core makes the maximal subgraph where every instance has at least degree `k`.
Grakn uses K-core to identify tightly connected clusters within the knowledge graph.

To compute clusters using coreness with the `k` value of at least 2, we run the following query.


<div class="tabs dark">

[tab:Graql]
```lang-graql
compute cluster in [person, employment, organisation], using k-core;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery&lt;ConceptSet&gt; query = Graql.compute(GraqlSyntax.Compute.Method.CLUSTER).
in("person", "employment", "organisation").
using(GraqlSyntax.Compute.Algorithm.K_CORE);

List&lt;ConceptSet&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query retrieves the set of concept IDs that belong to clusters which include instances of `person`, `employment` and `organisation` concept types and all have a minimum degree of 2.

#### Specify the minimum k value
To compute clusters using coreness with a given minimum `k` value, we use of the `where` keyword followed by an assignment of `min-k`.

<div class="tabs dark">

[tab:Graql]
```lang-graql
compute cluster in [person, employment, organisation], using k-core, where min-k=5;
```
[tab:end]

[tab:Java]
```lang-java
ComputeQuery&lt;ConceptSet&gt; query = Graql.compute(GraqlSyntax.Compute.Method.CLUSTER).
in("person", "employment", "organisation").
using(GraqlSyntax.Compute.Algorithm.K_CORE).
where(GraqlSyntax.Compute.Argument.min_k(5));


List&lt;ConceptSet&gt; answers = query.withTx(transaction).execute();
```
<!-- 1.5 List&lt;ConceptSetMeasure&gt; answer = transaction.execute(query.toString()); -->
[tab:end]
</div>

This query retrieves the set of concept IDs that belong to clusters which include instances of `person`, `employment` and `organisation` concept types and all have a minimum degree of 5.

## Summary
We use a compute query to run distributed analytics on the entire knowledge graph or a large subset of it filtered by a concept type. This statistical analytics include statistical function, shortest path, centrality and cluster

Next, we learn about the [Concept API](/docs/concept-api/overview) and how it is used via the [Grakn Clients](/docs/client-api/overview) to retrieve information on a specific instance and its surroundings.