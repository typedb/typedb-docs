---
pageTitle: Delete Query
keywords: typeql, delete query, deletion
longTailKeywords: typedb delete data, typeql delete query, typeql delete instances
Summary: Delete queries in TypeDB.
---

## Delete Instances of a Type
To delete an instance of a type from the knowledge graph, we use a [match clause](../11-query/01-match-clause.md) followed by the `delete` keyword and statements indicating data to delete.
To try the following examples with one of the TypeDB clients, follows these [Clients Guide](#clients-guide).

Match-Delete queries are NOT lazy: the `match` will be fully evaluated and answers recorded, and each answer will in turn have
the operations specified in the `delete` clause applied. This avoids modifying the graph while traversing it.


<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has email "raphael.santos@gmail.com"; delete $p isa person;
```
[tab:end]

[tab:Java]
```java
TypeQLDelete query = TypeQL.match(
    var("p").isa("person").has("email", "raphael.santos@gmail.com")
).delete(var("p").isa("person"));
```
[tab:end]
</div>

This deletes a particular instance of the `person` type with the email `raphael.santos@gmail.com`. We must write the `isa` clause to tell
the parser to remove the instance of data represented by the variable `$p`. If we don't know the type, we can usually use `thing`,
the supertype of all data instances.

Deleting an instance of a relation type follows exactly the same style: 

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
  $org isa organisation, has name "Pharos";
  $emp (employer: $org, employee: $p) isa employment;
delete $emp isa employment;
```
[tab:end]

[tab:Java]
```java
TypeQLDelete query = TypeQL.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("emp").rel("employer", "org").rel("employee", "p").isa("employment")
).delete(var("emp").isa("employment"));
```
[tab:end]
</div>

This deletes all instances of the `employment` type where the `employer` is an `organisation` with `name` of `"Pharos"`.

Attributes are normally owned by other concepts (ie. `$x has attribute $a`). This means we can both delete an attribute
ownership, as in the next section, or delete the instance itself following the above style of using `isa` in the delete clause.

## Delete Attribute Ownerships
We can remove the ownership of an attribute by another concept in the same way it is inserted or queried: using the `has` clause.

Note that attributes with the same value and type are shared among their owners. For this reason, usually, an attribute is not deleted directly. 

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $t isa travel, has start-date $st; $d 2013-12-22; delete $t has $st;
```
[tab:end]

[tab:Java]
```java
TypeQLDelete query = TypeQL.match(
  var("t").isa("travel").has("start-date", var("st")),
  var("st").eq(LocalDate.of(2013, 12, 22).atStartOfDay())
).delete(var("t").has(var("st")));
```
[tab:end]
</div>

This looks for a `travel` that owns the attribute `start-date` with the value of `2013-12-22` in the `match` clause. 
We then disassociate the `travel` instance `$t` from the attribute `$st` with the `delete $t has $st` clause.

This will _not_ delete the entire instance of type `start-date` and value `2013-12-22` - it remains associated with any other instance that may own it.

If we had instead written the query as `match $t isa travel, has start-date $st;  $st == 2013-12-22"; delete $st isa start-date;`, 
we would have deleted the instance of `start-date` with value `2013-12-22` and its association with all other concept types that previously owned it.

Note also that you must not specify a type for the attribute when deleting, as this creates a derived `isa` constraint on the attribute. You must use `delete $t has $st`, _not_ `delete $t has start-date $st`.

## Delete Role Players from Relations

In TypeDB, existing relations can be extended with new role players, or shrunk by removing role players.
If an employer merged with another, we may have to reassign all existing `employment` relations to the new company.

To remove the old employer from the employment relation, we mirror the `delete` syntax with what the `insert` syntax 
for role players looks like.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match
  $org isa organisation, has name "Pharos";
  $emp (employer: $org, employee: $p) isa employment;
delete $emp (employer: $org);
```
[tab:end]

[tab:Java]
```java
TypeQLDelete query = TypeQL.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("emp").rel("employer", "org").rel("employee", "p").isa("employment")
).delete(var("emp").rel("employer", "org"));
```
[tab:end]
</div>

This TypeQL query will find all employments where the employer is an organisation with the name `Pharos`. It will then
remove the organisation from the employment relation. It is required to provide the role that the role player is playing
in the `delete` statement. If the role is unknown, it is possible to use the generic `role` supertype
in the `delete` block, though being as specific as possible is recommended.

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a `delete` query, is as simple as calling the [`query().delete()`](../03-client-api/01-java.md) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a `delete` query, is as simple as passing the TypeQL(string) query to the `query().delete()` function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a `delete` query, is as simple as passing the TypeQL(string) query to the `query().delete()` method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
The `delete` query preceded by a `match` clause is used to delete one or more facts from the knowledge graph.

We can delete instances by using `$var isa [your type]`: an `isa` will always indicate removal of an instance and all its edges.
Additionally, we can remove just attribute ownerships using the `has` statement in the `delete` clause. Removing
a role player from a relation can similarly be achieved by using role player syntax: `delete $r (some_role: $player);` without
an `isa` statement.

Next, we learn how to [update data](../11-query/05-update-query.md) in a TypeDB knowledge graph.
