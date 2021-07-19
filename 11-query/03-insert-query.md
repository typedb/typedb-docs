---
pageTitle: Insert Query
keywords: typeql, insert query, insertion
longTailKeywords: typedb insert data, typeql insert query, typeql create instances
Summary: Insert queries in TypeDB.
---

## Insert Instances of an Entity Type
To insert an instance of an entity type into the knowledge graph, we use the `insert` keyword followed by a series of statements that are similar to [match patterns](../11-query/01-match-clause.md#match-instances-of-an-entity). To try the following examples with one of the TypeDB clients, follows these [Clients Guide](#clients-guide).

<div class="tabs dark">

[tab:TypeQL]
```typeql
insert $p isa person, has full-name "John Parkson", has gender "male", has email "john.parkson@gmail.com", has phone-number "+44-1234-567890";
```
[tab:end]

[tab:Java]
```java
TypeQLInsert query = TypeQL.insert(
  var("p").isa("person").has("full-name", "John Parkson").has("email", "john.parkson@gmail.com").has("phone-number", "+44-1234-567890")
);
```
[tab:end]
</div>

This `insert` query inserts a `person` with a `full-name` attribute of `John Parkson`, an `email` attribute of `john.parkson@gmail.com` and a phone number of `+44-1234-567890`.

## Insert Instances of an Attribute Type
Similar to inserting an instance of an entity, to insert an instance of an attribute, we use the `insert` keyword followed by the variable pattern to describe the attribute of interest and its value.

<div class="tabs dark">

[tab:TypeQL]
```typeql
insert $x isa emotion; $x "like";
```
[tab:end]

[tab:Java]
```java
TypeQLInsert query = TypeQL.insert(
  var("x").eq("like").isa("emotion")
);
```
[tab:end]
</div>

## Insert Instances of a Relation Type
Given the dependent nature of relations, inserting an instance of a relation is quite different from that of an entity. The roles of a relation to be inserted are expected to be played by instances that already exist in the knowledge graph. Therefore inserting a relation is always preceded by matching the role players - what is commonly called the `match insert`. What follows the `insert` keyword, is a series of statements that are similar to the [match patterns](../11-query/01-match-clause.md#match-instances-of-a-relation).

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
  $org isa organisation, has name "Facelook";
  $person isa person, has email "tanya.arnold@gmail.com";
insert $new-employment (employer: $org, employee: $person) isa employment;
  $new-employment has reference-id "WGFTSH";
```
[tab:end]

[tab:Java]
```java
TypeQLInsert query = TypeQL.match(
  var("org").isa("organisation").has("name", "Facelook"),
  var("person").isa("person").has("email", "tanya.arnold@gmail.com")
).insert(
  var("new-employment").rel("employer", "org").rel("employee", "person").has("reference-id", "WGFTSH").isa("employment")
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
[Note]
As of version 1.7.0, relations are allowed to have duplicate role players. 
</div>

This means we can model true reflexive relations. Taking `friendship` as an example

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
  $person isa person;
insert
  $reflexive-friendship (friend: $person, friend: $person) isa friendship;
```
[tab:end]

[tab:Java]
```java
TypeQLInsert query = TypeQL.match(
  var("person").isa("person")
).insert(
  var("reflexive-friendship").rel("friend", "person").rel("friend", "person").isa("friendship")
);
```
[tab:end]
</div>

As a consequence, you can query for the duplicate role player as a duplicate role player and get an answer back:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $friendship (friend: $p, friend: $p) isa friendship; get $friendship;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("friendship").rel("friend", "p").rel("friend", "p").isa("friendship")
).get("friendship");
```
[tab:end]
</div>

### Extending a relation with a new role player
We can add role players to a relation by `match`ing the relation and the concept that will be the new role player, and then insert the new role player into the same relation.

<div class="tabs dark">

[tab:TypeQL]
<!-- test-ignore -->
```TypeQL
## inserting the new friendship to a friendship list
match
  $julie isa person, has full-name "Julie Hutchinson";
  $miriam isa person, has full-name "Miriam Morton";
  $f ($julie, $miriam) isa friendship;
  $list (owner: $miriam) isa friendship-list, has title "best friends";
insert $list (listed: $f);
```
[tab:end]

[tab:Java]
<!-- test-ignore -->
```java
TypeQLInsert insert_query = TypeQL.match(
  var("julie").isa("person").has("name", "Julie Hutchinson"),
  var("miriam").isa("person").has("name", "Miriam Hutchinson"),
  var("f").rel(var("julie")).rel(var("miriam")).isa("friendship"),
  var(list).rel("owner", var("miriam")).isa("friendship-list").has("title", "best friends")
).insert(
  var("list").rel("listed", var("f"))
);
```
[tab:end]
</div>


## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing an `insert` query, is as simple as calling the [`query().insert()`](../03-client-api/01-java.md) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing an `insert` query, is as simple as passing the TypeQL(string) query to the `query().insert()` function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing an `insert` query, is as simple as passing the TypeQL(string) query to the `query().insert()` method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
An `insert` query optionally preceded by a `match` clause is used to insert a data instance into the knowledge graph.

Next, we learn how to [delete data](../11-query/04-delete-query.md) from a knowledge graph.
