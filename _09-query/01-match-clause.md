---
title: Match Clause
keywords: graql, query, match
tags: [graql]
summary: "Describing patterns in a Grakn knowledge graph."
permalink: /docs/query/match-clause
---

## Introduction
`match` clause describes a pattern in the knowledge graph. In other words, it use the semantics of the knowledge graph as defined in the [schema](/docs/schema/overview) to find a specific match. We can use the `match` clause to target instances of data or elements of the schema.

## Variables
Graql assigns instances and values to variables. A Graql variable is prefixed with `$` and is simply a placeholder for an instance that may be of type [entity](/docs/schema/concepts#entity), [relationship](/docs/schema/concepts#relationship), [attribute](/docs/schema/concepts#attribite) or simply a hard-coded value of our own.

In case of a hard-coded value, the accepted data types are:
- long: a 64-bit signed integer.
- double: a double-precision floating point number, including a decimal point.
- string: enclosed in double `"` or single `'` quotes
- boolean: `true` or `false`
- date: a date or date-time in ISO 8601 format

## Matching Data Instances
What follows in this section, describes how we can use the `match` keyword to find instances of data that we are interested in. What we want to do with the matched instances, is out of the scope of this section. But for the sake of completeness, we end each `match` clause with `get;`. In the next section, we will learn about [using _get_ for reading the knowledge graph](...).

### Matching instances of an entity
Matching instances of an entity type is easy. We do so by using a variable followed by the `isa` keyword and the label of the entity of interest. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $p isa person; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("p").isa("person")
).get();
```
<!-- for (ConceptMap answer : answer_iterator) {
  System.out.println(answer.get("p").id());
} -->
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $p isa person; get;");
```
<!-- let answer = await answerIterator.next();
while (answer != null) {
  console.log(answer.map().get("p")["id"]);
  answer = await answerIterator.next();
} -->
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $p isa person; get;")
```
<!-- answer = next(answer_iterator, done)
while (answer is not null):
  print(answer.map().get("p").id)
  answer = next(answer_iterator, done) -->
[tab:end]
</div>

The example above, for every person, assigns the person (entity) instance to the variable `$p`.

#### Instances of an entity with particular attributes
To narrow down the match on an entity, we can specify the attributes that the entity must own. To do so, we use the `has` keyword. Let's look at an example.


<div class="tabs">

[tab:Graql]
```graql
match $p isa person has name $n; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("p").isa("person").has("name", var("n"))
).get();
```
<!-- for ( ConceptMap answer : answer_iterator) {
  System.out.println(answer.get("n").asAttribute().value());
} -->
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $p isa person has name $n; get;");
```
<!-- let answer = await answerIterator.next();
while (answer != null) {
  console.log(await answer.map().get("n").value());
  answer = await answerIterator.next();
} -->
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $p isa person has name $n; get;")
```
<!-- answer = next(answer_iterator, done)
while (answer is not null):
  print(answer.map().get("n").value())
  answer = next(answer_iterator, done) -->
[tab:end]
</div>


We will soon learn how this `match` clause can be extended by [targeting attributes more specifically](#matching-instances-of-an-attribute).

### Matching instances of a relationship
Because of the dependent nature of relationships, matching them is quite different to matching entities and attributes. Let's look at an example.


<div class="tabs">

[tab:Graql]
```graql
match $emp (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  Var.isa("employment").rel("employer", "x").rel("employee", "y"),
).get();
```
<!-- for ( ConceptMap answer : answer_iterator) {
  System.out.println("employment: " + answer.get("emp").id());
  System.out.println("employer: " + answer.get("x").id());
  System.out.println("employee: " + answer.get("y").id());
} -->
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $emp (employer: $x, employee: $y) isa employment; get;");
```
<!-- let answer = await answerIterator.next();
while (answer != null) {
  answer = await answer.map();
  console.log("employment: " + answer.get("emp")["id"]);
  console.log("employer: " + answer.get("x")["id"]);
  console.log("employee: " + answer.get("y")["id"]);
  answer = await answerIterator.next();
} -->
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $emp (employer: $x, employee: $y) isa employment; get;")
```
<!-- done = object()
  answer = next(answer_iterator, done)
  while (answer is not done):
    print("employment: " + answer.map().get("emp").id)
    print("employer: " + answer.map().get("x").id)
    print("employee: " + answer.map().get("y").id)
    answer = next(answer_iterator, done) -->
[tab:end]
</div>

The example above, for every employment, assigns the employment (relationship) instance to the variable `$emp`, the employer company (entity) to the variable `$x` and the employee person (entity) to the variable `$y`.

#### Instances of a relationship with particular attributes
To narrow down the match on a relationship, we can specify the attributes that the relationship must own. To do so, we use the `has` keyword. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $emp (employer: $x, exmployee: $y) isa employment has reference-id $ref; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("emp").isa("employment").rel("employer", "x").rel("employee", "y").has("reference-id", var("ref")),
).get();
```

[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $emp (employer: $x, employee: $y) isa employment has reference-id $ref; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $emp (employer: $x, employee: $y) isa employment has reference-id $ref; get;")
```
[tab:end]
</div>

We will soon learn how this `match` clause can be extended by [targeting more specific attributes](#matching-instances-of-an-attribute).

#### Leaving the instance unassigned
Assigning a relationship to a variable is optional. We may only be interested in the roleplayers of a certain relationship. In such case, we would write the above like so:

```graql
match (employer: $x, employee: $y) isa employment; get;
```

#### Leaving the roles out
In scenarios where the relationship relates to only one role, we can omit the roles altogether. Let's look at another example.

<div class="tabs">

[tab:Graql]
```graql
match $fr ($x, $y, $z) isa friendship; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("fr").isa("friendship").rel("x").rel("y").rel("z"),
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $fr ($x, $y, $z) isa friendship; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $fr ($x, $y, $z) isa friendship; get;")
```
[tab:end]
</div>

### Matching instances of an attribute
Instances of attributes can be matched in various ways depending on the use case.

#### Independent of type
We can match instances of attributes based on their value regardless of what type of attribute they are. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $x "some value"; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("x").val("some value")
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $x "some value"; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $x "some value"; get;')
```
[tab:end]
</div>

This, matches instances of any attribute type whose value is "some value" and assigns them to variable `$x`.

#### Independent of owner
We can match instances of attributes based on their value regardless of what they belong to. Let's look an example.

<div class="tabs">

[tab:Graql]
```graql
match $n isa name "John"; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("x").isa("name").val("John")
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $n isa name "John"; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $n isa name "John"; get;')
```
[tab:end]
</div>

This matches instances of attribute `name` with value `"John"`, regardless of what owns the attribute `name`.

#### With a given subset
To match all instances of attributes that contain a substring, we use the `contains` keyword. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $phone-number contains "+44"; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("phone-number").val(Predicates.contains("+44"))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $phone-number contains "+44"; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $phone-number contains "+44"; get;')
```
[tab:end]
</div>

This matches instances of any attribute whose value contains the substring `"+44"`.

#### With a given regex
The value of an attribute can also be matched using a regex. Let's look an example.

<div class="tabs">

[tab:Graql]
```graql
match $x /.*(Mary|Barbara).*/; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("phone-number").val(Predicates.regex("/.*(Mary|Barbara).*/"))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $x /.*(Mary|Barbara).*/; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $x /.*(Mary|Barbara).*/; get;')
```
[tab:end]
</div>

This matches the instances of any attribute whose value matches the given regex - `"Mary"` or `"Barbara"`.

#### Owners with multiple attributes
To match instances of a thing that owns multiple attributes, we can simply chain triples of `has` + label + variable. Separating each triple with a comma is optional.

<div class="tabs">

[tab:Graql]
```graql
match $p isa person has first-name $fn, has last-name $ln; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("phone-number").val(Predicates.regex(/.*(Mary|Barbara).*/))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $x /.*(Mary|Barbara).*/; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $x /.*(Mary|Barbara).*/; get;')
```
[tab:end]
</div>

#### Owners with attributes of given values
We can also match instances that have an attribute with a specific value. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $p isa person has first-name "John" has age < 25; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = query_builder.match(
  var("p").isa("person").has("first-name", "John").has("age", Predicates.lt(25))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $p isa person has first-name "John" has age < 25; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $p isa person has first-name "John" has age < 25; get;')
```
[tab:end]
</div>

But if in this example, we still want to know how old exactly each John is? we can separate the condition like so.

<div class="tabs">

[tab:Graql]
```graql
match $p isa person has first-name "John" has age $a; $a < 25; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = queryBuilder.match(
  var("p").isa("person").has("name", "John").has("age", var("a")),
  var("a").val(Predicates.lt(25))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query('match $p isa person has first-name "John" has age $a; $a < 25; get;');
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query('match $p isa person has first-name "John" has age $a; $a < 25; get;')
```
[tab:end]
</div>

### Instances of a direct type
The type that an instance belongs to may be a subtype of another. This means when we use `isa` we are matching all direct and indirect instances of the given type. To only match the direct instances, we use `isa!` instead. Given the [previous organisation example](/docs/schema/concepts#subtyping-an-entity), if we were to only match the direct instances of `organisation`, we would write the match clause like so.

<div class="tabs">

[tab:Graql]
```graql
match $o isa! organisation; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = queryBuilder.match(
  var("o").isaExplicit("organisation")
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $o isa! organisation; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $o isa! organisation; get;")
```
[tab:end]

The example above matches only the direct instances of `organisation`. That means the instances of `company` and `university` (which subtype `organisation`) would not be included.
</div>

### One particular instance
To match a particular instance with the given ID, we use the `id` keyword. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $x id V41016; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = queryBuilder.match(
  var("x").id(ConceptId.of("V41016"))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $x id V41016; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $x id V41016; get;")
```
[tab:end]
</div>

### Comparators
When matching an instance of an attribute based on its value or simply comparing two variables, the following comparators can be used: `==`, `!=`, `>`, `>=`, `<` and `<=`

## Matching Schema Elements
In this section, we learn how we can use the `match` keyword to find patterns in the schema of a Grakn knowledge graph. What we choose to do with the matched schema elements, is out of the scope of this section. But for the sake of completeness, we end each `match` clause with `get;`. In the next section, we will learn about [using _get_ for reading the knowledge graph](...).

Having fully understood the [schema concepts](/docs/schema/concepts) and how they are defined, you can think of the following `match` examples as fill-in-the-blank questions, were the-blank is a Graql variable and the sentences are different parts of the schema as defined in the `schema.gql` file.

### Subtypes of a given type
To match all concepts of a given type, we use the `sub` keyword. Here are the examples for matching subtypes of all concepts types, including `thing` that is a parent to all other types.

<div class="tabs">

[tab:Graql]
```graql
match $x sub thing; get;
match $x sub attribute; get;
match $x sub entity; get;
match $x sub role; get;
match $x sub relationship; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator_a = queryBuilder.match(
  var("x").sub("thing")
).get();

GetQuery answer_iterator_b = queryBuilder.match(
  var("x").sub("attribute")
).get();

GetQuery answer_iterator_c = queryBuilder.match(
  var("x").sub("entity")
).get();

GetQuery answer_iterator_d = queryBuilder.match(
  var("x").sub("role")
).get();

GetQuery answer_iterator_e = queryBuilder.match(
  var("x").sub("relationship")
).get();

```
[tab:end]

[tab:Javascript]
```javascript
const answerIteratorA = await transaction.query("match $x sub thing; get;");
const answerIteratorB = await transaction.query("match $x sub attribute; get;");
const answerIteratorC = await transaction.query("match $x sub entity; get;");
const answerIteratorD = await transaction.query("match $x sub role; get;");
const answerIteratorE = await transaction.query("match $x sub relationship; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator_a = transaction.query("match $x sub thing; get;")
answer_iterator_b = transaction.query("match $x sub attribute; get;")
answer_iterator_c = transaction.query("match $x sub entity; get;")
answer_iterator_d = transaction.query("match $x sub role; get;")
answer_iterator_e = transaction.query("match $x sub relationship; get;")
```
[tab:end]
</div>

### Roles of a given relationship
Given a particular relationship, we can use the `relates` keyword to match all roles related to that relationship. Let's look an example.

<div class="tabs">

[tab:Graql]
```graql
match employment relates $x; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator_e = queryBuilder.match(
  label("employment").relates(var("x"))
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match employment relates $x; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match employment relates $x; get;")
```
[tab:end]
</div>

This matches all roles of the `employment` relationship - `employer` and `employee`.

#### Subroles of a given role in a super-relationship
As we learned about [subtyping relationships](/docs/schema/concepts#subtyping-a-relationship), we saw that a role related to a sub-relationship is linked to a corresponding parent's role using the `as` keyword. We can use the same keyword in a `match` clause to match the corresponding role in the given sub-relationship. Let's look an example.

<div class="tabs">

[tab:Graql]
```graql
match employment relates $x as member; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator_e = queryBuilder.match(
  label("employment").relates(var("x")),
  var("x").sub("member")
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match employment relates $x as member; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match employment relates $x as member; get;")
```
[tab:end]
</div>

This matches all the roles that correspond to the `member` role of the relationship which `employment` subtypes. In this case, the super-relationship being `membership` and the matched role being `employee`.

### Roleplayers of a given role
Given a role, we can match the `thing`s that play that role by using the `plays` keyword. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $x plays employee; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = queryBuilder.match(
  var("x").plays("employee")
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $x plays employee; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $x plays employee; get;")
```
[tab:end]
</div>

This matches all `thing`s that play the role `employee` in any relationship - `person`.

## Owners of a given attribute
Given an attribute, we can match the `thing`s that own that attribute by using the `has` keyword. Let's look at an example.

<div class="tabs">

[tab:Graql]
```graql
match $x has name; get;
```
[tab:end]

[tab:Java]
```java
GetQuery answer_iterator = queryBuilder.match(
  var("x").has("name")
).get();
```
[tab:end]

[tab:Javascript]
```javascript
const answerIterator = await transaction.query("match $x has name; get;");
```
[tab:end]

[tab:Python]
```python
answer_iterator = transaction.query("match $x has name; get;")
```
[tab:end]
</div>

This matches all `thing`s that have `name` as their attribute - `person`, `organisation`, `company` and `university`.

Note: although, `name` has explicitly been assigned to only `person` and `organisation`, the matched `thing`s include `company` and `university` as well. This is because they both subtype `organisation` and therefore inherit `name` as an attribute of their own.

## Examples
To see some `get` queries powered by complex and expressive `match` clause, check out the [examples of querying a sample knowledge graph](/docs/examples/queries).

## Summary
We learned how to use the `match` clause to write intuitive statements that describe a desired pattern in the knowledge graph and fill in the variables that hold the data we would like to acquire.

Next, we will learn how to use the `match` clause in conjunction with Graql queries to carry out instructions - starting with the [get query](/docs/schema/concepts).
