---
sidebarTitle: Insert
pageTitle: Insert Query
permalink: /docs/query/insert-query
---

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing a `insert` query, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eager-executation-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing a `insert` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing a `insert` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
</div>

## Insert Instances of an Entity Type
To insert an instance of an entity type into the knowledge graph, we use the `insert` keyword followed by what looks a lot like what we used for [matching instances of entities](/docs/query/match-clause#match-instances-of-an-entity).

<div class="tabs dark">

[tab:Graql]
```graql
insert $p isa person, has full-name "John Parkson", has nickname "Johny", has gender "male", has email "john.parkson@gmail.com", has phone-number "+44-1234=567890";
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.insert(
  var("p").isa("person").has("full-name", "John Parkson").has("nickname", "Johny").has("email", "john.parkson@gmail.com")
  .has("phone-number", "+44-1234-567890")
);
```
[tab:end]
</div>

<!-- In a scenario where the instance to be inserted owns an attribute whose value must be extracted from the existing data, we use the so-called `match insert` query.

<div class="tabs dark">

[tab:Graql]
```graql
match
  $p-a id V41016, has surname $s;
  insert $p-b isa person, has surname $s;
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.match(
  var("p-a").id("V41016").has("surname", var("s"))
).insert(
  var("p-b").isa("person").has("surname", var("s"))
);
```
1.5 transaction.execute(query.toString());
transaction.commit();
[tab:end]
</div> -->

This `match insert` query:
1. Assigns the `surname` attribute of a `person` with `id` of `V41016` to variable `$s`.
2. Inserts a `person` entity with the `surname` attribute holding the value of the variable `$s`.

## Insert Instances of an Attribute Type
Similar to inserting an instance of an entity, to insert an instance of an attribute, we use the `insert` keyword followed by the variable pattern to describe the attribute of interest and its value.

<div class="tabs dark">

[tab:Graql]
```graql
insert $x isa emotion; $x == "like";
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.insert(
  var("x").isa("emotion").val("like")
);
```
[tab:end]
</div>

## Insert Instances of a Relationship Type
Given the dependent nature of relationships, inserting an instance of a relationship is quite different from that of an entity. The roles of a relationship to be inserted are expected to be played by instances that already exist in the knowledge graph. Therefore inserting a relationship is always preceded by matching the roleplayers - what is commonly called the `match insert`. What follows the `insert` keyword looks a lot like what we used for [matching instances of relationships](/docs/query/match-clause#match-instances-of-a-relationship).

<div class="tabs dark">

[tab:Graql]
```graql
match
  $org isa organisation, has name "Facelook";
  $person id V8272;
insert $new-employment (employer: $org, employee: $person) isa employment;
  $new-employment key reference-id "WGFTSH";
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.match(
  var("org").isa("organisation").has("name", "Facelook"),
  var("p").isa("person").id("V8272")
).insert(
  var("emp").isa("employment").rel("employer", "org").rel("employee", "p").has("reference-id", "WGFTSH")
);
```
[tab:end]
</div>

This `match insert` query:
1. Matches the `organisation` that plays `employer`, assigned to variable `$c`.
2. Matches the `person` that plays `employee`, assigned to variable `$p`.
3. Inserts an `employment` relationship with `$c` and `$p` as its roleplayers, assigned to variable `$emp`.
4. Inserts the ownership of `reference-id` with value `WGFTSH` by to the `$emp` relationship instance.

## Summary
An `insert` query optionally preceded by a `match` clause is used to insert a data instance into the knowledge graph.

Next, we learn how to [delete data](/docs/query/delete-query) from a knowledge graph.