---
title: Delete Query
keywords: graql, query, delete
tags: [graql]
summary: "Graql data from a Grakn knowledge graph."
permalink: /docs/query/delete-query
---

## Deleting Instances of Entity
To delete an instance of type entity from the knowledge graph, we use a [match clause](/docs/query/match-clause) followed by the `delete` keyword and the variable to be deleted. Let's look at a few example.

```graql
match $p isa person id V41016; delete $p;
```

The delete query above, deletes a particular `person` with id of `V41016`.

## Deleting Instances of Relationship
Similar to deleting an entity, we first `match` and then `delete`.

```graql
match
  $org isa organisation has name "Black House";
  $org-emp (employer: $org, employee: $employee) isa employment;
$delete $org-emp;
```

The delete query above, deletes all instances of `employment` where the `employer` is an `ogranisation` with `name` of `"Black House"`.

## Deleting Associations with Attributes
Attributes with the same value are shared among their owners. It's important that one understands thoroughly how [attributes are defined](/docs/schema/concepts#defining-an-attribute) in a Grakn knowledge graph
prior to performing `delete` queries on them.

To delete only the association that a thing has with an attribute, we use the `via` keyword. Let's look at an example.

```graql
match $c isa car has color "red" via $r; delete $r;
```

The delete query above, looks for a `car` that has the attribute `color` with value of `"red"` and deletes its assocaiation with that instance of `color`, while retaining the instance of attribute itself and its association with anything else that owns it. Not that if we had instead wrote the query as `match $c isa car has color $c;  $c = "red"; delete $c;`, we would have deleted the instance of color with value `"red"` and its association with anything else that might have previously owned it.

## Summary
An `insert` query preceded by a `match` clause is used to delete a data instance from the knowledge graph.

Next, we will learn how to [update data](/docs/query/updating-data) in a knowledge graph.