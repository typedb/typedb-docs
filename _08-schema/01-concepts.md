---
title: Concepts
keywords: schema
tags: [graql]
summary: "How a Grakn Schema is defined."
permalink: /docs/schema/concepts
---

## Define
As the name suggests, the `define` keyword is used to develop the [schema](/docs/schema/overview) which represents the dataset stored in a Grakn knowledge graph. We use `define` to add new entities, relationships, attributes and rules to the schema.

When defining the schema in a single `schema.gql` file, the keyword `define` needs to be included only once at the very top.

`define` can also be used in the [interactive mode of the Grakn Console]() as well as the Grakn Clients [Java](/docs/client-api/java), [Python](/docs/client-api/python) and [Node.js](/docs/client-api/nodejs).

<div class="alert">
[Important]
Don't forget to `commit` after executing a `define` statement. Otherwise, anything you have defined will NOT be committed to the original keyspace that is running on the Grakn server.
When using one of the Grakn clients, to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the [interactive mode of Grakn Console](), we use the `commit` command.
</div>


## Entity
An entity is a thing with a distinct existence. For example, `organisation`, `company` and `person`. The existence of each of these entities is independent of any other concept in the domain.

### Defining an entity
To define a new entity, we use the `sub` keyword followed by `entity`.

<div class="tabs">

[tab:Graql]

```graql
define

person sub entity,
  has name;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("person").sub("entity").has("name")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define person sub entity, has name;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define person sub entity, has name;")
transaction.commit()
```
[tab:end]
</div>

### Assigning an attribute to an entity
An entity can be assigned any number of attributes. To do so, we use the `has` keyword followed by the attribute's label.

<div class="tabs">

[tab:Graql]
```graql
define

person sub entity,
  has name,
  has forename
  has surname
  has middle-name;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("person").sub("entity").has("name").has("forename").has("surname").has("middle-name")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define person sub entity, has name, has forename, has surname, has middle-name;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define person sub entity, has name, has forename, has surname, has middle-name;")
transaction.commit()
```
[tab:end]
</div>

To assign a unique attribute to an entity, we use the `key` keyword followed by the attribute's label.

<div class="tabs">

[tab:Graql]
```graql
define

person sub entity,
    key email;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("person").sub("entity").key("email")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define person sub entity, key email;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define person sub entity, key email;")
transaction.commit()
```
[tab:end]
</div>

This guarantees `email` to have a unique value for all instances of `person`.


<div class="alert">
[Note]
Although the attributes above have been assigned to the `person` entity, they are yet to be defined. We will soon learn how to [define an attribute](#defining-an-attribute).
</div>


### Entity to play a role
An entity can play a role in a relationship. To define the role played by an entity, we use the `plays` keyword followed by the role's label.

<div class="tabs">

[tab:Graql]
```graql
define

person sub entity,
  plays employee;

company sub entity,
  plays employer;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("person").sub("entity").plays("employee"),
  label("company").sub("entity").plays("employer"),
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define person sub entity, plays employee; company sub entity, plays employer;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define person sub entity, plays employee; company sub entity, plays employer;")
transaction.commit()
```
[tab:end]
</div>

<div class="alert">
[Note]
The relationship that relates to the roles `employer` and `employee` jas not yet been defined. We will soon learn how to [define a relationship](#defining-a-relationship).
</div>

### Subtyping an entity
An entity can be defined to inherit another entity. Let's look at an example of subtyping the `organisation` entity.

<div class="tabs">

[tab:Graql]
```graql
define

organisation sub entity,
  plays owner,
  plays property,
  plays employer,
  has name;

company sub organisation;

university sub organisation,
  has rank;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("organisation").sub("entity").plays("owner").plays("property").plays("employer").has("name"),
  label("company").sub("organisation"),
  label("university").sub("organisation").has("rank")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define organisation sub entity, plays owner, plays property, plays employer, has name; company sub organisation; university sub organisation, has rank;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query(define organisation sub entity, plays owner, plays property, plays employer, has name; company sub organisation; university sub organisation, has rank;)
```
[tab:end]
</div>

As you can see in the example above, when defining entities, what follows the `sub` keyword can be a label previously given to another entity. In this example, `company` and `university` are both considered to be subtypes of `organisation` and so are defined that way. By subtyping a parent entity, the children inherit all attributes owned and roles played by their parent. Therefore, although not defined explicitly, we are right to assume that both `company` and `university` have a `name` and play the roles `owner`, `property` and `employer`. However, the attribute `rank` is only owned by a `university`.

<div class="alert">
[Note]
The relationships that relate to the roles `owner`, `property` and `employer` have not been defined in the example above. We will soon learn how to [define a relationship](#defining-a-relationship). Similarly, the attributes `name` and `rank` are yet to be defined. We will soon learn how to [define an attribute](#defining-an-attribute) as well.
</div>

The ability to subtype entities not only helps mirror the reality of the dataset as perceived in the real world but also enables [automated reasoning using type hierarchies](...).

#### Defining an abstract entity
There may be scenarios where a parent entity is only defined for other entities to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `is-abstract` keyword. Let's say in the example above, we would like to define the `organisation` entity type to be abstract. By doing so, we're indicating that no data instances of the `organisation` entity are allowed to be created.

<div class="tabs">

[tab:Graql]
```graql
define

organisation sub entity is-abstract;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("organisation").sub("entity").isAbstract()
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define organisation sub entity is-abstract;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define organisation sub entity is-abstract;")
transaction.commit()
```
[tab:end]

</div>

## Relationship
A relationship describes how two or more things are in some way connected to each other. For example, `loan` and `employment`. Each of these relationships must relate to roles that are played by something else in the domain. In other words, relationships are dependent on the existence of at least two other things.

### Defining a relationship
To define a new relationship, we use the `sub` keyword followed by `relationship`.

```graql
define

employment sub relationship;
```

To complete the definition of a relationship, its roles must be determined. To do so, we use the `relates` keyword followed by the role's label.

<div class="tabs">

[tab:Graql]
```graql
define

employment sub relationship,
  relates employee,
  relates employer;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("employment").sub("relationship").relates("employee").relates("employer")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define employment sub relationship, relates employee, relates employer;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define employment sub relationship, relates employee, relates employer;")
transaction.commit()
```
[tab:end]
</div>

The roles `employee` and `employer` are now ready to be played by other elements in the schema.

### Roleplayers of a relationship
Entities, attributes, and even other relationships can play a role in a relationship. To do this we make use of the `plays` keyword followed by the role's label.

We have already seen how to [define an entity to play a role](#defining-an-entity-to-play-a-role) and will soon learn how to [define an attribute to play a role](#defining-an-attribute-to-play-a-role) as well. But what about a relationship that plays a role in another relationship?

### Defining a relationship to play a role
Let's go through a simple example of how a relationship can play a role in another relationship.

<div class="tabs">

[tab:Graql]
```graql
define

loan sub relationship,
  relates lender,
  relates recipient,
  plays subject;

legal-constraint sub relationship,
  relates subject,
  relates legality;

bank sub entity,
  plays lender;

person sub entity,
  plays recipient;

terms-n-conditions sub entity,
  plays legality;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("loan").sub("relationship").relates("lender").relates("recipient")
  .plays("subject"),
  label("legal-constraint").sub("relationship").relates("subject").relates("legality"),
  label("bank").sub("entity").plays("lender"),
  label("person").sub("entity").plays("recipient"),
  label("terms-n-conditions").sub("entity").plays("legality")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define loan sub relationship, relates lender, relates recipient, plays subject; legal-constraint sub relationship, relates subject, relates legality; bank sub entity, plays lender; person sub entity, plays recipient; terms-n-conditions sub entity, plays legality;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define loan sub relationship, relates lender, relates recipient, plays subject; legal-constraint sub relationship, relates subject, relates legality; bank sub entity, plays lender; person sub entity, plays recipient; terms-n-conditions sub entity, plays legality;")
transaction.commit()
```
[tab:end]
</div>

The example can be read in plain english as follows.
: In a `loan`, the `lender` is a `bank` and the `recipient` isa `person`. The `loan` is the `subject` of a `legal-constraint` where `terms-n-conditions` is the `legality`.

### A relationship with many roleplayers
A relationship can relate to any number of roles. The example below illustrates a three-way relationship.

<div class="tabs">

[tab:Graql]
```graql
define

mortgage sub relationship,
  relates debtor,
  relates lender,
  relates subject;

person sub entity,
  plays debtor;

bank sub entity,
  plays lender;

house sub entity,
  plays subject;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("mortgage").sub("relationship").relates("debtor").relates("lender")
  .relates("subject"),
  label("person").sub("entity").plays("debtor"),
  label("bank").sub("entity").plays("lender"),
  label("person").sub("entity").plays("recipient"),
  label("house").sub("entity").plays("legality")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define mortgage sub relationship, relates debtor, relates lender, relates subject; person sub entity, plays debtor; bank sub entity, plays lender; house sub entity, plays subject;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define mortgage sub relationship, relates debtor, relates lender, relates subject; person sub entity, plays debtor; bank sub entity, plays lender; house sub entity, plays subject;")
transaction.commit()
```
[tab:end]
</div>

The example can be read in plain English as follows.
: In a `mortgage`, a `person` is the `debtor`, a `bank` is the `lender` and the `house` is the `subject`.

### Assigning attributes to a relationship
A relationship can be assigned any number of attributes. To do so, we use the `has` keyword followed by the attribute's label.

<div class="tabs">

[tab:Graql]
```graql
define

employment sub relationship,
  has job-title,
  relates employer,
  relates employee;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("employment").sub("relationship").relates("employer").relates("employee").has("job-title")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define employment sub relationship, has job-title, relates employer, relates employee;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define employment sub relationship, has job-title, relates employer, relates employee;")
transaction.commit()
```
[tab:end]
</div>

To assign a unique attribute to a relationship, we use the `key` keyword followed by the attribute's label.

<div class="tabs">

[tab:Graql]
```graql
define

employment sub relationship,
  key reference-id,
  relates employer,
  relates employee;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("employment").sub("relationship").key("reference-id").relates("employer").relates("employee")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define employment sub relationship, key reference-id, relates employer, relates employee;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define employment sub relationship, key reference-id, relates employer, relates employee;")
transaction.commit()
```
[tab:end]
</div>

This guarantees `reference-id` to have a unique value for all instances of `employment`.

<div class="alert">
[Note]
Although the attributes above have been assigned to `employment`, they are yet to be defined. We will soon learn how to [define an attribute](#defining-an-attribute).
</div>

### Subtyping a relationship
A relationship can be defined to inherit another relationship. Let's take a look at an example of subtyping an `affiliation` relationship.

<div class="tabs">

[tab:Graql]
```graql
define

affiliation sub relationship,
  key reference-id,
  relates party;

membership sub affiliation,
  relates member as party,
  relates group as party;

employment sub membership,
  relates employee as member,
  relates employer as group,
  has job-title;

board-membership sub membership,
  relates board-member as member,
  relates board as group;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("affiliation").sub("relationship").relates("party").key("reference-id"),
  label("member").sub("party"),
  label("group").sub("party"),
  label("membership").sub("affiliation").relates("member").relates("group"),
  label("employee").sub("member"),
  label("employer").sub("group"),
  label("employment").sub("membership").relates("employee").relates("employer")
  .has("job-title"),
  label("board-member").sub("member"),
  label("board").sub("group"),
  label("board-membership").sub("membership").relates("board-member").relates("board")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define affiliation sub relationship, key reference-id, relates party; membership sub affiliation, relates member as party, relates group as party; employment sub membership, relates employee as member, relates employer as group, has job-title; board-membership sub membership, relates board-member as member, relates board as group;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define affiliation sub relationship, key reference-id, relates party; membership sub affiliation, relates member as party, relates group as party; employment sub membership, relates employee as member, relates employer as group, has job-title; board-membership sub membership, relates board-member as member, relates board as group;")
transaction.commit()
```
[tab:end]
</div>

As you can see in the example above, when defining relationships, what follows the `sub` keyword can be a label previously given to another relationship. In this case, `employment` and `board-membership` are both considered to be subtypes of `membership` which is itself a subtype of `affiliation`. By subtyping a parent relationship, the children inherit all attributes owned and roles related to and played by their parent. Therefore, although not defined explicitly, we are right to assume that both `employment` and `board-membership` relate to the roles `member`, `group` and `party` and own the key attribute `reference-id`.

<div class="alert">
[Note]
Although the attributes above have been assigned to `affiliation` and `employment`, they are yet to be defined. We will soon learn how to [define an attribute](#defining-an-attribute).
</div>

Note the use of the `as` keyword. This is necessary to determine the correspondence between the role of the child and that of the parent.

<div class="alert">
[Important]
All roles defined to relate to the parent relationship must also be defined to relate to the child relationship using the `as` keyword.
</div>

The ability to subtype relationships not only helps mirror the reality of the dataset as perceived in the real world but also enables [automated reasoning using type hierarchies](...).

#### Defining an abstract relationship
There may be scenarios where a parent relationship is only defined for other relationships to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `is-abstract` keyword. Let's say in the example above, we would like to define the `affiliation` relationship type to be abstract. By doing so, we're indicating that no data instances of the `affiliation` relationship are allowed to be created.

<div class="tabs">

[tab:Graql]
```graql
define

affiliation sub relationship is-abstract,
  relates party;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("affiliation").sub("relationship").isAbstract().relates("party")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define affiliation sub relationship is-abstract, relates party;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define affiliation sub relationship is-abstract, relates party;")
transaction.commit()
```
[tab:end]

</div>


## Attribute
An attribute is a piece of information that determines the property of an element in the domain. For example, `name`, `language` and `age`. These attributes can be assigned to anything that needs them as a property.

### Defining an attribute
To define a new attribute, we use the `sub` keyword followed by `attribute`, `datatype` and, at last, the type of the desired value.

<div class="tabs">

[tab:Graql]
```graql
define

name sub attribute datatype string;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("name").sub("attribute").datatype(AttributeType.DataType.STRING)
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define name sub attribute datatype string;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define name sub attribute datatype string;")
transaction.commit()
```
[tab:end]
</div>

This attribute is now ready to be assigned to any other defined type in the schema.

The data types available in a Grakn knowledge graph are:
- long: a 64-bit signed integer.
- double: a double-precision floating point number, including a decimal point.
- string: enclosed in double `"` or single `'` quotes
- boolean: `true` or `false`
- date: a date or date-time in ISO 8601 format

**The same attribute can belong to multiple `thing`s.**.

<div class="tabs">

[tab:Graql]
```graql
define

colour sub attribute datatype string;

car sub entity,
  has colour;

bicycle sub entity,
  has colour;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("colour").sub("attribute").datatype(AttributeType.DataType.STRING),
  label("car").sub("entity").has("colour"),
  label("bicycle").sub("entity").has("colour")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define colour sub attribute datatype string; car sub entity,  has colour; bicycle sub entity, has colour;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define colour sub attribute datatype string; car sub entity,  has colour; bicycle sub entity, has colour;")
transaction.commit()
```
[tab:end]
</div>

<div class="alert">
[Important]
In this example, the attribute `colour` with the value of, for instance `"red"`, exists only once in the knowledge graph and shared among any number of instances that may own it. This is useful when we need to query the knowledge graph for anything that has the `colour` attribute with value `"red"`. In this case, we would get all the red cars and bicycles as the answer.
</div>

**A `thing` can have any number of the same attribute that holds different values.** In other words, a `thing` can have a many-to-many relationship with its attributes.

<div class="tabs">

[tab:Graql]
```graql
genre sub attribute datatype string;

movie sub entity,
  has genre;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("genre").sub("attribute").datatype(AttributeType.DataType.STRING),
  label("movie").sub("entity").has("genre"),
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("genre sub attribute datatype string; movie sub entity, has genre;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("genre sub attribute datatype string; movie sub entity, has genre;")
transaction.commit()
```
[tab:end]
</div>

An instance of a `movie` can have one instance of `genre`, or two or three, ... you get the idea.

We have already seen how to [assign an attribute to an entity](#assigning-an-attribute-to-an-entity) and similarly to [assign an attribute to a relationship](#assigning-an-attribute-to-a-relationship). But what about assigning an attribute, an attribute of its own?

### Assigning an attribute to another attribute
Like entities and relationships, attributes can also own an attribute of their own. To do this, we use the 'has' keyword followed by the attribute's label.

<div class="tabs">

[tab:Graql]
```graql
define

text sub attribute datatype string,
  has language;

language sub attribute datatype string;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("text").sub("attribute").datatype(AttributeType.DataType.STRING).has("language"),
  label("language").sub("attribute").datatype(AttributeType.DataType.STRING)
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define text sub attribute datatype string, has language; language sub attribute datatype string;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define text sub attribute datatype string, has language; language sub attribute datatype string;")
transaction.commit()
```
[tab:end]
</div>

In this example, attribute `text` can be owned by, for instance, an `email` relationship. What this example aims to showcase is that the `text` attribute, besides its own value, owns an attribute named `language` which holds the name of the language the text is in.

### Defining an attribute to play a role
An attribute can play a role in a relationship. To define the role played by an attribute, we use the `plays` keyword followed by the role's label.

<div class="tabs">

[tab:Graql]
```graql
define

word sub attribute datatype string,
  plays originated;

language sub entity,
  plays origin;

origination sub relationship,
  relates origin,
  relates originated;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("word").sub("attribute").datatype(AttributeType.DataType.STRING).plays("originated"),
  label("language").sub("entity").plays("origin"),
  label("origination").sub("relationship").relates("origin").relates("originated")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define word sub attribute datatype string,plays originated;language sub entity,plays origin;origination sub relationship,relates origin,relates originated;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define word sub attribute datatype string,plays originated;language sub entity,plays origin;origination sub relationship,relates origin,relates originated;")
transaction.commit()
```
[tab:end]
</div>

The definition above contains also a relationship. We learned earlier how to [define a relationship](#defining-a-relationship).

### Subtyping an attribute
An attribute can be defined to inherit another attribute.

<div class="tabs">

[tab:Graql]
```graql
define

name sub attribute datatype string;
forename sub name;
surname sub name;
middle-name sub name;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("name").sub("attribute").datatype(AttributeType.DataType.STRING),
  label("forename").sub("name"),
  label("surname").sub("name"),
  label("middle-name").sub("name")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define name sub attribute datatype string; forename sub name; surname sub name; middle-name sub name;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define name sub attribute datatype string; forename sub name; surname sub name; middle-name sub name;")
transaction.commit()
```
[tab:end]
</div>

What this definition means is that `forename`, `surname` and `middle-name` are all inherently subtypes of `name`. They inherit the datatype of `name` as well as its contextuality.

The ability to subtype attributes not only helps mirror the reality of our dataset but also enables [automated reasoning using type hierarchies](...).

#### Defining an abstract relationship
There may be scenarios where a parent attribute is only defined for other attributes to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `is-abstract` keyword. Let's say in the example above, we would like to define the `name` attribute type to be abstract. By doing so, we are indicating that no data instances of the `name` attribute are allowed to be created.

<div class="tabs">

[tab:Graql]
```graql
define

name sub attribute is-abstract datatype string;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("name").sub("attribute").datatype(AttributeType.DataType.STRING),
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("define name sub attribute is-abstract datatype string;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("define name sub attribute is-abstract datatype string;")
transaction.commit()
```
[tab:end]
</div>

## Undefine
As the name suggests, the `undefine` keyword is used to remove the definition of a type from the schema.

<div class="alert">
[Important]
Don't forget to `commit` after executing an `undefine` statement. Otherwise, anything you have undefined will NOT be committed to the original keyspace that is running on the Grakn server.
When using one of the Grakn clients, to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the [interactive mode of Grakn Console](), we use the `commit` command.
</div>

### Undefining an attribute's association
To undefine the association a `thing` has with an attribute we use the following syntax.

<div class="tabs">

[tab:Graql]
```graql
undefine person has name;
```
[tab:end]

[tab:Java]
```java
Graql.undefine(
  label("person").has("name")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("undefine person has name;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("undefine person has name;")
transaction.commit()
```
[tab:end]
</div>

The query above, removes the attribute `name` from the entity `person`.

<div class="alert">
[Important]
It's important to note that `underfine [label] sub [type] has [attribute's label];` undefines the `label` itself, rather than the attribute's association.
</div>

### Undefining a relationship
Given the dependent nature of relationships, before undefining the relationship itself, we must first undefine all roles that it relates to. Given an [earlier employment example](#subtyping-a-relationship), we would undefine the employment relationship, as shown below.

<div class="tabs">

[tab:Graql]
```graql
undefine
  employment relates employer, relates employee;
  employer sub group;
  employee sub member;
  employment sub membership;
```
[tab:end]

[tab:Java]
```java
Graql.undefine(
  label("employment").relates("employer").relates("employee"),
  label("employer").sub("group"),
  label("employee").sub("member"),
  label("employment").sub("membership")
);

transaction.execute(query.toString());
transaction.commit();
```
[tab:end]

[tab:Javascript]
```javascript
await transaction.query("undefine employment relates employer, relates employee; employer sub group; employee sub member; employment sub membership;");
transaction.commit();
```
[tab:end]

[tab:Python]
```python
transaction.query("undefine employment relates employer, relates employee; employer sub group; employee sub member; employment sub membership;")
transaction.commit()
```
[tab:end]
</div>

### Underfining a Supertype
When the `thing` to be undefined is a supertype to something else, we must first undefine all its subtypes before undefining the supertype itself.

## Summary
We learned that a Grakn schema is essentially a collection of Entities, Relationships, and Attributes - what we call the Grakn Concepts. The modularity of these concepts and how they interact with one another is what allows us to model the schema in a way to represent the true nature of any dataset in any domain.

In the next section, we will learn about one last addition to the schema - [Graql Rules](/docs/schema/rules).
