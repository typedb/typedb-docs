---
pageTitle: Match Clause
keywords: graql, query, match, pattern, statement, variable
longTailKeywords: graql match, graql match get, graql patterns, graql statements, graql variables
Summary: Targeting instances of data that match expressive patterns in Grakn.
---

## Match Clause
We use match clauses to retrieve data instances and schema types that follow a particular pattern. Using match clauses forms the basis of our data retrieval.
By defining the [schema](../09-schema/00-overview.md), we effectively define a vocabulary to be used to describe concepts of our domain.

Once the schema is defined, we can form graph patterns for which we want to search within our knowledge graph. We do that by using match clauses.
Each match clause represents a particular graph pattern via its corresponding query pattern. The match clause is then executed as a part of a [Get](../11-query/02-get-query.md), [Insert](../11-query/03-insert-query.md), [Delete](/docs/schema/delete-query) or [Aggregate](/docs/schema/aggregate-query) query. In the case of a Get query, what we expect to be returned is the tuples of instances fulfilling the specified pattern.

In the subsequent sections, we shall see how to match specific graph patterns. To try the following examples with one of the Grakn clients, follows these [Clients Guide](#clients-guide).

## Match Instances of Concept Types
What follows in this section, describes how we can use the `match` keyword to find instances of data that we are interested in. What we choose to do with the matched result, is out of the scope of this section. But for the sake of completeness, we end each `match` clause with `get;`. In the next section, we learn about [using _get_ for the retrieval of information from the knowledge graph](../11-query/02-get-query.md).

### Match instances of an entity
Matching instances of an entity type is easy. We do so by using a variable followed by the `isa` keyword and the label of the entity type.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("p").isa("person")
).get("p");
```
[tab:end]
</div>

The example above, for every person, assigns the person (entity) instance to the variable `$p`.

#### Instances of an entity with particular attributes
To only match the instances of entities that own a specific attribute, we use the `has` keyword, followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $n; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("p").isa("person").has("full-name", var("n"))
).get("p");
```
[tab:end]
</div>


We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

### Match instances of a relation
Because of the [dependent nature of relations](../09-schema/01-concepts.md#define-a-relation), matching them is slightly different to matching entities and attributes.

<div class="tabs dark">

[tab:Graql]
```graql
match $emp (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("emp").rel("employer", "x").rel("employee", "y").isa("employment")
).get("emp");
```
[tab:end]
</div>

The example above, for every employment, assigns the instance of the employment (relation) type to the variable `$emp`, the instance of the employer organisation (entity) type to the variable `$x` and the instance of the employee person (entity) type to the variable `$y`.

#### Instances of a relation with particular attributes
To only match the instances of relations that own a specific attribute, we use the `has` keyword followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $emp (employer: $x, employee: $y) isa employment, has reference-id $ref; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("emp").rel("employer", "x").rel("employee", "y").has("reference-id", var("ref")).isa("employment")
).get("emp");
```
[tab:end]
</div>

We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

#### Leave the relation instance unassigned
Assigning a relation to a variable is optional. We may only be interested in the role players of a certain relation. In such a case, we would write the above match clause like so:

<div class="tabs dark">

[tab:Graql]
```graql
match (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```java
// FIXME(vmax): anonymous variables are not allowed 
//GraqlMatch.Filtered query = Graql.match(
//  var().isa("employment").rel("employer", "x").rel("employee", "y")
//).get();
```
[tab:end]
</div>

#### Leave the roles out
We can always choose to not include the label of roles when matching a relation. This, especially, makes sense when matching a relation that relates to only one role.

<div class="tabs dark">

[tab:Graql]
```graql
match $fr ($x, $y) isa friendship; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("fr").rel("x").rel("y").isa("friendship")
).get("fr");
```
[tab:end]
</div>

### Match instances of an attribute
We can match instances of attribute types in various ways depending on our use case.

#### Independent of label
We can match instances of attributes type based on their value regardless of their label.

<div class="tabs dark">

[tab:Graql]
```graql
match $x "like"; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("x").eq("like")
).get("x");
```
[tab:end]
</div>

This matches instances of any attribute type whose value is `"like"` and assigns each to variable `$x`.

#### Independent of owner
We can match instances of attributes based on their value regardless of what concept type they belong to.

<div class="tabs dark">

[tab:Graql]
```graql
match $n isa nickname; $n "Mitzi"; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("x").eq("Mitzi").isa("nickname")
).get("x");
```
[tab:end]
</div>

This matches instances of the attribute with the label of `nickname` and value of `"Mitzi"`, regardless of what owns the attribute `nickname`.

#### With a given subset
To match all instances of attribute types that contain a substring, we use the `contains` keyword.

<div class="tabs dark">

[tab:Graql]
```graql
match $phone-number contains "+44"; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("phone-number").contains("+44")
).get("phone-number");
```
[tab:end]
</div>

This matches instances of any attribute type whose value contains the substring `"+44"`.

#### With a given regex
The value of an attribute can also be matched using a regex. We allow the range of [Java Regex Patterns](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html).

<div class="tabs dark">

[tab:Graql]
```graql
match $x like "(Miriam Morton|Solomon Tran)"; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("phone-number").regex("(Miriam Morton|Solomon Tran)")
).get("phone-number");
```
[tab:end]
</div>

This matches the instances of any attribute type whose value matches the given regex - `"Miriam Morton"` or `"Solomon Tran"`.

#### Owners with multiple attributes
To match instances of a concept type that owns multiple attributes, we can simply chain triples of `has`, label and variable. Separating each triple with a comma is optional.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has nickname $nn, has full-name $fn; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("p").isa("person").has("nickname", var("nn")).has("full-name", var("fn"))
).get("p");
```
[tab:end]
</div>

#### Owners with attributes of given values
We can also match instances that own an attribute with a specific value or range of values.

<div class="tabs dark">

[tab:Graql]
```graql
match $s isa school, has ranking < 100; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("s").isa("school").has("ranking", Graql.lt(100))
).get("s");
```
[tab:end]
</div>

But if in this example, we still want to know the ranking of each matched school? we split the variable assignment and the condition like so.

<div class="tabs dark">

[tab:Graql]
```graql
match $s isa school, has ranking $r; $r < 100; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("s").isa("school").has("ranking", var("r")),
  var("r").lt(100)
).get("s");
```
[tab:end]
</div>

### Disjunction of patterns
By default, a collection of patterns in a `match` clause constructs conjunction of patterns. To include patterns in the form of a disjunction, we need to wrap each pattern in `{}` and place the `or` keyword in between them.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $fn; { $fn contains "Miriam"; } or { $fn contains "Solomon"; }; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("p").isa("person").has("full-name", var("fn")),
  or(
    var("fn").contains("Miriam"),
    var("fn").contains("Solomon")
  )
).get("p");
```
[tab:end]
</div>

### Instances of a direct type
The type that an instance belongs to may be a subtype of another. This means when we use `isa`, we are matching all direct and indirect instances of the given type. To only match the direct instances, we use `isa!` instead. Given the [previous organisation example](../09-schema/01-concepts.md#subtype-an-entity), if we were to only match the direct instances of `organisation`, we would write the match clause like so.

<div class="tabs dark">

[tab:Graql]
```graql
match $rr isa! romantic-relationship; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("rr").isa("romantic-relationship")
).get("rr");
```
[tab:end]
</div>

This query matches only the direct instances of `romantic-relationship`. That means the instances of `open-relation`, `domestic-relation` and `complicated-relation` (which all subtype `romantic-relationship`) would not be included.

### One particular instance
Grakn assigns an auto-generated id to each instance. Although this id is generated by Grakn solely for internal use, it is indeed possible to find an instance with its Grakn id.
To do so, we use the `id` keyword followed by the `id` assigned to the instance by Grakn.

<div class="tabs dark">

[tab:Graql]
<!-- test-ignore -->
```graql
match $x id V41016; get;
```
[tab:end]

[tab:Java]
<!-- test-ignore -->
```java
GraqlMatch.Filtered query = Graql.match(
  var("x").id("V41016")
).get("x");
```
[tab:end]
</div>

### Comparators
When matching an instance of an attribute type based on its value or simply comparing two variables, the following comparators may be used: `==`, `!=`, `>`, `>=`, `<` and `<=`.

## Match Schema Concepts
In this section, we learn how we can use the `match` keyword to find patterns in the schema of a Grakn knowledge graph. Matching concepts of a schema is always preceded by `get;`. In the next section, we learn about [how to use the get keyword](../11-query/02-get-query.md).

Having fully understood the [schema concepts](../09-schema/01-concepts.md) and how they are defined, you can think of the following `match` examples as fill-in-the-blank questions, where the-blank is a Graql variable and the sentences are different parts of the schema statements.

### Direct and indirect subtypes of a given type
To match all schema concepts of a given type, **all the way down the type hierarchy**, we use the `sub` keyword.

<div class="tabs dark">
[tab:Graql]
```graql
match $x sub post; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query_a = Graql.match(
  var("x").sub("post")
).get("x");
```
[tab:end]
</div>

Running the above query on the `social_network` knowledge graph, returns the `post` concept type itself, as well as all concept types that are subtypes of `post`, directly (i.e. `media`, `comment`, `album` and `status-update`) and indirectly (i.e. `photo` and `video`).

### Direct subtypes of a given type
To match the schema concepts of a given type, **all the way down its type hierarchy**, we use the `sub!` keyword.

<div class="tabs dark">
[tab:Graql]
```graql
match $x sub! post; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query_a = Graql.match(
  var("x").subX("post")
).get("x");
```
[tab:end]
</div>

Running the above query on the `social_network` knowledge graph, returns the `post` concept type itself, as well as the concept types that subtype `post` directly (i.e. `media`, `comment`, `album` and `status-update`) or through any of its subtypes (i.e. `photo` and `video`).

### A given type
To match only the given type and not any of its subtypes, we use the `type` keyword.

<div class="tabs dark">
[tab:Graql]
```graql
match $x type post; get $x;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query_a = Graql.match(
  var("x").type("post")
).get("x");
```
[tab:end]
</div>

Running the above query, returns only the concept type that has the label `post`.


### Roles of a given relation
Given a particular relation, we can use the `relates` keyword to match all roles related to the given relation type.

<div class="tabs dark">

[tab:Graql]
```graql
match employment relates $x; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  type("employment").relates(var("x"))
).get("x");
```
[tab:end]
</div>

This matches all roles of the `employment` relation - `employer` and `employee`.

#### Subroles of a given role in a super-relation
When we learned about [subtyping relations](../09-schema/01-concepts.md#subtype-a-relation), we saw that a role related to a sub-relation is linked to a corresponding parent's role using the `as` keyword. We can use the same keyword in a `match` clause to match the corresponding role in the given sub-relation.

<div class="tabs dark">

[tab:Graql]
```graql
match location-of-office relates $x as located-subject; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  type("location-of-office").relates(var("x")),
  var("x").sub("located-subject")
).get("x");
```
[tab:end]
</div>

This matches all the roles that correspond to the `located-subject` role of the relation which `location-of-office` subtypes. In this case, the super-relation being `location-of-everything` and the matched role being `located-subject`.

### Role players of a given role
Given a role, we can match the concept types that play the given role by using the `plays` keyword.

<div class="tabs dark">

[tab:Graql]
```graql
match $x plays employee; get;
```
[tab:end]

[tab:Java]
```java
// FIXME(vmax): fill in needed relation
GraqlMatch.Filtered query = Graql.match(
  var("x").plays("FIXME", "employee")
).get("x");
```
[tab:end]
</div>

This matches all concept types that play the role `employee` in any relation.

### Owners of a given attribute
Given an attribute type, we can match the concept types that own the given attribute type by using the `has` keyword.

<div class="tabs dark">

[tab:Graql]
```graql
match $x has title; get;
```
[tab:end]

[tab:Java]
```java
GraqlMatch.Filtered query = Graql.match(
  var("x").has("title", var())
).get("x");
```
[tab:end]
</div>

This matches all concept types that own `title` as their attribute.

## Examples
To see some `get` queries powered by complex and expressive `match` clauses, check out the [examples of querying a sample knowledge graph](/docs/examples/queries).

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a query that contains a `match` clause, is as simple as calling the [`execute()`](../03-client-api/01-java.md#eagerly-execute-a-graql-query) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a query that contains a `match` clause, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a query that contains a `match` clause, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
We learned how to use the `match` clause to write intuitive statements that describe a desired pattern in the knowledge graph and fill in the variables that hold the data we would like to acquire.

Next, we learn how to use the `match` clause in conjunction with Graql queries to carry out instructions - starting with the [get query](../11-query/02-get-query.md).
