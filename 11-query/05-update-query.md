---
pageTitle: Update Query
keywords: graql, update query, modification
longTailKeywords: grakn update data, graql update query, graql update instances
Summary: Updating data in Grakn with the Update Query.
---

## Update Instances of Concepts

In a Grakn knowledge graph, each instance is a "fact". Relations and entities are extensible and reducible, by adding or removing role players to them over time.
Each attribute value can be owned and the ownership can be removed or added: updating an attribute value directly therefore means changing the attribute value for ALL owners of this attribute value! 
Achieving this requires [deleting](../11-query/04-delete-query.md) the attribute value and connecting previous owners to a different value instance. 
Updating the attribute value that is owned by a concept means changing the connection to the value, rather than the value itself. We can achieve this in a single query using an Update query, which consists of a match, a delete, and an insert.

To try the following examples with one of the Grakn clients, follow these [Clients Guide](#clients-guide).

## Update attribute owned by a concept
Usually, we want to change the value of an attribute that is associated to another instance. To do so, we first need to [delete the association that the instance has with the attribute of interest](../11-query/04-delete-query.md#delete-attribute-ownerships) and then [insert the new instance of the attribute](../11-query/03-insert-query.md#insert-instances-of-an-attribute-type). We can do this in a single update query as follows:

<div class="tabs dark">

[tab:Graql]

```graql
## disconnecting from the old attribute value
match $org isa organisation, has name "Medicely", has registration-number $rn; 
delete $org has $rn;
insert $org has registration-number "81726354";
```
[tab:end]

[tab:Java]
```java
GraqlUpdate update_query = Graql.match(
  var("org").isa("organisation").has("name", "Medicely").has("registration-number", var("rn"))
).delete(
  var("org").has(var("rn"))
).insert(
  var("org").has("registration-number", "81726354")
);
```
[tab:end]
</div>

This query first deletes the association that the `organisation` with id `V17391` has with the instance of the `registration-number` attribute type and then continues to insert the new instance of the `registration-number` to be owned by the same instance of `organisation`.


### Update all instances of a given attribute
There may also be cases where we need to update the value of all instances of an attribute type. This amounts to _rewriting_ the value of an attribute fact. 
To do so, we can again make use of an update query.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $m isa media, has caption $c;
  $c contains "inappropriate word";
delete $c isa caption;
insert $m has caption "deleted";
```
[tab:end]

[tab:Java]
```java
GraqlUpdate update_query = Graql.match(
  var("m").isa("media").has("caption", var("c")),
  var("c").contains("inappropriate word")
).delete(
  var("c").isa("caption")
).insert(
  var("m").has("caption", "deleted")
);
```
[tab:end]
</div>

This query first looks for any instance of type `media` that owns the `caption` attribute containing an `"inappropriate word"`, then for each `media`-`attribute` pair it finds, deletes the caption and inserts a caption reading `deleted` in its place.


### Modifying a relation's role player

To replace a role player, we combine the steps for extending the relation, with steps for [deleting a role player](../11-query/04-delete-query.md#delete-role-players-from-relations):

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name "Pharos";
  $new-org isa organisation, has name "Medicely";
  $emp (employer: $org, employee: $p) isa employment;
delete
  $emp (employer: $org);
insert
  $emp (employer: $new-org);
```
[tab:end]

[tab:Java]
```java
GraqlUpdate update_query = Graql.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("new-org").isa("organisation").has("name", "Medicely"),
  var("emp").rel("employer", "org").rel("employee", "p").isa("employment")
).delete(
  var("emp").rel("employer", "org")
).insert(
  var("emp").rel("employer", "new-org")
);
```
[tab:end]
</div>

After these queries, all employments by the organisation named `Pharos` were replaced employments by the organisation named `Medicely`.

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing an `update` query, is as simple as calling the [`query().update()`](../03-client-api/01-java.md) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing an `update` query, is as simple as passing the Graql(string) query to the `query().update()` function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing an `update` query, is as simple as passing the Graql(string) query to the `query().update()` method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>


## Summary
Updating data in Graql is usually involves an update query, which takes the form of `match-delete-insert`. You can use these queries to
add and remove role players from relations, or add and remove ownerships of attributes. Attribute values themselves can be treated
as immutable, and changing their values amounts to deleting the value and moving all the ownerships of the old value to some 
new value.


Next, we learn how to [aggregate values over a set of data](../11-query/06-aggregate-query.md) in a Grakn knowledge graph.
