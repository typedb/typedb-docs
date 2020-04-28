---
pageTitle: Delete Query
keywords: graql, delete query, deletion
longTailKeywords: grakn delete data, graql delete query, graql delete instances
Summary: Delete queries in Grakn.
---

## Delete Instances of an Entity Type
To delete an instance of an entity type from the knowledge graph, we use a [match clause](../11-query/01-match-clause.md) followed by the `delete` keyword and statements indicating data to delete. To try the following examples with one of the Grakn clients, follows these [Clients Guide](#clients-guide).

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has email "raphael.santos@gmail.com"; delete $p isa person;
```
[tab:end]

[tab:Java]
```java
GraqlDelete query = Graql.match(
    var("p").isa("person").has("email", "raphael.santos@gmail.com")
).delete(var("p").isa("person"));
```
[tab:end]
</div>

This deletes a particular instance of the `person` type with the id of `V41016`. We must write the `isa` clause to tell
the parser to remove the instance of data represented by the variable `$p`. If we don't know the type, we can usually use `thing`,
the supertype of all data instances.

## Delete Instances of a Relation Type
To delete an instance of a relation type, similar to deleting an entity type, we first `match` and then `delete`.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name "Pharos";
  $emp (employer: $org, employee: $p) isa employment;
delete $emp isa employment;
```
[tab:end]

[tab:Java]
```java
GraqlDelete query = Graql.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("emp").isa("employment").rel("employer", "org").rel("employee", "p")
).delete(var("emp").isa("employment"));
```
[tab:end]
</div>

This deletes all instances of the `employment` type where the `employer` is an `organisation` with `name` of `"Pharos"`.

## Delete Attribute Ownerships
We can remove the ownership of an attribute by another concept in the same way it is inserted or queried: using the `has` clause.

Note that attributes with the same value are shared among their owners, so we can't just delete the attribute directly. It's important that one understands thoroughly how [attributes are defined](../09-schema/01-concepts.md#define-an-attribute).

<div class="tabs dark">

[tab:Graql]
```graql
match $t isa travel, has start-date $d; $d 2013-12-22; delete $t has $d;
```
[tab:end]

[tab:Java]
```java
GraqlDelete query = Graql.match(
  var("t").isa("travel").has("start-date", var("st")),
  var("st").val(LocalDate.of(2013, 12, 22).atStartOfDay())
).delete(var("r").has(var("st")));
```
[tab:end]
</div>

TODO continue from here:
This looks for a `travel` that owns the attribute `start-date` with the value of `2013-12-22`, captures the association between the attribute and the owner as the variable `$r` and finally deletes `$r`. This ensures that the attribute instance of type `start-date` and value `2013-12-22` remains associated with any other instance that may own it.

If we had instead written the query as `match $t isa travel, has start-date $st;  $st == 2013-12-22"; delete $st;`, we would have deleted the instance of `start-date` with value `2013-12-22` and its association with all other concept types that previously owned it.

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a `delete` query, is as simple as calling the [`execute()`](../03-client-api/01-java.md#eagerly-execute-a-graql-query) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a `delete` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a `delete` query, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
The `delete` query preceded by a `match` clause is used to delete one or more data instances from the knowledge graph.

Next, we learn how to [update data](../11-query/05-updating-data.md) in a Grakn knowledge graph.