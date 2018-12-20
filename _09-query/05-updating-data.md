---
sidebarTitle: Update
pageTitle: Updating Data
summary: ""
permalink: /docs/query/updating-data
---

## Updading Data
In a Grakn Knowledge Graph, updating a data instance is essentially [deleting](/docs/query/delete-query) the current instance followed by [inserting](/docs/query/insert-query) the new instance.

## Updating Instances of Attributes
In most cases, a `thing` is expected to own only one instance of its attribute and, therefore, the value of its attribute may need to be updated. To do so, we first need to [delete the association that the thing has with the attribute of interest](/docs/query/delete-query#deleting-instances-of-attributes) and then [insert the new instance of the attribute](/docs/query/delete-query#inserting-instances-of-attribute).

Let's look at an example.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
## deleting the old
match $comp isa company id V17391 has registration-number via $r; delete $r;

## inserting the new
insert $comp isa company id V17391 has registration-number "81726354";
```
[tab:end]

[tab:Java]
```java
DeleteQuery delete_query = Graql.match(
  var("comp").isa("company").id(ConceptId.of("V17391")).has(Label.of("registration-number"), var("rn"), var("r"))
).delete("r");


InsertQuery insert_query = Graql.insert(
  var("comp").isa("company").id(ConceptId.of("V17391")).has("registration-number", "81726354")
);

delete_query.withTx(transaction).execute();
insert_query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5
transaction.execute(delete_query.toString());
transaction.execute(insert_query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```nodejs
await transaction.query("match $comp isa company id V17391 has registration-number via $r; delete $r;");
await transaction.query('insert $comp isa company id V17391 has registration-number "81726354";');
await transaction.commit();
```
[tab:end]

[tab:Python]
```cpython
transaction.query("match $comp isa company id V17391 has registration-number via $r; delete $r;")
transaction.query('insert $comp isa company id V17391 has registration-number "81726354";')
atransaction.commit()
```
[tab:end]
</div>

This first deletes the association that the `company` with id `V17391` has with attribute `registration-number` by using the `via` keyword and then continues to insert the new instance of the `registration-number` to be owned by the same `company`.


### Updating all instances of a given attribute
There may also be cases where we need to update the value of all instances that are of a certain attribute type. To do so, first, we assign the new instance of the given attribute to all things that own the old instance, and then delete the old instance.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
match $x isa thing has color "maroon"; insert $x has color "red";
match $c isa color "maroon"; delete $c;
```
[tab:end]

[tab:Java]
```java
InsertQuery insert_query = Graql.match(
  var("x").isa("thing").has("color", "maroon")
).insert(
  var("x").has("color", "red")
);

DeleteQuery delete_query = Graql.match(
  var("c").isa("color").val("maroon")
).delete("c");

insert_query.withTx(transaction).execute();
delete_query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5
transaction.execute(insert_query.toString());
transaction.execute(delete_query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```nodejs
await transaction.query("match $comp isa company id V17391 has registration-number via $r; delete $r;");
await transaction.query('insert $comp isa company id V17391 has registration-number "81726354";');
await transaction.commit();
```
[tab:end]

[tab:Python]
```cpython
transaction.query("match $comp isa company id V17391 has registration-number via $r; delete $r;")
transaction.query('insert $comp isa company id V17391 has registration-number "81726354";')
transaction.commit()
```
[tab:end]
</div>

This first looks for anything that owns the `color` attribute with the value of `"maroon"` and then inserts the new instance of the `color` attribute with the value of `"red"` to be owned by the matched owners. Finally, it deletes all instances of `color` with the value of `"maroon"`.

### Updating the roleplayers of a relationship
To change the roleplayers of a given relationship, we first need to [delete the instances of the relationship](/docs/query/delete-query# deleting-instances-of-relationship) with the current roleplayers and [insert the new instance of the relationship](/docs/query/insert-query#inserting-instances-of-relationship) with the new roleplayer.

<div class="gtabs dark" data-parse-to-html="true">

[tab:Graql]
```graql
## inserting the new
match
  $p isa person has name "Amabo";
  $org isa organisation has name "Etihw Esouh";
insert $emp (employer: $org, $employee: $p) isa employment;

## deleting the old
match
  $p isa person has name "Pmurt";
  $org isa organisation has name "Etihw Esouh";
  $emp (employer: $org, $employee: $p) isa employment;
delete $emp;
```
[tab:end]

[tab:Java]
```java
InsertQuery insert_query = Graql.match(
  var("p").isa("person").has("name", "Amabo"),
  var("org").isa("organisation").has("name", "Etihw Esouh"),
).insert(
  var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
);

DeleteQuery delete_query = Graql.match(
  var("p").isa("person").has("name", "Pmurt"),
  var("org").isa("organisation").has("name", "Etihw Esouh"),
  var("emp").isa("employment").rel("employer", var("org")).rel("employee", var("p"))
).delete("emp");

insert_query.withTx(transaction).execute();
delete_query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5
transaction.execute(insert_query.toString());
transaction.execute(delete_query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```nodejs
await transaction.query('match $p isa person has name "Amabo"; $org isa organisation has name "Etihw Esouh"; insert $emp (employer: $org, $employee: $p) isa employment;');
await transaction.query('match $p isa person has name "Pmurt"; $org isa organisation has name "Etihw Esouh"; $emp (employer: $org, $employee: $p) isa employment; delete $emp');
await transaction.commit();
```
[tab:end]

[tab:Python]
```cpython
transaction.query('match $p isa person has name "Amabo"; $org isa organisation has name "Etihw Esouh"; insert $emp (employer: $org, $employee: $p) isa employment;')
transaction.query('match $p isa person has name "Pmurt"; $org isa organisation has name "Etihw Esouh"; $emp (employer: $org, $employee: $p) isa employment; delete $emp')
transaction.commit()
```
[tab:end]
</div>

This updates the `employee` roleplayer of the `employment` relationship where the `employer` is a `company` named `"Etihw Esouh"`.

## Summary
Due to the expressivity of Graql, updating instances requires a thorough understanding of the underlying logic as explained when [defining the schema](/docs/schema/concepts). Simply put, to update is essentially to first `delete` and then `insert`.

Next, we will learn how to [aggregate values over a set of data](/docs/query/aggregate-query) in a Grakn knowledge graph.