---
pageTitle: Updating Data
keywords: graql, update query, modification
longTailKeywords: grakn update data, graql update query, graql update instances
Summary: Updating data in Grakn.
---

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing `insert` and `delete` queries, is as simple as calling the [`withTx().execute()`](../03-client-api/01-java.md#client-api-method-eagerly-execute-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing `insert` and `delete` queries, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing `insert` and `delete` queries, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#client-api-title-transaction) object.
</div>

## Update Instances of Concept Types
In a Grakn Knowledge Graph, updating a data instance is essentially [deleting](../10-query/04-delete-query.md) the current instance followed by [inserting](../10-query/03-insert-query.md) the new instance.

## Update Instances of an Attribute Type
In most cases, a concept type is expected to own only one instance of an attribute and, therefore, the value of its attribute may need to be updated. To do so, we first need to [delete the association that the instance has with the attribute of interest](../10-query/04-delete-query.md#delete-associations-with-attributes) and then [insert the new instance of the attribute](../10-query/03-insert-query.md#insert-instances-of-an-attribute-type).

<div class="tabs dark">

[tab:Graql]

```graql
## deleting the old
match $org isa organisation, has name "Medicely", has registration-number $rn via $r; delete $r;

## inserting the new
match $org isa organisation, has name "Medicely"; insert $org has registration-number "81726354";
```
[tab:end]

[tab:Java]
```java
GraqlDelete delete_query = Graql.match(
  var("org").isa("organisation").has("name", "Medicely").has("registration-number", var("rn"), var("r"))
).delete("r");

GraqlInsert insert_query = Graql.match(
  var("org").isa("organisation").has("name", "Medicely")
).insert(
  var("org").has("registration-number", "81726354")
);
```
[tab:end]
</div>

This query first deletes the association that the `organisation` with id `V17391` has with the instance of the `registration-number` attribute type by using the `via` keyword and then continues to insert the new instance of the `registration-number` to be owned by the same instance of `organisation`.


### Update all instances of a given attribute
There may also be cases where we need to update the value of all instances of an attribute type. To do so, we first assign the new instance of the given attribute to all instances that own the old instance, and then delete the old instance of the attribute type.

<div class="tabs dark">

[tab:Graql]
```graql
## inserting the new
match
  $m isa media, has caption $c;
  $c contains "inappropriate word";
insert $m has caption "deleted";

## deleting the old
match $c isa caption; $c contains "inappropriate word"; delete $c;
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
  var("c").isa("caption").contains("inappropriate word")
).delete("c");
```
[tab:end]
</div>

This query first looks for any instance of type `media` that owns the `caption` attribute containing an `"inappropriate word"` and then inserts the new instance of the `caption` attribute with the value of `"deleted"` to be owned by the matched owners. Finally, it deletes all instances of `caption` with the value of `"inappropriate word"`.

### Update the roleplayers of a relation
To change the roleplayers of a given relation, we first need to [delete the instances of the relation](../10-query/04-delete-query.md#delete-instances-of-a-relation-type) with the current roleplayers and [insert the new instance of the relation](../10-query/03-insert-query.md#insert-instances-of-a-relation-type) with the new roleplayers.

<div class="tabs dark">

[tab:Graql]
```graql
## inserting the new
match
  $p isa person, has name "Amabo";
  $org isa organisation, has name "Etihw Esouh";
insert $emp (employer: $org, $employee: $p) isa employment;

## deleting the old
match
  $p isa person, has name "Prumt";
  $org isa organisation, has name "Etihw Esouh";
  $emp (employer: $org, $employee: $p) isa employment;
delete $emp;
```
[tab:end]

[tab:Java]
```java
GraqlInsert insert_query = Graql.match(
  var("p").isa("person").has("name", "Amabo"),
  var("org").isa("organisation").has("name", "Wieth Souhe")
).insert(
  var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
);

GraqlDelete delete_query = Graql.match(
  var("p").isa("person").has("name", "Prumt"),
  var("org").isa("organisation").has("name", "Wieth Souhe"),
  var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
).delete("emp");
```
[tab:end]
</div>

This query updates the `employee` roleplayer of the `employment` relation where the `employer` is an `organisation` named `"Wieth Souhe"`.

## Summary
Due to the expressivity of Graql, updating instances requires a thorough understanding of the underlying logic as explained when [defining the schema](../09-schema/01-concepts.md). Simply put, to update is essentially to first `delete` and then `insert`.

Next, we learn how to [aggregate values over a set of data](../10-query/06-aggregate-query.md) in a Grakn knowledge graph.