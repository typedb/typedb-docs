---
pageTitle: Match query
keywords: typeql, query, match, pattern, statement, variable
longTailKeywords: typeql match, match get, query patterns, match clause, typeql variables
Summary: Targeting instances of data or schema types that match expressive patterns in TypeDB.
---

# Match query

We use `match` keyword to retrieve data instances and schema types that follow a particular pattern. Using `match` 
statement forms the basis of our data retrieval or even data modification query. By defining the [schema](05-schema.md),
we effectively define a vocabulary to be used to describe concepts of our knowledge domain.

Once the schema is defined, we can form patterns for which we want to search within our data. We do 
that by using `match` keyword. Each match statement represents a particular pattern via its corresponding query 
pattern. The match clause is then executed as a part of other types of queries:

- [Get](../../11-query/02-get-query.md) — returns data instances or types fulfilling the specified pattern.
- [Insert](../../11-query/03-insert-query.md) — inserts new data instances using specified pattern as context.
- [Delete](../../11-query/04-delete-query.md) — deletes data instances fulfilling the specified pattern.
- [Aggregate](../../11-query/06-aggregate-query.md) — calculates a value using data instances or types fulfilling the 
  specified pattern as context.

We can query schema with `match` and `get` keywords. We can even use aggregate with the results if we want. But to 
change the schema we must use `define` or `udefine` keywords.

## Query pattern anatomy

At the core of each query sits a query pattern that describes a subset of data of our particular interest. Here we
examine the structure of query patterns closer. In general, patterns can be thought of as different arrangements of
statement collections. TypeQL statements constitute the smallest building blocks of queries. Let's have a close
look at the constructs of a basic match clause.

![Statement structure](../../images/query/statement-structure.png)

- Most statements start with a **variable** (`V`) providing a concept reference. We can reference both data and schema
  concepts via variables. A TypeQL variable is prefixed with a dollar sign `$`.

- The variable is followed by a comma-separated list of **properties** (`P1`, `P2`, `P3`) describing the concepts the
  variable refers to. Here we can see that all the concepts that variable `$p` refers to, must be of type `person`.
  The matched instances are expected to own an attribute of type `name` with the value of `"Masako Holley"`.  
  Additionally, we require the concepts to own an attribute of type `email` with any value. We signal that 
  we want to fetch the owned `email`s as well by defining an extra `$email` variable. Consequently, after 
  performing a match on this statement, we should obtain pairs of concepts that satisfy our statement.

- We mark the end of the statement with a semi-colon `;`.

There is some freedom in forming and composing our statements. For example, as shown below, we could write our 
single statement with three properties as three combined statements.

<!-- test-ignore -->
```typeql
$p isa person;
$p has name 'Masako Holley';
$p has email $email;
```

Lastly, to create a viable query from that statement, we need to add `match` keyword at the beginning. After that it 
is ready to be sent to the TypeDB server in a data read transaction.

<div class="note">
[Important]
We can send queries to read or write schema or data of a database. So the `match` keyword can be used with both data 
and schema concepts. But to write into the schema we shall use `define` or `undefine`.
</div>

## Match Schema Concepts

We can use the `match` keyword to find types in the schema of a TypeDB database. 

### Match Everything

We can request everything from a schema. To do that we would use `Thing` concept. As every schema concept is a 
subtype of `Thing` we can do it like that: 

```typeql
match $s sub thing;
```

<div class="note">
[Important]
By default, if we send `match` query without stating what we want to do with matched pattern (without the get 
statement in the example above) it is processed as `match ... get` query, so it returns all mentioned variables.
</div>

### Examples of combining with other types of queries

#### Get

Get all attributes owned by user type and all its subtypes:

```typeql
match $u sub user, owns $a; get $a;
```

#### Insert

Use [define](05-schema.md#define) instead.

#### Delete

Use [undefine](05-schema.md#undefine) instead.

#### Aggregate

Count the number of types there are subtyping a `user` type (including the `user` type itself) and owning any attribute:

```typeql
match $u sub user, owns $a; get $u; count;
```

### Direct and Indirect Subtypes of a Given Type

To match all schema concepts of a given type, **all the way down the type hierarchy**, we use the `sub` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $o sub object;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query_a = TypeQL.match(
//var("o").sub("object")
//);
```
[tab:end]
</div>

Running the above query on the `iam` [schema](../01-start/03-quickstart.md#fifth-step--prepare-a-schema), returns  
the `object` concept type itself, as well as all concept types that are subtypes of `object`, directly (i.e. 
`resource` and `resource-collection`) and indirectly (i.e. `file`, `interface`, `directory` and `application`).

<!--- #todo Think of Adding query result illustration -->

### Direct Subtypes of a Given Type

To match the schema concepts that are **direct subtypes** of a given type, we use the `sub!` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $o sub! object;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query_a = TypeQL.match(
//  var("o").subX("object")
//);
```
[tab:end]
</div>

Running the above query on the `iam` [schema](../01-start/03-quickstart.md#fifth-step--prepare-a-schema), returns direct 
subtypes of the `object` type itself (i.e. `resource` and `resource-collection`).

### Given Type Only

To match only the given type and not any of its subtypes, we use the `type` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $o type object;
```
[tab:end]

[tab:Java]
<!-- test-delay -->
```java
//TypeQLMatch.Filtered query_a = TypeQL.match(
//  var("o").type("object")
//);
```
[tab:end]
</div>

Running the above query, returns only the concept type that has the label `object`.

### Roles of a Given Relation

Given a particular relation, we can use the `relates` keyword to match all roles related to the given relation type.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match permission relates $x;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  type("permission").relates(var("x"))
//);
```
[tab:end]
</div>

This matches all roles of the `permission` relation — `permission:permitted-access` and `permission:permitted-subject`.

#### Subroles of a Given Role
<!--- Revisit this one ====================================================================================== -->

Role related to a sub-relation is linked to a corresponding parent's role using the `as` keyword. We can use the 
same keyword in a `match` clause to match the corresponding role in the given sub-relation.

<div class="tabs dark">

[tab:TypeQL]
<!-- test-delay -->
```typeql
match group-membership relates $x as member; get $x;
```
[tab:end]

[tab:Java]
<!-- test-delay -->
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  type("group-membership").relates(var("x"), "member")
//).get("x");
```
[tab:end]
</div>

This matches all the roles that correspond to the `member` role of the relation which `group-membership` subtypes. In 
this case, the super-relation being `membership` and the matched role being `group-member`.

### Role Players of a Given Role

We can match the concept types that play the given role by using the `plays` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x plays permission:permitted-subject;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("x").plays("permission", "permitted-subject")
//);
```
[tab:end]
</div>

This matches all concept types that play the role `permitted-subject` in any relation.

### Owners of a Given Attribute

Given an attribute type, we can match the concept types that own the given attribute type by using the `owns` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x owns name;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("x").owns("name")
//);
```
[tab:end]
</div>

This matches all concept types that own `name` as their attribute.

## Match Data

We can use the `match` keyword to find instances of types or data in a TypeDB database.

### Match Everything

We can request every instance of data from a database. To do that we would use `Thing` concept. As every schema concept 
is a subtype of `Thing` we can do it like that:

```typeql
match $t isa thing; get $t;
```

<!--- Add Java example -->

### Examples of combining with other types of queries

#### Get

Get an E-mail of a user with name "Kevin Morrison":

```typeql
match $u isa user, has name 'Kevin Morrison', has email $email; get $email;
```

<div class="note">
[Note]
If we drop the `get $email` part the query will still perform as `get` query but will return all variables from 
`match` statement. 
</div>

#### Insert

Insert a new E-mail for a user with name "Kevin Morrison":

```typeql
match $u isa user, has name 'Kevin Morrison'; insert $u has email "k.morrison@vaticle.com";
```

#### Delete

Delete an E-mail "k.morrison@vaticle.com" for a user with name "Kevin Morrison":

```typeql
match $u isa user, has name "Kevin Morrison", has email $email; $email "k.morrison@vaticle.com"; delete $email isa email;
```

The query is a bit longer than expected, but that can be explained by the constraints of the `delete` statement.
We need to use variable for a deleted concept, hence we add the `$email`. We need to use a proper statement with
`delete` keyword, that is why we use the `delete $email isa email` and not just `delete $email`.

<div class="note">
[Note]
If we use the statement `delete $u has $email` instead we will delete ownership of the email attribute $email but 
the instance itself will be left hanging;
</div>

#### Aggregate

Count the number of users:

```typeql
match $u isa user; get $u; count;
```

### Match Instances of an Entity

Matching instances of an entity type is easy. We do so by using a variable followed by the `isa` keyword and the 
label of the entity type.

<div class="note">
[Warning]
Using `isa` will return all direct and indirect instances (instances of all subtypes of the given type). To limit 
results to only direct instances of the given type use `isa!` instead. See the [Example](#instances-of-a-direct-type).
</div>

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("p").isa("person")
//);
```
[tab:end]
</div>

The example above will return all instance of the person type and any of it's sub-types.

#### Instances of an entity with particular attributes

To only match the instances of entities that own a specific attribute, we use the `has` keyword, followed by the 
attribute's label and a variable.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has name $n;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("p").isa("person").has("name", var("n"))
//);
```
[tab:end]
</div>

We soon learn [how to target attributes of a specific value](#owners-with-attributes-of-given-values).

### Match instances of a relation

Because of the [dependent nature of relations](../02-dev/05-schema.md#relation), matching them is slightly different to 
matching entities and attributes as we usually need to add some details of the participants of the relation.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has name "Kevin Morrison";
$pe (permitted-subject: $p, permitted-access: $ac) isa permission; get $pe;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//var(p).isa("person").has("name", "Kevin Morrison"), var("pe").rel("permitted-subject", var("p")).rel
//        ("permitted-access", var("ac")).isa("permission")
//).get(var("pe"));
```
[tab:end]
</div>

In the example above, for given instance of `person` type that has `name` attribute with a value of `Kevin Morrison` 
we look for every permission, where this instance of `person` plays role `permitted-subject`. And we get all the 
resulted permissions as a result.

#### Instances of a relation with particular attributes

To only match the instances of relations that own a specific attribute, we use the `has` keyword followed by the 
attribute's label and a variable.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $pe (permitted-subject: $p, permitted-access: $ac) isa permission, has validity "True"; get $pe;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//var("pe").rel("permitted-subject", var("p")).rel("permitted-access", var("ac")).isa("permission")).has("validity",
//        "True")
//).get(var("pe"));
```
[tab:end]
</div>

We soon learn [how to target attributes of a specific value](#match-instances-of-an-attribute).

#### Leave the relation instance unassigned

Assigning a relation to a variable is optional. We may only be interested in the role players of a certain relation. 
In such a case, we would write the above match clause like so:

<div class="tabs dark">

[tab:TypeQL]
```typeql
match (permitted-subject: $p, permitted-access: $ac) isa permission;
```
[tab:end]

[tab:Java]
```java
// FIXME(vmax): anonymous variables are not allowed 
//TypeQL.Filtered query = TypeQL.match(
//  var().isa("permission").rel("permitted-subject", "p").rel("permitted-access", "ac")
//).get();
```
[tab:end]
</div>

#### Leave the roles out

We can always choose to not include the label of roles when matching a relation. This, especially, makes sense when 
matching a relation that relates to only one role.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $sp ($x, $y) isa segragation-policy; get $sp;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("sp").rel("x").rel("y").isa("segragation-policy")
//).get("sp");
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
match $x "Masako Holley";
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("x").eq("Masako Holley")
//);
```
[tab:end]
</div>

This matches instances of any attribute type whose value is `Masako Holley` (for instance, a person, user-group, 
action or user-role) and assigns each to variable `$x`.

#### Independent of owner
<!--- Consider removing this example -->

We can match instances of attributes based on their value regardless of what concept type they belong to.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $n isa name; $n "Masako Holley"; get $n;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("x").eq("Masako Holley").isa("name")
//);
```
[tab:end]
</div>

This matches instances of the attribute with the label of `name` and value of `Masako Holley`, regardless of what 
owns the attribute `name`.

#### Contains string

To match all instances of attribute types that contain a substring, we use the `contains` keyword.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $name contains "Masako"; get $name;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("name").contains("Masako")
//).get("name");
```
[tab:end]
</div>

This matches instances of any attribute type whose value contains the substring `Masako`.

#### With a given regex

The value of an attribute can also be matched using a regular expression or regex. We allow the range of 
[Java Regex Patterns](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html).

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $x like "(Masako Holley|Kevin Morrison)";
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("x").regex("(Masako Holley|Kevin Morrison)")
//);
```
[tab:end]
</div>

This matches the instances of any attribute type whose value matches the given regex - `Masako Holley` or 
`Kevin Morrison`.

#### Owners with multiple attributes

To match instances of a concept type that owns multiple attributes, we can simply chain statements of `has`, label and 
variable.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has name $n, has email $email, has credential $cr; get $p;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("p").isa("person").has("name", var("n")).has("email", var("email")).has("credential", var("credential"))
//);
```
[tab:end]
</div>

#### Owners with attributes of given values

We can also match instances that own an attribute with a specific value or range of values.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $r isa record, has number < 100; get $r;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("r").isa("record").has("number", TypeQL.lt(100))
//).get("r");
```
[tab:end]
</div>

But if in this example, we still want to know the ranking of each record, we split the variable assignment and 
the condition like so.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $r isa record, has number $n; $n < 100; get $r, $n;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("r").isa("record").has("number", var("n")),
//  var("n").lt(100)
//).get("r", "n");
```
[tab:end]
</div>

### Disjunction of patterns

By default, a collection of patterns in a `match` clause constructs conjunction of patterns. To include patterns in 
the form of a disjunction, we need to wrap each pattern in `{}` and place the `or` keyword in between them.

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $p isa person, has name $n; { $n contains "Masako"; } or { n contains "Kevin"; }; get $p;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("p").isa("person").has("name", var("n")),
//  or(
//    var("n").contains("Masako"),
//    var("n").contains("Kevin")
//  )
//).get("p");
```
[tab:end]
</div>

### Instances of a direct type

The type that an instance belongs to may be a subtype of another. This means when we use `isa`, we are matching all 
direct and indirect instances of the given type. To only match the direct instances, we use `isa!` instead. 

<div class="tabs dark">

[tab:TypeQL]
```typeql
match $u isa! user;
```
[tab:end]

[tab:Java]
```java
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("u").isa("user")
//);
```
[tab:end]
</div>
<!--- Double-check the Java query isa! -->

This query matches only the direct instances of `user`. That means the instances of `person` would not be included.

### One particular instance

TypeDB assigns an auto-generated id to each instance. Although this id is generated by TypeDB solely for internal use, 
it is indeed possible to find an instance with its TypeDB id.
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
//TypeQLMatch.Filtered query = TypeQL.match(
//  var("x").iid("0x966e80018000000000000000")
//).get("x");
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
//TypeQLMatch query = TypeQL.match(
//  var("x").isa("person"), 
//  var("y").isa("person"),
//  TypeQL.not(var("x").is(var("y")))
//);
```
[tab:end]
</div>

### Comparators

When matching an instance of an attribute type based on its value or simply comparing two variables, the following 
comparators may be used: `=`, `!=`, `>`, `>=`, `<` and `<=`.

## Complex queries

By arranging statements together, we can express more complex pattern scenarios and their corresponding data.

![Pattern structure](../../images/query/pattern-structure.png)

1. **Statement**: simplest possible arrangement — a single basic building block
   as [explained above](#query-pattern-anatomy).
2. **Conjunction**: a set of patterns where to satisfy a match, **all** patterns must be matched. We use
   conjunctions by default just by separating the partaking patterns with semi-colons `;`.
3. **Disjunction**: a set of patterns where to satisfy a match, **at least one** pattern must be matched. We form  
   disjunctions by enclosing the partaking patterns within curly braces `{}` and interleaving them with
   the `or` keyword.
4. **Negation**: defines a conjunctive pattern that explicitly defines conditions **not** to be met. We form
   negations by defining the pattern of interest inside a `not {};` block.

To better illustrate the possibilities, we will now look at an example of a more complex pattern.

![Example pattern](../../images/query/example-pattern.png)

The pattern above describes pairs of instances of `person` who are both have permission to access the same file with
a filepath of `README.md`.
The pattern additionally specifies the access to be either `modify_file` or `view_file`, and any of them to not be
named `Masako Holley`.
Additionally, the pattern asks to fetch the `name` of each of the people in the pair.

The pattern is a conjunction of four different pattern types:
- **Conjunction 1** specifies the variables for people, their names, action and file that has filepath `README.md`,
  specifies their types.
- **Disjunction** specifies that the actions of interest are either `modify_file` or `view_file`.
- **Negation 1** specifies that person 1 shall not have name `Masako Holley`.
- **Negation 2** specifies that person 2 shall not have name `Masako Holley`.
- **Conjunction 2** defines the pattern requiring the file to have access that we specified earlier, and both
  person to have a permission to this access type of this file.

<!---
```typeql
match

$p1 isa person, has name $pn1;
$p2 isa person, has name $pn2;
$ac isa action;
$f isa file, has filepath "README.md";
{$ac has name "modify_file";} or {$ac has name "view_file";};
not {$p1 has name "Masako Holley";};
not {$p2 has name "Masako Holley";};
$a($f, $ac) isa access;
$pe1($p1, $a) isa permission;
$pe2($p2, $a) isa permission;
```
-->

## How to Send a Query

The easiest way to send a query to the TypeDB server is to use TypeDB Studio to 
[do so](../../02-clients/01-studio.md#write--read-data).

Alternatively, you can use any other [client](../02-dev/04-clients.md) to handle server connection, sessions, 
transactions, etc.

Among the list of clients there are TypeDB drivers for different programming languages. Sending a query in one of those
should be as easy as calling a function. But it might require additional efforts to control session and transaction.
For example, let's see how to send a query in some of the most popular programming languages:

- [Java](../../02-clients/03-java.md): Executing a query that contains a `match` clause, is as simple as calling the 
  [`query().match()`](../../02-clients/03-java.md#api-reference) method on a transaction and passing the query object 
  to it.
- [Node.js](../../02-clients/05-nodejs.md): Executing a query that contains a `match` clause, is as simple as 
  passing the TypeQL(string) query to the `query().match()` function available on the 
  [`transaction`](../../02-clients/05-nodejs.md#api-reference) object.
- [Python](../../02-clients/04-python.md): Executing a query that contains a `match` clause, is as simple as  
  passing the TypeQL(string) query to the `query().match()` method available on the
  [`transaction`](../../02-clients/04-python.md#api-reference) object.
