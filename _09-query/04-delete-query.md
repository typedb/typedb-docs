---
sidebarTitle: Delete
pageTitle: Delete Query
summary: "Graql data from a Grakn knowledge graph."
permalink: /docs/query/delete-query
---

## Delete Instances of an Entity Type
To delete an instance of an entity type from the knowledge graph, we use a [match clause](/docs/query/match-clause) followed by the `delete` keyword and the variable to be deleted.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
match $p isa person id V41016; delete $p;
```
[tab:end]

[tab:Java]
```lang-java
DeleteQuery query = Graql.match(
    var("p").isa("person").id(ConceptId.of("V41016"))
).delete("p");

);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```lang-javascript
await transaction.query('match $p isa person id V41016; delete $p;');
await transaction.commit();
```
[tab:end]

[tab:Python]
```lang-python
transaction.query('match $p isa person id V41016; delete $p;')
transaction.commit()
```
[tab:end]
</div>

This deletes a particular instance of the `person` type with the id of `V41016`.

## Delete Instances of a Relationship Type
To delete an instance of a relationship type, similar to deleting an entity type, we first `match` and then `delete`.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
match
  $org isa organisation has name "Black House";
  $emp (employer: $org, employee: $p) isa employment;
$delete $emp;
```
[tab:end]

[tab:Java]
```lang-java
DeleteQuery query = Graql.match(
  var("org").isa("organisation").has("name", "Black House"),
  var("emp").isa("employment").rel("employer", "org").rel("employee", "p")
).delete("emp");

);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```lang-javascript
await transaction.query('match $org isa organisation has name "Black House"; $emp (employer: $org, employee: $p) isa employment; $delete $emp;');
await transaction.commit();
```
[tab:end]

[tab:Python]
```lang-python
transaction.query('match $org isa organisation has name "Black House"; $emp (employer: $org, employee: $p) isa employment; $delete $emp;')
transaction.commit()
```
[tab:end]
</div>

This deletes all instances of the `employment` type where the `employer` is an `ogranisation` with `name` of `"Black House"`.

## Delete Associations with Attributes
Attributes with the same value are shared among their owners. It's important that one understands thoroughly how [attributes are defined](/docs/schema/concepts#define-an-attribute) in a Grakn knowledge graph prior to performing `delete` queries on them.

To delete only the association that a thing has with an attribute, we use the `via` keyword to capture and delete the relationship between the owner and the owned attribute - NOT the instance of the attribute type itself, as doing so disowns the instance from any other instance that may have owned it.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
match $c isa car has colour "red" via $r; delete $r;
```
[tab:end]

[tab:Java]
```lang-java
DeleteQuery query = Graql.match(
  var("ca").isa("car").has(Label.of("colour"), var("co"), var("r")),
  var("co").val("red")
).delete("r");

);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```lang-javascript
await transaction.query('match $c isa car has colour "red" via $r; delete $r;');
await transaction.commit()
```
[tab:end]

[tab:Python]
```lang-python
transaction.query('match $c isa car has colour "red" via $r; delete $r;')
transaction.commit()
```
[tab:end]
</div>

This looks for a `car` that owns the attribute `colour` with the value of `"red"`, captures the association between the attribute and the owner as the variable `$r` and finally deletes `$r`. This ensures that the attribute instance of type `colour` and value `"red"` remains associated with any other instance that may own it.

If we had instead written the query as `match $c isa car has colour $c;  $c == "red"; delete $c;`, we would have deleted the instance of colour with value `"red"` and its association with all other concept types that previously owned it.

## Summary
The `delete` query preceded by a `match` clause is used to delete one or more data instances from the knowledge graph.

Next, we will learn how to [update data](/docs/query/updating-data) in a Grakn knowledge graph.