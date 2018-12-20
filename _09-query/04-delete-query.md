---
sidebarTitle: Delete
pageTitle: Delete Query
summary: "Graql data from a Grakn knowledge graph."
permalink: /docs/query/delete-query
---

## Deleting Instances of Entity
To delete an instance of type entity from the knowledge graph, we use a [match clause](/docs/query/match-clause) followed by the `delete` keyword and the variable to be deleted.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
match $p isa person id V41016; delete $p;
```
[tab:end]

[tab:Java]
```java
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
```nodejs
await transaction.query('match $p isa person id V41016; delete $p;');
await transaction.commit();
```
[tab:end]

[tab:Python]
```cpython
transaction.query('match $p isa person id V41016; delete $p;')
transaction.commit()
```
[tab:end]
</div>

This deletes a particular `person` with the id of `V41016`.

## Deleting Instances of Relationship
To delete an instance of a relationship, similar to deleting an entity, we first `match` and then `delete`.

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
```java
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
```nodejs
await transaction.query('match $org isa organisation has name "Black House"; $emp (employer: $org, employee: $p) isa employment; $delete $emp;');
await transaction.commit();
```
[tab:end]

[tab:Python]
```cpython
transaction.query('match $org isa organisation has name "Black House"; $emp (employer: $org, employee: $p) isa employment; $delete $emp;')
transaction.commit()
```
[tab:end]
</div>

This deletes all instances of `employment` where the `employer` is an `ogranisation` with `name` of `"Black House"`.

## Deleting Associations with Attributes
Attributes with the same value are shared among their owners. It's important that one understands thoroughly how [attributes are defined](/docs/schema/concepts#defining-an-attribute) in a Grakn knowledge graph prior to performing `delete` queries on them.

To delete only the association that a thing has with an attribute, we use the `via` keyword to capture the relationship between the owner and the owned attribute.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
match $c isa car has color "red" via $r; delete $r;
```
[tab:end]

[tab:Java]
```java
DeleteQuery query = Graql.match(
  var("ca").isa("car").has(Label.of("color"), var("co"), var("r")),
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
```nodejs
await transaction.query('match $c isa car has color "red" via $r; delete $r;');
await transaction.commit()
```
[tab:end]

[tab:Python]
```cpython
transaction.query('match $c isa car has color "red" via $r; delete $r;')
transaction.commit()
```
[tab:end]
</div>

This looks for a `car` that has the attribute `color` with the value of `"red"` and deletes its association with that instance of `color`, while retaining the instance of the attribute itself and its association with anything else that owns it. Not that if we had instead written the query as `match $c isa car has color $c;  $c == "red"; delete $c;`, we would have deleted the instance of colour with value `"red"` and its association with anything else that might have previously owned it.

## Summary
The `delete` query preceded by a `match` clause is used to delete one or more data instances from the knowledge graph.

Next, we will learn how to [update data](/docs/query/updating-data) in a Grakn knowledge graph.