---
pageTitle: Insert Query
keywords: graql, insert query, insertion
longTailKeywords: grakn insert data, graql insert query, graql create instances
Summary: Insert queries in Grakn.
---

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a `insert` query, is as simple as calling the [`withTx().execute()`](../03-client-api/01-java.md#client-api-method-eagerly-execute-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a `insert` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a `insert` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#client-api-title-transaction) object.
</div>

## Insert Instances of an Entity Type
To insert an instance of an entity type into the knowledge graph, we use the `insert` keyword followed by what looks a lot like what we used for [matching instances of entities](../10-query/01-match-clause.md#match-instances-of-an-entity).

<div class="tabs dark">

[tab:Graql]
```graql
insert $p isa person, has full-name "John Parkson", has gender "male", has email "john.parkson@gmail.com", has phone-number "+44-1234=567890";
```
[tab:end]

[tab:Java]
```java
GraqlInsert query = Graql.insert(
  var("p").isa("person").has("full-name", "John Parkson").has("email", "john.parkson@gmail.com").has("phone-number", "+44-1234-567890")
);
```
[tab:end]
</div>

This `match insert` query:
1. Assigns the `surname` attribute of a `person` with `id` of `V41016` to variable `$s`.
2. Inserts a `person` entity with the `surname` attribute holding the value of the variable `$s`.

## Insert Instances of an Attribute Type
Similar to inserting an instance of an entity, to insert an instance of an attribute, we use the `insert` keyword followed by the variable pattern to describe the attribute of interest and its value.

<div class="tabs dark">

[tab:Graql]
```graql
insert $x isa emotion; $x "like";
```
[tab:end]

[tab:Java]
```java
GraqlInsert query = Graql.insert(
  var("x").isa("emotion").val("like")
);
```
[tab:end]
</div>

## Insert Instances of a Relation Type
Given the dependent nature of relations, inserting an instance of a relation is quite different from that of an entity. The roles of a relation to be inserted are expected to be played by instances that already exist in the knowledge graph. Therefore inserting a relation is always preceded by matching the roleplayers - what is commonly called the `match insert`. What follows the `insert` keyword looks a lot like what we used for [matching instances of relations](../10-query/01-match-clause.md#match-instances-of-a-relation).

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name "Facelook";
  $person isa person, has email "tanya.arnold@gmail.com";
insert $new-employment (employer: $org, employee: $person) isa employment;
  $new-employment has reference-id "WGFTSH";
```
[tab:end]

[tab:Java]
```java
GraqlInsert query = Graql.match(
  var("org").isa("organisation").has("name", "Facelook"),
  var("p").isa("person").has("email", "tanya.arnold@gmail.com")
).insert(
  var("emp").isa("employment").rel("employer", "org").rel("employee", "p").has("reference-id", "WGFTSH")
);
```
[tab:end]
</div>

This `match insert` query:
1. Matches the `organisation` that plays `employer`, assigned to variable `$c`.
2. Matches the `person` that plays `employee`, assigned to variable `$p`.
3. Inserts an `employment` relation with `$c` and `$p` as its roleplayers, assigned to variable `$emp`.
4. Inserts the ownership of `reference-id` with value `WGFTSH` by to the `$emp` relation instance.

## Summary
An `insert` query optionally preceded by a `match` clause is used to insert a data instance into the knowledge graph.

Next, we learn how to [delete data](../10-query/04-delete-query.md) from a knowledge graph.