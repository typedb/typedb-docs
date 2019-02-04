---
sidebarTitle: Delete
pageTitle: Delete Query
permalink: /docs/query/delete-query
---

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing a `delete` query, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eager-executation-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing a `delete` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing a `delete` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
</div>

## Delete Instances of an Entity Type
To delete an instance of an entity type from the knowledge graph, we use a [match clause](/docs/query/match-clause) followed by the `delete` keyword and the variable to be deleted.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person id V41016; delete $p;
```
[tab:end]

[tab:Java]
```java
DeleteQuery query = Graql.match(
    var("p").isa("person").id("V41016")
).delete("p");
```
[tab:end]
</div>

This deletes a particular instance of the `person` type with the id of `V41016`.

## Delete Instances of a Relationship Type
To delete an instance of a relationship type, similar to deleting an entity type, we first `match` and then `delete`.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name "Pharos";
  $emp (employer: $org, employee: $p) isa employment;
$delete $emp;
```
[tab:end]

[tab:Java]
```java
DeleteQuery query = Graql.match(
  var("org").isa("organisation").has("name", "Pharos"),
  var("emp").isa("employment").rel("employer", "org").rel("employee", "p")
).delete("emp");
```
[tab:end]
</div>

This deletes all instances of the `employment` type where the `employer` is an `organisation` with `name` of `"Pharos"`.

## Delete Associations with Attributes
Attributes with the same value are shared among their owners. It's important that one understands thoroughly how [attributes are defined](/docs/schema/concepts#define-an-attribute) in a Grakn knowledge graph prior to performing `delete` queries on them.

To delete only the association that a thing has with an attribute, we use the `via` keyword to capture and delete the relationship between the owner and the owned attribute - NOT the instance of the attribute type itself, as doing so disowns the instance from any other instance that may have owned it.

<div class="tabs dark">

[tab:Graql]
```graql
match $t isa travel, has start-date 2013-12-22 via $r; delete $r;
```
[tab:end]

[tab:Java]
```java
DeleteQuery query = Graql.match(
  var("t").isa("travel").has("start-date", var("st"), var("r")),
  var("st").val(LocalDate.of(2013, 12, 22).atStartOfDay())
).delete("r");
```
[tab:end]
</div>

This looks for a `travel` that owns the attribute `start-date` with the value of `2013-12-22`, captures the association between the attribute and the owner as the variable `$r` and finally deletes `$r`. This ensures that the attribute instance of type `start-date` and value `2013-12-22` remains associated with any other instance that may own it.

If we had instead written the query as `match $t isa travel, has start-date $st;  $st == 2013-12-22"; delete $st;`, we would have deleted the instance of `start-date` with value `2013-12-22` and its association with all other concept types that previously owned it.

## Summary
The `delete` query preceded by a `match` clause is used to delete one or more data instances from the knowledge graph.

Next, we learn how to [update data](/docs/query/updating-data) in a Grakn knowledge graph.