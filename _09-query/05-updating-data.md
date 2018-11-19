---
title: Updating Data
keywords: graql, query, update
tags: [graql]
summary: ""
permalink: /docs/query/updating-data
---

## Updading Data
In a Grakn Knowledge Graph, updating a data instance is essentially [deleting](/docs/query/delete-query) the current instance followed by [inserting](/docs/query/insert-query) the new instance.

## Updating Instances of Attributes
In most cases, a `thing` is expected to own only one instance of its attribute and, therefore, the value of its attribute may need to be updated. To do so, we first need to [delete the association that the thing has with the attribute of interest](/docs/query/delete-query#deleting-instances-of-attributes) and then [insert the new instance of the attribute](/docs/query/delete-query#inserting-instances-of-attribute).

Let's look at an example.

```graql
## deleting the old
match $comp isa company id V17391 has registration-number via $r; delete $r;

## inserting the new
Insert $comp isa company id V17391 has registration-number "81726354";
```
In the above example, we first delete the association that the `company` with id `V17391` has with attribute `registration-number` by using the `via` keyword and then continue to assign the new instance of the `registration-number` to the same `company`.


### Updating all instances of a given attribute
There may also be cases when we need to update the value of all instances that are of a certain attribute type. To do so, first, we assign the new instance of the given attribute to all things that own the old instance, and then delete the old instance.
Let's look at an example.

```graql
match
  $x isa thing has color "maroon";
insert $x has color "red";
delete $c isa color "maroon";
```

In the example above, we first look for anything that as `colour` with value `maroon` and then assign it the new `colour` with value `red`. Finally, we delete all instances of `colour` with value `maroon`.

### Updating the roleplayers of a relationship
To change the roleplayer of a given relationship, we first need to [delete the instance of the relationship](/docs/query/delete-query# deleting-instances-of-relationship) with the current roleplayers and [insert the new instance of the relationship](/docs/query/insert-query#inserting-instances-of-relationship) again with the correct new roleplayer. Let's look at an example.

```graql
## deleting the old
match
  $p isa person has name "Pmurt";
  $org isa organisation has name "Etihw Esouh";
  $emp (employer: $org, $employee: $p) isa employment;
delete $emp;

## inserting the new
match
  $p isa person has name "Amabo";
  $org isa organisation has name "Etihw Esouh";
insert $emp (employer: $org, $employee: $p) isa employment;
```

In the example above, we are updating an instance of an `employment` to have a different roleplayer as its `employee`.

## Summary
Due to the expressivity of Graql, updating instances requires a thorough understanding of the underlying logic as explained wh [defining the schema](/docs/schema/concepts). Simply put, to update is essentially to first `delete` and then `insert.

Next, we will learn how to [aggregate values over a set of data](/docs/query/aggregate-query) in a Grakn knowledge graph.