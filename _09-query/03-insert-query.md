---
title: Insert Query
keywords: graql, query, insert
tags: [graql]
summary: "Inserting data into a Grakn knowledge graph."
permalink: /docs/query/insert-query
---

## Inserting Instances of Entity
To insert an instance of an entity into the knowledge graph, we use the `insert` keyword followed by what looks a lot like what we used for [matching instances of entities](/docs/query/match-clause#matching-instances-of-an-entity). Let's look at an example.

```graql
insert $p isa person has forename "Johny", has middle-name "Jimbly", has surname "Joe";
```

In a scenario where the instance to be inserted extracts the value of its attributes from the existing data, we can use the so-called `match insert` query. Let's look at an example.

```graql
match
  $p-a isa person id V41016 has surname $s;
  insert $p-b isa person has surname $s;
```

This `match insert` query:
1. Assigns the `surname` attribute of a `person` with `id` of `V41016` to variable `s`.
2. Inserts a `person` entity with the `surname` attribute holding the value of the variable `s`.

## Inserting Instances of Attribute
Similar to inserting an instance of an entity, to insert an instance of an attribute, we use the `insert` keyword followed by the variable pattern to describe the attribute of interest and its value. Looks look at an example.

```graql
insert $x isa environment "Production";
```

**We can also choose to insert an attribute to the association of a `thing` with another attribute, which is essentially a relationship.** To do this, we use the `via` keyword. Let's look at an example.

```graql
match
  $x isa copoun has code "GraknKGMSforVisionaries" via $r;
insert $r has expiry-date 01/01/2020;
```

## Inserting Instances of Relationship
Given the dependent nature of relationships, inserting an instance of a relationship is quite different from that of an entity. The roles of a relationship to be inserted are expected to be played by instances that already exist in the knowledge graph. Therefore inserting a relationship is always preceded by matching the roleplayers - what is commonly called the `match insert`. What follows the `insert` keyword looks a lot like what we used for [matching instances of relationships](/docs/query/match-clause#matching-instances-of-an-relationship). Let's look at an example.

```graql
match
  $company isa company has name "Grakn Cloud";
  $person isa person has name "Hamzaa Shahza";
insert $new-employment (employer: $company, employee: $person) isa employment;
  $new-employment key reference-id "WGFTSH";
```

This `match insert` query:
1. Assigns the `employer`'s roleplayer to the `company` variable.
2. Assigns the `employee`s roleplayer to the `person` variable.
3. Inserts an `employment` relationship with `company` and `person` as its roleplayers and assigns it to the `new-employment` variable.
4. Inserts `WGFTSH` to attribute `reference-id` as the key to the `new-employment` instance.

## Summary
An `insert` query optionally preceded by a `match` clause is used to insert a data instance into the knowledge graph.

Next, we will learn how to [delete data](/docs/query/delete-query) from a knowledge graph.