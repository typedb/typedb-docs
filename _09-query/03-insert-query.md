---
title: Insert Query
keywords: graql, query, insert
tags: [graql]
summary: "Inserting data into a Grakn knowledge graph."
permalink: /docs/query/insert-query
---

## Inserting Instances of Entity
To insert an instance of an entity into the knowledge graph, we use the `insert` keyword followed by what looks a lot like what we used for [matching instances of entities](/docs/query/match-clause#matching-instances-of-an-entity).

<div class="tabs">

[tab:Graql]
```graql
insert $p isa person has forename "Johny", has middle-name "Jimbly", has surname "Joe";
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.insert(
  var("p").isa("person").has("forename", "Johny").has("middle-name", "Jimbly").has("surname", "Joe")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```javascript
await transaction.query('insert $p isa person has forename "Johny", has middle-name "Jimbly", has surname "Joe";');
await transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query('insert $p isa person has forename "Johny", has middle-name "Jimbly", has surname "Joe";')
transaction.commit()
```
[tab:end]

</div>

In a scenario where the instance to be inserted extracts the value of its attributes from the existing data, we use the so-called `match insert` query.

<div class="tabs">

[tab:Graql]
```graql
match
  $p-a isa person id V41016 has surname $s;
  insert $p-b isa person has surname $s;
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.match(
  var("p-a").isa("person").id(ConceptId.of("V41016")).has("surname", var("s"))
).insert(
  var("p-b").isa("person").has("surname", var("s"))
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```javascript
await transaction.query('match $p-a isa person id V41016 has surname $s; insert $p-b isa person has surname $s;');
await transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query('match $p-a isa person id V41016 has surname $s; insert $p-b isa person has surname $s;')
transaction.commit()
```
[tab:end]
</div>

This `match insert` query:
1. Assigns the `surname` attribute of a `person` with `id` of `V41016` to variable `s`.
2. Inserts a `person` entity with the `surname` attribute holding the value of the variable `s`.

## Inserting Instances of Attribute
Similar to inserting an instance of an entity, to insert an instance of an attribute, we use the `insert` keyword followed by the variable pattern to describe the attribute of interest and its value.

<div class="tabs">

[tab:Graql]
```graql
insert $x isa environment "Production";
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.insert(
  var("x").isa("environment").val("Production")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString());
transaction.commit(); -->
[tab:end]

[tab:Javascript]
```javascript
await transaction.query('insert $x isa environment "Production";');
await transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query('insert $x isa environment "Production";')
transaction.commit()
```
[tab:end]
</div>

## Inserting Instances of Relationship
Given the dependent nature of relationships, inserting an instance of a relationship is quite different from that of an entity. The roles of a relationship to be inserted are expected to be played by instances that already exist in the knowledge graph. Therefore inserting a relationship is always preceded by matching the roleplayers - what is commonly called the `match insert`. What follows the `insert` keyword looks a lot like what we used for [matching instances of relationships](/docs/query/match-clause#matching-instances-of-an-relationship).

<div class="tabs">

[tab:Graql]
```graql
match
  $company isa company has name "Grakn Cloud";
  $person isa person id V8272;
insert $new-employment (employer: $company, employee: $person) isa employment;
  $new-employment key reference-id "WGFTSH";
```
[tab:end]

[tab:Java]
```java
InsertQuery query = Graql.match(
  var("c").isa("company").has("name", "Grakn Cloud"),
  var("p").isa("person").id(ConceptId.of("V8272"))
).insert(
  var("emp").isa("employment").rel("employer", "c").rel("employee", "p").has("reference-id", "WGFTSH"),
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query('match $company isa company has name "Grakn Cloud"; $person isa person id V8272; insert $new-employment (employer: $company, employee: $person) isa employment; $new-employment key reference-id "WGFTSH";');
await transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query('match $company isa company has name "Grakn Cloud"; $person isa person id V8272; insert $new-employment (employer: $company, employee: $person) isa employment; $new-employment key reference-id "WGFTSH";')
transaction.commit()
```
[tab:end]
</div>

This `match insert` query:
1. Matches the `company` that will play `employer`, assigned to variable `c`.
2. Matches the `person` that will play `employee`, assigned to variable `p`.
3. Inserts an `employment` relationship with `c` and `p` as its roleplayers, assigned to variable `emp`.
4. Inserts the ownership of `reference-id` with value `WGFTSH` by to the `emp` relationship instance.

## Summary
An `insert` query optionally preceded by a `match` clause is used to insert a data instance into the knowledge graph.

Next, we will learn how to [delete data](/docs/query/delete-query) from a knowledge graph.