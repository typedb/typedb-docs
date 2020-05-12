---
pageTitle: Insert Query
keywords: graql, insert query, insertion
longTailKeywords: grakn insert data, graql insert query, graql create instances
Summary: Insert queries in Grakn.
---

## Insert Instances of an Entity Type
To insert an instance of an entity type into the knowledge graph, we use the `insert` keyword followed by a series of statements that are similar to [match patterns](../11-query/01-match-clause.md#match-instances-of-an-entity). To try the following examples with one of the Grakn clients, follows these [Clients Guide](#clients-guide).

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

This `insert` query inserts a `person` with a `full-name` attribute of `John Parkson`, an `email` attribute of `john.parkson@gmail.com` and a phone number of `+44-1234-567890`.

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
Given the dependent nature of relations, inserting an instance of a relation is quite different from that of an entity. The roles of a relation to be inserted are expected to be played by instances that already exist in the knowledge graph. Therefore inserting a relation is always preceded by matching the role players - what is commonly called the `match insert`. What follows the `insert` keyword, is a series of statements that are similar to the [match patterns](../11-query/01-match-clause.md#match-instances-of-a-relation).

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
  var("person").isa("person").has("email", "tanya.arnold@gmail.com")
).insert(
  var("new-employment").isa("employment").rel("employer", "org").rel("employee", "person").has("reference-id", "WGFTSH")
);
```
[tab:end]
</div>

This `match insert` query:
1. Matches the `organisation` that plays `employer`, assigned to variable `$org`.
2. Matches the `person` that plays `employee`, assigned to variable `$person`.
3. Inserts an `employment` relation with `$org` and `$person` as its role players, assigned to variable `$new-employment`.
4. Inserts the ownership of `reference-id` with value `WGFTSH` to the `$new-employment` relation instance.

### Duplicate Role Players

<div class="note">
    [New Behavior as of Grakn Core 1.7.0]
    As of Grakn 1.7.0, relations are allowed to have duplicate role players. 
</div>

This means we can model true reflexive relations. Taking `friendship` as an example

<div class="tabs dark">

[tab:Graql]
```graql
match
  $person isa person;
insert
  $reflexive-friendship (friend: $person, friend: $person) isa friendship;
```
[tab:end]

[tab:Java]
```java
GraqlInsert query = Graql.match(
  var("person").isa("person")
).insert(
  var("reflexive-friendship").isa("friendship").rel("friend", "person").rel("friend", "person")
);
```
[tab:end]
</div>

As a consequence, you can query for the duplicate role player as a duplicate role player and get an answer back:

<div class="tabs dark">

[tab:Graql]
```graql
match $friendship (friend: $p, friend: $p) isa friendship; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("friendship").isa("friendship").rel("friend", "p").rel("friend", "p")
).get();
```
[tab:end]
</div>

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a `insert` query, is as simple as calling the [`execute()`](../03-client-api/01-java.md#eagerly-execute-a-graql-query) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a `insert` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a `insert` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
An `insert` query optionally preceded by a `match` clause is used to insert a data instance into the knowledge graph.

Next, we learn how to [delete data](../11-query/04-delete-query.md) from a knowledge graph.
