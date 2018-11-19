---
title: Concepts
keywords: schema
tags: [graql]
summary: "How a Grakn Schema is defined."
permalink: /docs/schema/concepts
---

## Define
As the name suggests, the `define` keyword is used to define elements of the schema. These elements may be substances of Schema Concepts or [Rules](/docs/schema/rules).

When defining the schema in a single `schema.gql` file, the keyword `define` needs to be included only once at the very top.

`define` can also be used in the [Grakn Console's interactive mode] and Grakn [Java](...), [Python](...) and [Node.js](...) Clients.


## Entity
An entity is a thing with a distinct existence. For example, `organisation`, `company` and `person`. The existence of each of these entities is independent of any other element in the domain.

### Defining an entity
To define a new entity, we use the `sub` keyword followed by `entity`.

```graql
define

person sub entity;
```

### Assigning an attribute to an entity
An entity can be assigned any number of attributes. To do so, we use the `has` keyword followed by the attribute's label.

```graql
define

person sub entity,
  has name,
  has forename
  has surname
  has middle-name;
```

To assign a unique attribute to an entity, we use the `key` keyword followed by the attribute's label.

```graql
define

person sub entity,
    key email;
```
This guarantees `email` to have a unique value for all instances of `person`.


Note that although these attributes have been assigned to `person`, they are yet to be defined. We will soon learn how to [define an attribute](#defining-an-attribute).

### Entity to play a role
An entity can play a role in a relationship. To define the role played by an entity, we use the `plays` keyword followed by the role's label.

```graql
define

person sub entity,
  plays employee;

company sub entity,
  plays employer;

employment sub relationship,
  relates employee,
    relates employer;
```

The definition above contains also a relationship. We will soon learn how to [define a relationship](#defining-a-relationship).

### Subtyping an entity
An entity can be defined to inherit another entity. Let's go through an example of subtyping the `organisation` entity.

```graql
define

organisation sub entity,
  plays owner,
  plays property,
  has name;

company sub organisation,
  plays employer;

university sub organisation;
```

As you can see in the example above, when defining entities, what follows the `sub` keyword can be the label that is previously given to another entity. In this example, `company` and `university` are both considered to be subtypes of `organisation` and so are defined that way. By subtyping a parent entity, the children inherit all attributes owned and roles played by their parent. Therefore, although not defined explicitly, we are right to assume that both `company` and `university` have a `name` and play the roles `owner` and `property`.

The ability to subtype entities not only helps mirror the reality of our dataset but also enables [automated reasoning using type hierarchies](...).


## Relationship
A relationship describes how two or more things are in some way connected to each other. For example, `loan` and `employment`. Each of these relationships must relate to something else in the domain. In other words, relationships are dependent on the existence of at least two other things.

### Defining a relationship
To define a new relationship, we use the `sub` keyword followed by `relationship`.

```graql
define

employment sub relationship;
```

To complete the definition of a relationship, its roles must be determined. To do so, we use the `relates` keyword followed by the role's label.

```graql
define

employment sub relationship,
  relates employee,
  relates emplyer;
```

The roles `employee` and `employer` are now ready to be played by other elements in the schema.

### Roleplayers of a relationship
Entities, attributes, and even other relationships can play a role in a relationship. To do this we make use of the `plays` keyword followed by the role's label.

We have already seen how to [define an entity to play a role](#defining-an-entity-to-play-a-role) and will soon learn how to [define an attribute to play a role](#defining-an-attribute-to-play-a-role). But what about a relationship that plays a role in another relationship?

### Defining a relationship to play a role
Let's go through a simple example of how a relationship can play a role in another relationship.

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

The diagram below illustrates what has been defined in the example above.

<<insert diagram>>

### A relationship with many roleplayers
A relationship can relate to any number of roles. The example below illustrates a three-way relationship.

```graql
define

mortgage sub relationship,
  relates debtor,
    relates lender,
    relates subject;

bank sub entity,
  plays lender;

person sub entity,
  plays debtor;

house sub entity,
  plays subject;
```

The diagram below illustrates what has been defined the example above.

<<insert diagram>>

### Assigning attributes to a relationship
A relationship can be assigned any number of attributes. To do so, we use the `has` keyword followed by the attribute's label.

```graql
define

employment sub relationship,
  has job-title
    relates emplyer,
    relates employee;
```

Note that although the attribute `job-title` has been assigned to `employment`, they are yet to be defined. We will soon learn how to [define an attribute](#defining-an-attribute).

To assign a unique attribute to a relationship, we use the `key` keyword followed by the attribute's label.

```graql
define

employment sub relationship,
    key reference-id;
```

This guarantees `reference-id` to have a unique value for all instances of `employment`.

### Subtyping a relationship
An entity can be defined to inherit another entity. Let's go through an example of subtyping an `organisation` entity.

```graql
define

affiliation sub relationship,
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

As you can see in the example above, when defining relationships, what follows the `sub` keyword can be the label given to another relationship. In this case, `employment` and `board-membership` are both considered to be subtypes of `membership` which is itself a subtype of `affiliation`. By subtyping a parent relationship, the children inherit all attributes owned and roles related to their parent. Therefore, although not defined explicitly, we are right to assume that both `employment` and `board-membership` relate to roles `member`, `group` and `party`.

Note the use of the `as` keyword. This is necessary to determine the correspondence between the parent's and child's role.

The ability to subtype relationships not only helps mirror the reality of our dataset but also enables [automated reasoning using type hierarchies](...).

## Attribute
An attribute is a piece of information that determines the property of an element in the domain. For example, `name`, `language` and `age`. These attributes can be assigned to anything that needs them as a property.

### Defining an attribute
To define a new attribute, we use the `sub` keyword followed by `attribute datatype` and the type of the desired value.

```graql
define

name sub attribute datatype string;
```

This attribute is now ready to be assigned to any other element in the schema.

The data types available in a Grakn knowledge graph are as follows:
- long: a 64-bit signed integer.
- double: a double-precision floating point number, including a decimal point.
- string: enclosed in double `"` or single `'` quotes
- boolean: `true` or `false`
- date: a date or date-time in ISO 8601 format

**The same attribute can belong to multiple `thing`s.** Let's look at an example.

```graql
define

color sub attribute datatype string;

car sub entity,
  has color;

bicylce sub entity,
  has color;
```

Note that, in this example, the attribute `color` with the same value, for instance `"red"`, exists only once in the knowledge graph and shared among anything that owns it. This is useful when we need to query the knowledge graph for anything that has the `color` attribute of `"red"`. In this case, we would get all the red cars and bicycles as the answer.

**A `thing` can have any number of the same attribute that holds different values.** In other words, a `thing` can have a many to many relationship with its attributes. Let's look at an example.

```graql
genre sub attribute datatype string;

movie sub entity,
  has genre;
```

A `movie` can have one `genre`, or two or three.

We have already seen how to [assign an attribute to an entity](#assigning-an-attribute-to-an-entity) and similarly to [assign an attribute to a relationship](#assigning-an-attribute-to-a-relationship). But what about assigning an attribute to another attribute of its own?

### Assigning an attribute to another attribute
Like entities and relationships, attributes can also own an attribute of their own. To do this, we use the 'has' keyword followed by the attribute's label.

```graql
text sub attribute datatype string,
  has word;

word sub attribute datatype string,
  has position;

position sub attribute datatype long;
```

### Defining an attribute to play a role
An attribute can play a role in a relationship. To define the role played by an attribute, we use the `plays` keyword followed by the role's label.

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

The definition above contains also a relationship. Previously we learned how to [define a relationship](#defining-a-relationship).

### Subtyping an attribute
An attribute can be defined to inherit another attribute. Let’s go through an example of subtyping a `name` attribute.

```graql
name sub attribute datatype string;
forename sub name;
surname sub name;
middle-name sub name;
```

What this definition means is that `forename`, `surname` and `middle-name` are all inherently subtypes of `name`. They inherit the datatype of `name` as well its contextuality.

The ability to subtype attributes not only helps mirror the reality of our dataset but also enables [automated reasoning using type hierarchies](...).

## Undefine
As the name suggests, the `undefine` keyword is used to define an element of the schema. These elements may be substances of Schema Concepts or [Rules](/docs/schema/rules).

`undefine` can also be used in the [Grakn Console's interactive mode] and Grakn [Java](...), [Python](...) and [Node.js](...) Clients.

Here are two examples of how a schema element can be undefined:

```graql
undefine person sub entity;
```

The Graql code above removes the type `person` from the schema.

```graql
undefine person has name;
```
The Graql code above removes the association between the attribute `name` and the type `person` from the schema.

## Summary
We learned that a Grakn schema is essentially a collection of Entities, Relationships, and Attributes - what we call the Grakn Concepts. The modularity of these concepts and how they interact with one another is what allows us to model the schema in a way to represent the true nature of any dataset in any domain.

In the next section, we will learn about one last addition to the schema - [Graql Rules](/docs/schema/rules).