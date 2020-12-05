---
pageTitle: Updating Data
keywords: graql, update query, modification
longTailKeywords: grakn update data, graql update query, graql update instances
Summary: Updating data in Grakn.
---

## Update Instances of Concepts

In a Grakn knowledge graph, each instance is a "fact". Relations and entities are extensible and reducible, by adding or removing role players to them over time.
Each attribute value can be owned and the ownership can be removed or added: updating an attribute value directly therefore means changing the attribute value for ALL owners of this attribute value! 
Achieving this requires [deleting](../11-query/04-delete-query.md) the attribute value and connecting previous owners to a different value instance. 
Updating the attribute value that is owned by a concept means changing the connection to the value, rather than the value itself.

To try the following examples with one of the Grakn clients, follow these [Clients Guide](#clients-guide).

## Update attribute owned by a concept
Usually, we want to change the value of an attribute that is associated to another instance. To do so, we first need to [delete the association that the instance has with the attribute of interest](../11-query/04-delete-query.md#delete-attribute-ownerships) and then [insert the new instance of the attribute](../11-query/03-insert-query.md#insert-instances-of-an-attribute-type).

<div class="tabs dark">

[tab:Graql]

```graql
## disconnecting from the old attribute value
match $org isa organisation, has name "Medicely", has registration-number $rn; delete $org has registration-number $rn;

## connect the new attribute value
match $org isa organisation, has name "Medicely"; insert $org has registration-number "81726354";
```
[tab:end]

[tab:Java]
```java
GraqlDelete delete_query = Graql.match(
  var("org").isa("organisation").has("name", "Medicely").has("registration-number", var("rn"))
).delete(var("org").has("registration-number", var("rn")));

GraqlInsert insert_query = Graql.match(
  var("org").isa("organisation").has("name", "Medicely")
).insert(
  var("org").has("registration-number", "81726354")
);
```
[tab:end]
</div>

This query first deletes the association that the `organisation` with id `V17391` has with the instance of the `registration-number` attribute type and then continues to insert the new instance of the `registration-number` to be owned by the same instance of `organisation`.


### Update all instances of a given attribute
There may also be cases where we need to update the value of all instances of an attribute type. This amounts to _rewriting_ the value of an attribute fact. 
To do so, we first assign the new instance of the given attribute to all instances that own the old instance, and then delete the old instance of the attribute type.

<div class="tabs dark">

[tab:Graql]
```graql
## inserting the new
match
  $m isa media, has caption $c;
  $c contains "inappropriate word";
insert $m has caption "deleted";

## deleting the old
match $c isa caption; $c contains "inappropriate word"; delete $c isa caption;
```
[tab:end]

[tab:Java]
```java
GraqlInsert insert_query = Graql.match(
  var("m").isa("media").has("caption", var("c")),
  var("c").contains("inappropriate word")
).insert(
  var("m").has("caption", "deleted")
);

GraqlDelete delete_query = Graql.match(
  var("c").contains("inappropriate word").isa("caption")
).delete(var("c").isa("caption"));
```
[tab:end]
</div>

This query first looks for any instance of type `media` that owns the `caption` attribute containing an `"inappropriate word"` and then inserts the new instance of the `caption` attribute with the value of `"deleted"` to be owned by the matched owners. Finally, it deletes all instances of `caption` with the value of `"inappropriate word"`.

### Extending a relation with a new role player
We can add role players to a relation by `match`ing the relation and the concept that will be the new role player, and then insert the new role player into the same relation.

<div class="tabs dark">

[tab:Graql]
```graql
## inserting the new role player into some theoretical multi-employment relation
match
  $emp (employer: $org, $employee: $p) isa employment;
  $p2 isa person;
  $p2 != $p;
insert $emp ($employee: $p2) isa employment;
```
[tab:end]

[tab:Java]
```java
GraqlInsert insert_query = Graql.match(
 var("emp").rel("employer", var("org")).rel("employee", var("p")).isa("employment"),
  var("p").isa("person"),
  var("p2").isa("person"),
  var("p").neq(var("p2"))
).insert(
  var("emp").rel("employee", var("p2")).isa("employment")
);
```
[tab:end]
</div>


### Modifying a relation's role player

To replace a role player, we combine the steps for extending the relation, with steps for [deleting a role player](../11-query/04-delete-query.md#delete-role-players-from-relations):

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name "Pharos";
  $new-org isa organisation, has name "Medicely";
  $emp (employer: $org, employee: $p) isa employment;
insert
  $emp (employer: $new-org);

match
  $emp (employer: $org, employer: $new-org, employee: $p) isa employment;
  $org isa organisation, has name "Pharos";
  $new-org isa organisation, has name "Medicely";
delete
  $emp (employer: $org);
```
[tab:end]

[tab:Java]
```java
GraqlInsert query = Graql.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("new-org").isa("organisation").has("name", "Medicely"),
  var("emp").rel("employer", "org").rel("employee", "p").isa("employment")
).insert(var("emp").rel("employer", "new-org"));

GraqlDelete deleteQuery = Graql.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("new-org").isa("organisation").has("name", "Medicely"),
  var("emp").rel("employer", "org").rel("employer", "new-org").rel("employee", "p").isa("employment")
).delete(var("emp").rel("employer", "org"));
```
[tab:end]
</div>

After these queries, all employments by the organisation named `Pharos` were replaced employments by the organisation named `Medicely`.

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing `insert` and `delete` queries, is as simple as calling the [`execute()`](../03-client-api/01-java.md#eagerly-execute-a-graql-query) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing `insert` and `delete` queries, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing `insert` and `delete` queries, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>


## Summary
Updating data in Graql is usually a two step process: a `match-delete` followed by a `match-insert`. You can use these queries to
add and remove role players from relations, or add and remove ownerships of attributes. Attribute values themselves can be treated
as immutable, and changing their values amounts to deleting the value and moving all the ownerships of the old value to some 
new value.


Next, we learn how to [aggregate values over a set of data](../11-query/06-aggregate-query.md) in a Grakn knowledge graph.
