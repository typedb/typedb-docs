---
sidebarTitle: Match
pageTitle: Match Clause
permalink: /docs/query/match-clause
---

## Match Concept Types and Their Instances
`match` clause describes a pattern in the knowledge graph. In other words, it uses the semantics of the knowledge graph as defined in the [schema](/docs/schema/overview) to find a specific match. We can use the `match` clause to target instances of data or concepts defined in the schema.

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing a query that contains a `match` clause, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eagerly-execute-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing a query that contains a `match` clause, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing a query that contains a `match` clause, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
</div>

## Variables
Graql assigns instances of data and schema concepts to variables. A Graql variable is prefixed with `$` and is simply a placeholder for an instance of a concept type or simply a hard-coded value.

In case of a hard-coded value, the accepted datatypes are:
- `long`: a 64-bit signed integer.
- `double`: a double-precision floating point number, including a decimal point.
- `string`: enclosed in double `"` or single `'` quotes
- `boolean`: `true` or `false`
- `date`: a date or date-time in ISO 8601 format

## Match Instances of Concept Types
What follows in this section, describes how we can use the `match` keyword to find instances of data that we are interested in. What we choose to do with the matched result, is out of the scope of this section. But for the sake of completeness, we end each `match` clause with `get;`. In the next section, we learn about [using _get_ for retrieval of information from the knowledge graph](/docs/query/get-query).

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
GraqlGet query = Graql.match(
  Graql.var("p").isa("person")
).get();
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
GraqlGet query = Graql.match(
  var("p").isa("person").has("full-name", var("n"))
).get();
```
[tab:end]
</div>


We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

### Match instances of a relationship
Because of the [dependent nature of relationships](/docs/schema/concepts#define-a-relationship), matching them is slightly different to matching entities and attributes.

<div class="tabs dark">

[tab:Graql]
```graql
match $emp (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("emp").isa("employment").rel("employer", "x").rel("employee", "y")
).get();
```
[tab:end]
</div>

The example above, for every employment, assigns the instance of the employment (relationship) type to the variable `$emp`, the instance of the employer organisation (entity) type to the variable `$x` and the instance of the employee person (entity) type to the variable `$y`.

#### Instances of a relationship with particular attributes
To only match the instances of relationships that own a specific attribute, we use the `has` keyword followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:Graql]
```graql
match $emp (employer: $x, employee: $y) isa employment, has reference-id $ref; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("emp").isa("employment").rel("employer", "x").rel("employee", "y").has("reference-id", var("ref"))
).get();
```
[tab:end]
</div>

We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

#### Leave the relationship instance unassigned
Assigning a relationship to a variable is optional. We may only be interested in the roleplayers of a certain relationship. In such case, we would write the above match clause like so:

<div class="tabs dark">

[tab:Graql]
```graql
match (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var().isa("employment").rel("employer", "x").rel("employee", "y")
).get();
```
[tab:end]
</div>

#### Leave the roles out
We can always chose to not include the lable of roles when matching a relationship. This, especially, makes sense when matching a relationship that relates to only one role.

<div class="tabs dark">

[tab:Graql]
```graql
match $fr ($x, $y) isa friendship; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("fr").isa("friendship").rel("x").rel("y")
).get();
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
GraqlGet query = Graql.match(
  var("x").val("like")
).get();
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
GraqlGet query = Graql.match(
  var("x").isa("nickname").val("Mitzi")
).get();
```
[tab:end]
</div>

This matches instances of attribute with label of `nickname` and value of `"Mitzi"`, regardless of what owns the attribute `nickname`.

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
GraqlGet query = Graql.match(
  var("phone-number").contains("+44")
).get();
```
[tab:end]
</div>

This matches instances of any attribute type whose value contains the substring `"+44"`.

#### With a given regex
The value of an attribute can also be matched using a regex.

<div class="tabs dark">

[tab:Graql]
```graql
match $x like "(Miriam Morton|Solomon Tran)"; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("phone-number").regex("(Miriam Morton|Solomon Tran)")
).get();
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
GraqlGet query = Graql.match(
  var("p").isa("person").has("nickname", var("nn")).has("full-name", var("fn"))
).get();
```
[tab:end]
</div>

#### Owners with attributes of given values
We can also match instances that own an attribute with a specific value.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has nickname "Mitzi", has phone-number contains "+44"; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("p").isa("person").has("nickname", "Mitzi").has("phone-number", Graql.contains("+44"))
).get();
```
[tab:end]
</div>

But if in this example, we still want to know how old exactly each John is? we can separate the condition like so.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has nickname "Mitzi", has phone-number $pn; $pn contains "+44"; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("p").isa("person").has("nickname", "Mitzi").has("phone-number", var("pn")),
  var("pn").contains("+44")
).get();
```
[tab:end]
</div>

### Disjunction of patterns
By default a collection of patterns in a `match` clause constructs a conjunction of patterns. To include patterns in form of a disjunction, we need o wrap each pattern in `{}` and place the `or` keyword in between them.

<div class="tabs dark">

[tab:Graql]
```graql
match $p isa person, has full-name $fn; { $fn contains "Miriam"; } or { $fn contains "Solomon"; }; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("p").isa("person").has("full-name", var("fn")),
  or(
    var("fn").contains("Miriam"),
    var("fn").contains("Solomon")
  )
).get();
```
[tab:end]
</div>

### Instances of a direct type
The type that an instance belongs to may be a subtype of another. This means when we use `isa`, we are matching all direct and indirect instances of the given type. To only match the direct instances, we use `isa!` instead. Given the [previous organisation example](/docs/schema/concepts#subtype-an-entity), if we were to only match the direct instances of `organisation`, we would write the match clause like so.

<div class="tabs dark">

[tab:Graql]
```graql
match $rr isa! romantic-relationship; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("rr").isaX("romantic-relationship")
).get();
```
[tab:end]
</div>

This query matches only the direct instances of `romantic-relationship`. That means the instances of `open-relationship`, `domestic-relationship` and `complicated-relationship` (which all subtype `romantic-relationship`) would not be included.

### One particular instance
Grakn assignes an auto-generated id to each instance. Although, this id is generated by Grakn solely for internal use, it is indeed possible to find an instance with its Grakn id.
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
GraqlGet query = Graql.match(
  var("x").id("V41016")
).get();
```
[tab:end]
</div>

### Comparators
When matching an instance of an attribute type based on its value or simply comparing two variables, the following comparators may be used: `==`, `!=`, `>`, `>=`, `<` and `<=`.

## Match Schema Concepts
In this section, we learn how we can use the `match` keyword to find patterns in the schema of a Grakn knowledge graph. Matching concepts of a schema is always preceded by `get;`. In the next section, we learn about [how to use the get keyword](/docs/query/get-query).

Having fully understood the [schema concepts](/docs/schema/concepts) and how they are defined, you can think of the following `match` examples as fill-in-the-blank questions, were the-blank is a Graql variable and the sentences are different parts of the schema statements.

### Subtypes of a given type
To match all concepts of a given type, we use the `sub` keyword. Here are the examples for matching subtypes of all concept types, including `thing` that is a supertype to all other types.

<div class="tabs dark">
[tab:Graql]
```graql
match $x sub thing; get;
match $x sub attribute; get;
match $x sub entity; get;
match $x sub role; get;
match $x sub relation; get;
```
[tab:end]

[tab:Java]
<!-- test-edge-case -->
<!-- ignore-test -->
```java
GraqlGet query_a = Graql.match(
  var("x").sub("thing")
).get();

GraqlGet query_b = Graql.match(
  var("x").sub("attribute")
).get();

GraqlGet query_c = Graql.match(
  var("x").sub("entity")
).get();

GraqlGet query_d = Graql.match(
  var("x").sub("role")
).get();

GraqlGet query_e = Graql.match(
  var("x").sub("relation")
).get();
```
[tab:end]
</div>

### Roles of a given relationship
Given a particular relationship, we can use the `relates` keyword to match all roles related to the given relationship type.

<div class="tabs dark">

[tab:Graql]
```graql
match employment relates $x; get;
```
[tab:end]

[tab:Java]
[tab:Java]
```java
GraqlGet query = Graql.match(
  type("employment").relates(var("x"))
).get();
```
[tab:end]
</div>

This matches all roles of the `employment` relationship - `employer` and `employee`.

#### Subroles of a given role in a super-relationship
When we learned about [subtyping relationships](/docs/schema/concepts#subtype-a-relationship), we saw that a role related to a sub-relationship is linked to a corresponding parent's role using the `as` keyword. We can use the same keyword in a `match` clause to match the corresponding role in the given sub-relationship.

<div class="tabs dark">

[tab:Graql]
```graql
match location-of-office relates $x as located-subject; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  type("location-of-office").relates(var("x")),
  var("x").sub("located-subject")
).get();
```
[tab:end]
</div>

This matches all the roles that correspond to the `located-subject` role of the relationship which `location-of-office` subtypes. In this case, the super-relationship being `location-of-everything` and the matched role being `located-subject`.

### Roleplayers of a given role
Given a role, we can match the concept types that play the given role by using the `plays` keyword.

<div class="tabs dark">

[tab:Graql]
```graql
match $x plays employee; get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
  var("x").plays("employee")
).get();
```
[tab:end]
</div>

This matches all concept types that play the role `employee` in any relationship.

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
GraqlGet query = Graql.match(
  var("x").has("title")
).get();
```
[tab:end]
</div>

This matches all concept types that own `title` as their attribute.

## Examples
To see some `get` queries powered by complex and expressive `match` clauses, check out the [examples of querying a sample knowledge graph](/docs/examples/queries).

## Summary
We learned how to use the `match` clause to write intuitive statements that describe a desired pattern in the knowledge graph and fill in the variables that hold the data we would like to acquire.

Next, we learn how to use the `match` clause in conjunction with Graql queries to carry out instructions - starting with the [get query](/docs/query/get-query).
