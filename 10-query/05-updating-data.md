---
sidebarTitle: Update
pageTitle: Updating Data
permalink: /docs/query/updating-data
---

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing `insert` and `delete` queries, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eager-executation-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing `insert` and `delete` queries, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing `insert` and `delete` queries, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
</div>

## Update Instances of Concept Types
In a Grakn Knowledge Graph, updating a data instance is essentially [deleting](/docs/query/delete-query) the current instance followed by [inserting](/docs/query/insert-query) the new instance.

## Update Instances of an Attribute Type
In most cases, a concept type is expected to own only one instance of an attribute and, therefore, the value of its attribute may need to be updated. To do so, we first need to [delete the association that the instance has with the attribute of interest](/docs/query/delete-query#delete-associations-with-attributes) and then [insert the new instance of the attribute](/docs/query/insert-query#insert-instances-of-an-attribute-type).

<div class="tabs dark">

[tab:Graql]
<!-- test edge case -->
<!-- ignore-test -->
```graql
## deleting the old
match $org id V17391, has registration-number $rn via $r; delete $r;

## inserting the new
insert $org isa organisation, has registration-number "81726354";
```
[tab:end]

[tab:Java]
```java
DeleteQuery delete_query = Graql.match(
  var("org").id("V17391").has("registration-number", var("rn"), var("r"))
).delete("r");

InsertQuery insert_query = Graql.insert(
  var("org").id("V17391").has("registration-number", "81726354")
);
```
[tab:end]
</div>

This query first deletes the association that the `organisation` with id `V17391` has with the instance of the `registration-number` attribute type by using the `via` keyword and then continues to insert the new instance of the `registration-number` to be owned by the same instance of `organisation`.


### Update all instances of a given attribute
There may also be cases where we need to update the value of all instances of an attribute type. To do so, we first assign the new instance of the given attribute to all instances that own the old instance, and then delete the old instance of the attribute type.

<div class="tabs dark">

[tab:Graql]
<!-- test edge case -->
<!-- ignore-test -->
```graql
match $m isa media, has caption $c; $c contains "inappropriate word"; insert $m has caption "deleted";
match $c isa caption; $c contains "inappropriate word"; delete $c;
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.match(
  var("m").isa("media").has("caption", var("c")),
  var("c").val(contains("inappropriate word"))
).insert(
  var("m").has("caption", "deleted")
);

DeleteQuery delete_query = Graql.match(
  var("c").isa("caption").val(contains("inappropriate word"))
).delete("c");
```
[tab:end]
</div>

This query first looks for any instance of type `media` that owns the `caption` attribute containing an `"inappropriate word"` and then inserts the new instance of the `caption` attribute with the value of `"deleted"` to be owned by the matched owners. Finally, it deletes all instances of `caption` with the value of `"inappropriate word"`.

### Update the roleplayers of a relationship
To change the roleplayers of a given relationship, we first need to [delete the instances of the relationship](/docs/query/delete-query#delete-instances-of-a-relationship-type) with the current roleplayers and [insert the new instance of the relationship](/docs/query/insert-query#insert-instances-of-a-relationship-type) with the new roleplayers.

<div class="tabs dark">

[tab:Graql]
<!-- test edge case -->
<!-- ignore-test -->
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
InsertQuery insert_query = Graql.match(
  var("p").isa("person").has("name", "Amabo"),
  var("org").isa("organisation").has("name", "Wieth Souhe")
).insert(
  var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
);

DeleteQuery delete_query = Graql.match(
  var("p").isa("person").has("name", "Prumt"),
  var("org").isa("organisation").has("name", "Wieth Souhe"),
  var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
).delete("emp");
```
[tab:end]
</div>

This query updates the `employee` roleplayer of the `employment` relationship where the `employer` is an `organisation` named `"Wieth Souhe"`.

## Summary
Due to the expressivity of Graql, updating instances requires a thorough understanding of the underlying logic as explained when [defining the schema](/docs/schema/concepts). Simply put, to update is essentially to first `delete` and then `insert`.

Next, we learn how to [aggregate values over a set of data](/docs/query/aggregate-query) in a Grakn knowledge graph.