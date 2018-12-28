---
sidebarTitle: Match
pageTitle: Match Clause
permalink: /docs/query/match-clause
---

## Match Concept Types and Their Instances
`match` clause describes a pattern in the knowledge graph. In other words, it uses the semantics of the knowledge graph as defined in the [schema](/docs/schema/overview) to find a specific match. We can use the `match` clause to target instances of data or concepts defined in the schema.

## Variables
Graql assigns instances of data and schema concepts to variables. A Graql variable is prefixed with `$` and is simply a placeholder for an instance of a concept type or simply a hard-coded value.

In case of a hard-coded value, the accepted datatypes are:
- `long`: a 64-bit signed integer.
- `double`: a double-precision floating point number, including a decimal point.
- `string`: enclosed in double `"` or single `'` quotes
- `boolean`: `true` or `false`
- `date`: a date or date-time in ISO 8601 format

## Match Instances of Concept Types
What follows in this section, describes how we can use the `match` keyword to find instances of data that we are interested in. What we choose to do with the matched result, is out of the scope of this section. But for the sake of completeness, we end each `match` clause with `get;`. In the next section, we will learn about [using _get_ for retrieval of information from the knowledge graph](/docs/query/get-query).

### Match instances of an entity
Matching instances of an entity type is easy. We do so by using a variable followed by the `isa` keyword and the label of the entity type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  Graql.var("p").isa("person")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $p isa person; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $p isa person; get;")
```
[tab:end]
</div>

The example above, for every person, assigns the person (entity) instance to the variable `$p`.

#### Instances of an entity with particular attributes
To only match the instances of entities that own a specific attribute, we use the `has` keyword, followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has name $n; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("p").isa("person").has("name", var("n"))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $p isa person has name $n; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $p isa person has name $n; get;")
```
[tab:end]
</div>


We will soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

### Match instances of a relationship
Because of the [dependent nature of relationships](/docs/schema/concepts#define-a-relationship), matching them is slightly different to matching entities and attributes.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $emp (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  Var.isa("employment").rel("employer", "x").rel("employee", "y"),
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $emp (employer: $x, employee: $y) isa employment; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $emp (employer: $x, employee: $y) isa employment; get;")
```
[tab:end]
</div>

The example above, for every employment, assigns the instance of the employment (relationship) type to the variable `$emp`, the instance of the employer company (entity) type to the variable `$x` and the instance of the employee person (entity) type to the variable `$y`.

#### Instances of a relationship with particular attributes
To only match the instances of relationships that own a specific attribute, we use the `has` keyword followed by the attribute's label and a variable.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $emp (employer: $x, exmployee: $y) isa employment has reference-id $ref; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("emp").isa("employment").rel("employer", "x").rel("employee", "y").has("reference-id", var("ref")),
).get();

Stream<ConceptMap> answers = transaction.stream(query.toString());
```

[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $emp (employer: $x, employee: $y) isa employment has reference-id $ref; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $emp (employer: $x, employee: $y) isa employment has reference-id $ref; get;")
```
[tab:end]
</div>

We will soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

#### Leave the relationship instance unassigned
Assigning a relationship to a variable is optional. We may only be interested in the roleplayers of a certain relationship. In such case, we would write the above match clause like so:

<div class="tabs dark">

[tab:Graql]
```lang-graql
match (employer: $x, employee: $y) isa employment; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = query_builder.match(
  var().isa("employment").rel("employer", "x").rel("employee", "y")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match (employer: $x, employee: $y) isa employment; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match (employer: $x, employee: $y) isa employment; get;")
```
[tab:end]
</div>

#### Leave the roles out
We can always chose to not include the lable of roles when matching a relationship. This, especially, makes sense when matching a relationship that relates to only one role.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $fr ($x, $y, $z) isa friendship; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = query_builder.match(
  var("fr").isa("friendship").rel("x").rel("y").rel("z"),
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $fr ($x, $y, $z) isa friendship; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $fr ($x, $y, $z) isa friendship; get;")
```
[tab:end]
</div>

### Match instances of an attribute
We can match instances of attribute types in various ways depending on our use case.

#### Independent of label
We can match instances of attributes type based on their value regardless of their label.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $x "some value"; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("x").val("some value")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $x "some value"; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $x "some value"; get;')
```
[tab:end]
</div>

This matches instances of any attribute type whose value is `"some value"` and assigns each to variable `$x`.

#### Independent of owner
We can match instances of attributes based on their value regardless of what concept type they belong to.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $n isa name "John"; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("x").isa("name").val("John")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $n isa name "John"; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $n isa name "John"; get;')
```
[tab:end]
</div>

This matches instances of attribute with label of `name` and value of `"John"`, regardless of what owns the attribute `name`.

#### With a given subset
To match all instances of attribute types that contain a substring, we use the `contains` keyword.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $phone-number contains "+44"; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("phone-number").val(Predicates.contains("+44"))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $phone-number contains "+44"; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $phone-number contains "+44"; get;')
```
[tab:end]
</div>

This matches instances of any attribute type whose value contains the substring `"+44"`.

#### With a given regex
The value of an attribute can also be matched using a regex.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $x /.*(Mary|Barbara).*/; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("phone-number").val(Predicates.regex("/.*(Mary|Barbara).*/"))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $x /.*(Mary|Barbara).*/; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $x /.*(Mary|Barbara).*/; get;')
```
[tab:end]
</div>

This matches the instances of any attribute type whose value matches the given regex - `"Mary"` or `"Barbara"`.

#### Owners with multiple attributes
To match instances of a concept type that owns multiple attributes, we can simply chain triples of `has`, label and variable. Separating each triple with a comma is optional.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has first-name $fn, has last-name $ln; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("phone-number").val(Predicates.regex(/.*(Mary|Barbara).*/))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $x /.*(Mary|Barbara).*/; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $x /.*(Mary|Barbara).*/; get;')
```
[tab:end]
</div>

#### Owners with attributes of given values
We can also match instances that own an attribute with a specific value.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has first-name "John" has age < 25; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("p").isa("person").has("first-name", "John").has("age", Predicates.lt(25))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $p isa person has first-name "John" has age < 25; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $p isa person has first-name "John" has age < 25; get;')
```
[tab:end]
</div>

But if in this example, we still want to know how old exactly each John is? we can separate the condition like so.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $p isa person has first-name "John" has age $a; $a < 25; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("p").isa("person").has("name", "John").has("age", var("a")),
  var("a").val(Predicates.lt(25))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query('match $p isa person has first-name "John" has age $a; $a < 25; get;');
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query('match $p isa person has first-name "John" has age $a; $a < 25; get;')
```
[tab:end]
</div>

### Instances of a direct type
The type that an instance belongs to may be a subtype of another. This means when we use `isa`, we are matching all direct and indirect instances of the given type. To only match the direct instances, we use `isa!` instead. Given the [previous organisation example](/docs/schema/concepts#subtype-an-entity), if we were to only match the direct instances of `organisation`, we would write the match clause like so.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $o isa! organisation; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("o").isaExplicit("organisation")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $o isa! organisation; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $o isa! organisation; get;")
```
[tab:end]

The matches only the direct instances of `organisation`. That means the instances of `company` and `university` (which subtype `organisation`) would not be included.
</div>

### One particular instance
To match a particular instance with the given ID, we use the `id` keyword followed by the `id` assigned to the instance by Grakn.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $x id V41016; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("x").id(ConceptId.of("V41016"))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $x id V41016; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $x id V41016; get;")
```
[tab:end]
</div>

### Comparators
When matching an instance of an attribute type based on its value or simply comparing two variables, the following comparators may be used: `==`, `!=`, `>`, `>=`, `<` and `<=`.

## Match Schema Concepts
In this section, we learn how we can use the `match` keyword to find patterns in the schema of a Grakn knowledge graph. Matching concepts of a schema is always preceded by `get;`. In the next section, we will learn about [how to use the get keyword](/docs/query/get-query).

Having fully understood the [schema concepts](/docs/schema/concepts) and how they are defined, you can think of the following `match` examples as fill-in-the-blank questions, were the-blank is a Graql variable and the sentences are different parts of the schema statements.

### Subtypes of a given type
To match all concepts of a given type, we use the `sub` keyword. Here are the examples for matching subtypes of all concept types, including `thing` that is a supertype to all other types.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $x sub thing; get;
match $x sub attribute; get;
match $x sub entity; get;
match $x sub role; get;
match $x sub relationship; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query_a = Graql.match(
  var("x").sub("thing")
).get();

Stream<ConceptMap> answers = transaction.stream(query_a.toString());

GetQuery query_b = Graql.match(
  var("x").sub("attribute")
).get();

Stream<ConceptMap> answers = transaction.stream(query_b.toString());

GetQuery query_c = Graql.match(
  var("x").sub("entity")
).get();

Stream<ConceptMap> answers = transaction.stream(query_c.toString());

GetQuery query_d = Graql.match(
  var("x").sub("role")
).get();

Stream<ConceptMap> answers = transaction.stream(query_d.toString());

GetQuery query_e = Graql.match(
  var("x").sub("relationship")
).get();

Stream<ConceptMap> answers = transaction.stream(query_e.toString());
```
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIteratorA = await transaction.query("match $x sub thing; get;");
const answerIteratorB = await transaction.query("match $x sub attribute; get;");
const answerIteratorC = await transaction.query("match $x sub entity; get;");
const answerIteratorD = await transaction.query("match $x sub role; get;");
const answerIteratorE = await transaction.query("match $x sub relationship; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator_a = transaction.query("match $x sub thing; get;")
answer_iterator_b = transaction.query("match $x sub attribute; get;")
answer_iterator_c = transaction.query("match $x sub entity; get;")
answer_iterator_d = transaction.query("match $x sub role; get;")
answer_iterator_e = transaction.query("match $x sub relationship; get;")
```
[tab:end]
</div>

### Roles of a given relationship
Given a particular relationship, we can use the `relates` keyword to match all roles related to the given relationship type.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match employment relates $x; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  label("employment").relates(var("x"))
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match employment relates $x; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match employment relates $x; get;")
```
[tab:end]
</div>

This matches all roles of the `employment` relationship - `employer` and `employee`.

#### Subroles of a given role in a super-relationship
When we learned about [subtyping relationships](/docs/schema/concepts#subtype-a-relationship), we saw that a role related to a sub-relationship is linked to a corresponding parent's role using the `as` keyword. We can use the same keyword in a `match` clause to match the corresponding role in the given sub-relationship.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match employment relates $x as member; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  label("employment").relates(var("x")),
  var("x").sub("member")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match employment relates $x as member; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match employment relates $x as member; get;")
```
[tab:end]
</div>

This matches all the roles that correspond to the `member` role of the relationship which `employment` subtypes. In this case, the super-relationship being `membership` and the matched role being `employee`.

### Roleplayers of a given role
Given a role, we can match the concept types that play the given role by using the `plays` keyword.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $x plays employee; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("x").plays("employee")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $x plays employee; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $x plays employee; get;")
```
[tab:end]
</div>

This matches all concept types that play the role `employee` in any relationship.

## Owners of a given attribute
Given an attribute type, we can match the concept types that own the given attribute type by using the `has` keyword.

<div class="tabs dark">

[tab:Graql]
```lang-graql
match $x has name; get;
```
[tab:end]

[tab:Java]
```lang-java
GetQuery query = Graql.match(
  var("x").has("name")
).get();

List<ConceptMap> answers = query.withTx(transaction).execute();
```
<!-- Stream<ConceptMap> answers = transaction.stream(query.toString()); -->
[tab:end]

[tab:Javascript]
```lang-javascript
const answerIterator = await transaction.query("match $x has name; get;");
```
[tab:end]

[tab:Python]
```lang-python
answer_iterator = transaction.query("match $x has name; get;")
```
[tab:end]
</div>

This matches all concept types that own `name` as their attribute.

## Examples
To see some `get` queries powered by complex and expressive `match` clauses, check out the [examples of querying a sample knowledge graph](/docs/examples/queries).

## Summary
We learned how to use the `match` clause to write intuitive statements that describe a desired pattern in the knowledge graph and fill in the variables that hold the data we would like to acquire.

Next, we will learn how to use the `match` clause in conjunction with Graql queries to carry out instructions - starting with the [get query](/docs/query/get-query).
