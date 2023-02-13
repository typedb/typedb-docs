---
pageTitle: Match Clause
keywords: typeql, query, match, pattern, statement, variable
longTailKeywords: typeql match, typeql match get, typeql patterns, typeql statements, typeql variables
Summary: Targeting instances of data that match expressive patterns in TypeDB.
---

# Match and Patterns

We use match clauses to retrieve data instances and schema types that follow a particular pattern. Using match 
clauses forms the basis of our data retrieval or data modification. By defining the [schema](05-schema.md), we 
effectively define a vocabulary to be used to describe concepts of our domain.

Once the schema is defined, we can form patterns for which we want to search within our data. We do 
that by using match clauses. Each match clause represents a particular pattern via its corresponding query 
pattern. The match clause is then executed as a part of other types of queries:

- [Get](../../11-query/02-get-query.md)
- [Insert](../../11-query/03-insert-query.md) 
- [Delete](../../11-query/04-delete-query.md) 
- [Aggregate](../../11-query/06-aggregate-query.md) 

In the case of a Get query, what we expect to be returned is the tuples of instances fulfilling the specified pattern.

## Schema and Data

We can send queries to read or write schema or data. So the match clause can be used with both data and schema concepts.

## Match Schema Concepts

We can use the `match` keyword to find types in the schema of a TypeDB database. 

### Match everything

We can request everything from a schema. To do that we would use `Thing` concept. As every schema concept is a 
subtype of `Thing` we can do it like that: 

```typeql
match $s sub thing; get $s;
```

<div class="note">
[Important]
Be default, if we send `match` query without stating what we want to do with matched pattern (without the get 
statement in the example above) it is processed as `match ... get`, so it returns all mentioned variables.
</div>

### Direct and indirect subtypes of a given type

To match all schema concepts of a given type, **all the way down the type hierarchy**, we use the `sub` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $o sub object; get $o;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query_a = TypeQL.match(
  var("o").sub("object")
).get("o");
```
[tab:end]
</div>

Running the above query on the `iam` [schema](../01-start/03-quickstart.md#fourth-step--prepare-a-schema), returns the `post` 
concept type itself, as well as all concept types that are subtypes of `post`, directly (i.e. `media`, `comment`, `album` and `status-update`) and indirectly (i.e. `photo` and `video`).

### Direct subtypes of a given type
To match the schema concepts that are **direct subtypes** of a given type, we use the `sub!` keyword.

<div class="tabs dark">
[tab:TypeQL]
```typeql
match $x sub! post; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query_a = TypeQL.match(
  var("x").subX("post")
).get("x");
```
[tab:end]
</div>

Running the above query on the `social_network` [knowledge graph](../08-examples/01-phone-calls-schema.md), returns direct subtypes of the `post` type itself (i.e. `media`, `comment`, `album` and `status-update`).

### A given type
To match only the given type and not any of its subtypes, we use the `type` keyword.

<div class="tabs dark">
[tab:TypeQL]
```typeql
match $x type post; get $x;
```
[tab:end]

[tab:Java]
<!-- test-delay -->
```java
TypeQLMatch.Filtered query_a = TypeQL.match(
  var("x").type("post")
).get("x");
```
[tab:end]
</div>

Running the above query, returns only the concept type that has the label `post`.


### Roles of a given relation
Given a particular relation, we can use the `relates` keyword to match all roles related to the given relation type.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match employment relates $x; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  type("employment").relates(var("x"))
).get("x");
```
[tab:end]
</div>

This matches all roles of the `employment` relation - `employer` and `employee`.

#### Subroles of a given role in a super-relation
When we learned about [subtyping relations](../09-schema/01-concepts.md#subtype-a-relation), we saw that a role related to a sub-relation is linked to a corresponding parent's role using the `as` keyword. We can use the same keyword in a `match` clause to match the corresponding role in the given sub-relation.

<div class="tabs dark">

[tab:TypeQL]
<!-- test-delay -->
```typeql
match friend-request relates $x as located; get $x;
```
[tab:end]

[tab:Java]
<!-- test-delay -->
```java
TypeQLMatch.Filtered query = TypeQL.match(
  type("friend-request").relates(var("x"), "subject")
).get("x");
```
[tab:end]
</div>

This matches all the roles that correspond to the `subject` role of the relation which `friend-request` subtypes. In this case, the super-relation being `request` and the matched role being `friendship`.

### Role players of a given role
Given a role, we can match the concept types that play the given role by using the `plays` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x plays employment:employee; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("x").plays("employment", "employee")
).get("x");
```
[tab:end]
</div>

This matches all concept types that play the role `employee` in any relation.

### Owners of a given attribute
Given an attribute type, we can match the concept types that own the given attribute type by using the `owns` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x owns title; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("x").owns("title")
).get("x");
```
[tab:end]
</div>

This matches all concept types that own `title` as their attribute.

## Match Data

We can use the `match` keyword to find instances of types or data in a TypeDB database.

### Match everything

We can request every instance of data from a database. To do that we would use `Thing` concept. As every schema concept 
is a subtype of `Thing` we can do it like that:

```typeql
match $t isa thing; get $t;
```

### Match instances of an entity
Matching instances of an entity type is easy. We do so by using a variable followed by the `isa` keyword and the label of the entity type.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person; get $p;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("p").isa("person")
).get("p");
```
[tab:end]
</div>

The example above, for every person, assigns the person (entity) instance to the variable `$p`.

#### Instances of an entity with particular attributes
To only match the instances of entities that own a specific attribute, we use the `has` keyword, followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has full-name $n; get $p;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("p").isa("person").has("full-name", var("n"))
).get("p");
```
[tab:end]
</div>


We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

### Match instances of a relation
Because of the [dependent nature of relations](../09-schema/01-concepts.md#define-a-relation), matching them is slightly different to matching entities and attributes.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $emp (employer: $x, employee: $y) isa employment; get $emp;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("emp").rel("employer", "x").rel("employee", "y").isa("employment")
).get("emp");
```
[tab:end]
</div>

The example above, for every employment, assigns the instance of the employment (relation) type to the variable `$emp`, the instance of the employer organisation (entity) type to the variable `$x` and the instance of the employee person (entity) type to the variable `$y`.

#### Instances of a relation with particular attributes
To only match the instances of relations that own a specific attribute, we use the `has` keyword followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $emp (employer: $x, employee: $y) isa employment, has reference-id $ref; get $emp;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("emp").rel("employer", "x").rel("employee", "y").has("reference-id", var("ref")).isa("employment")
).get("emp");
```
[tab:end]
</div>

We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

#### Leave the relation instance unassigned
Assigning a relation to a variable is optional. We may only be interested in the role players of a certain relation. In such a case, we would write the above match clause like so:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match (employer: $x, employee: $y) isa employment;
```
[tab:end]

[tab:Java]
```java
// FIXME(vmax): anonymous variables are not allowed 
//TypeQL.Filtered query = TypeQL.match(
//  var().isa("employment").rel("employer", "x").rel("employee", "y")
//).get();
```
[tab:end]
</div>

#### Leave the roles out
We can always choose to not include the label of roles when matching a relation. This, especially, makes sense when matching a relation that relates to only one role.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $fr ($x, $y) isa friendship; get $fr;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("fr").rel("x").rel("y").isa("friendship")
).get("fr");
```
[tab:end]
</div>

### Match instances of an attribute
We can match instances of attribute types in various ways depending on our use case.

#### Independent of label
We can match instances of attribute types based on their value regardless of their label.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x "law"; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("x").eq("law")
).get("x");
```
[tab:end]
</div>

This matches instances of any attribute type whose value is `"law"` (for instance, a profession and a university course) 
and assigns each to variable `$x`.

#### Independent of owner
We can match instances of attributes based on their value regardless of what concept type they belong to.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $n isa nickname; $n "Mitzi"; get $n;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("x").eq("Mitzi").isa("nickname")
).get("x");
```
[tab:end]
</div>

This matches instances of the attribute with the label of `nickname` and value of `"Mitzi"`, regardless of what owns the attribute `nickname`.

#### With a given subset
To match all instances of attribute types that contain a substring, we use the `contains` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $phone-number contains "+44"; get $phone-number;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("phone-number").contains("+44")
).get("phone-number");
```
[tab:end]
</div>

This matches instances of any attribute type whose value contains the substring `"+44"`.

#### With a given regex
The value of an attribute can also be matched using a regex. We allow the range of [Java Regex Patterns](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html).

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x like "(Miriam Morton|Solomon Tran)"; get $x;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("phone-number").regex("(Miriam Morton|Solomon Tran)")
).get("phone-number");
```
[tab:end]
</div>

This matches the instances of any attribute type whose value matches the given regex - `"Miriam Morton"` or `"Solomon Tran"`.

#### Owners with multiple attributes
To match instances of a concept type that owns multiple attributes, we can simply chain triples of `has`, label and variable.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has nickname $nn, has full-name $fn; get $p;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("p").isa("person").has("nickname", var("nn")).has("full-name", var("fn"))
).get("p");
```
[tab:end]
</div>

#### Owners with attributes of given values
We can also match instances that own an attribute with a specific value or range of values.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $s isa school, has ranking < 100; get $s;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("s").isa("school").has("ranking", TypeQL.lt(100))
).get("s");
```
[tab:end]
</div>

But if in this example, we still want to know the ranking of each matched school, we split the variable assignment and the condition like so.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $s isa school, has ranking $r; $r < 100; get $s;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("s").isa("school").has("ranking", var("r")),
  var("r").lt(100)
).get("s");
```
[tab:end]
</div>

### Disjunction of patterns
By default, a collection of patterns in a `match` clause constructs conjunction of patterns. To include patterns in the form of a disjunction, we need to wrap each pattern in `{}` and place the `or` keyword in between them.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has full-name $fn; { $fn contains "Miriam"; } or { $fn contains "Solomon"; }; get $p;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
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
The type that an instance belongs to may be a subtype of another. This means when we use `isa`, we are matching all direct and indirect instances of the given type. To only match the direct instances, we use `isa!` instead. 

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $rr isa! romantic-relationship; get $rr;
```
[tab:end]

[tab:Java]
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("rr").isa("romantic-relationship")
).get("rr");
```
[tab:end]
</div>

This query matches only the direct instances of `romantic-relationship`. That means the instances of `open-relation`, `domestic-relation` and `complicated-relation` (which all subtype `romantic-relationship`) would not be included.

### One particular instance
TypeDB assigns an auto-generated id to each instance. Although this id is generated by TypeDB solely for internal use, it is indeed possible to find an instance with its TypeDB id.
To do so, we use the `iid` keyword followed by the `iid` assigned to the instance by TypeDB.

<div class="tabs dark">
[tab:TypeQL]
<!-- test-ignore -->
```typeql
match $x iid 0x966e80018000000000000000; get $x;
```
[tab:end]

[tab:Java]
<!-- test-ignore -->
```java
TypeQLMatch.Filtered query = TypeQL.match(
  var("x").iid("0x966e80018000000000000000")
).get("x");
```
[tab:end]
</div>

### Concept Equality

TypeQL allows exact concept equality using the `is` keyword. This is commonly combined with negation to check two 
concepts are not equal:

<div class="tabs dark">
[tab:TypeQL]
<!-- test-ignore -->
```typeql
match $x isa person; $y isa person; not { $x is $y; }; 
```
[tab:end]

[tab:Java]
<!-- test-ignore -->
```java
TypeQLMatch query = TypeQL.match(
  var("x").isa("person"), 
  var("y").isa("person"),
  TypeQL.not(var("x").is(var("y")))
);
```
[tab:end]
</div>

### Comparators
When matching an instance of an attribute type based on its value or simply comparing two variables, the following comparators may be used: `=`, `!=`, `>`, `>=`, `<` and `<=`.

## Examples
To see some `get` queries powered by complex and expressive `match` clauses, check out the [examples of querying a sample knowledge graph](../08-examples/05-phone-calls-queries.md).

## Clients Guide

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing a query that contains a `match` clause, is as simple as calling the [`query().match()`](../03-client-api/01-java.md) method on a transaction and passing the query object to it.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing a query that contains a `match` clause, is as simple as passing the TypeQL(string) query to the `query().match()` function available on the [`transaction`](../03-client-api/03-nodejs.md#transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing a query that contains a `match` clause, is as simple as passing the TypeQL(string) query to the `query().match()` method available on the [`transaction`](../03-client-api/02-python.md#transaction) object.
</div>

## Summary
We learned how to use the `match` clause to write intuitive statements that describe a desired pattern in the knowledge graph and fill in the variables that hold the data we would like to acquire.

Next, we learn how to use the `match` clause in conjunction with TypeQL queries to carry out instructions - starting with the [get query](../11-query/02-get-query.md).
