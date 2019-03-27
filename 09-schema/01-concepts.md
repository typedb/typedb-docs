---
pageTitle: Schema Concepts
keywords: graql, schema, type hierarchy, concept, define
longTailKeywords: graql schema, graql define query, graql type hierarchy, graql concepts, graql define entity, graql define relation, graql define attribute, graql schema definition
Summary: A comprehensive guide on defining Schema Concepts in Grakn.
---

<div class = "note">
[Note]
**For those developing with Client [Java](../03-client-api/01-java.md)**: Executing `define` and `undefine` queries, is as simple as calling the [`withTx().execute()`](../03-client-api/01-java.md#client-api-method-eagerly-execute-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](../03-client-api/03-nodejs.md)**: Executing `define` and `undefine` queries, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/03-nodejs.md#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](../03-client-api/03-nodejs.md#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](../03-client-api/02-python.md)**: Executing `define` and `undefine` queries, is as simple as passing the Graql(string) query to the [`query()`](../03-client-api/02-python.md#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](../03-client-api/02-python.md#client-api-title-transaction) object.
</div>

<!-- !!! synced with codeKeywordsToLink -->
## Define
As the name suggests, we use the `define` keyword to develop the [schema](../09-schema/00-overview.md) which represents the dataset stored in a Grakn knowledge graph. We use `define` to add new entities, relations, attributes and rules to the schema.

When defining the schema in a single `schema.gql` file, the keyword `define` needs to be included only once at the very top.

We can also use the `define` keyword in the interactive mode of the [Grakn Console](../02-running-grakn/02-console.md) as well as the Grakn Clients [Java](../03-client-api/01-java.md#client-api-method-manipulate-the-schema-programatically), [Python](../03-client-api/02-python.md#client-api-method-lazily-execute-a-graql-query) and [Node.js](../03-client-api/03-nodejs.md#client-api-method-lazily-execute-a-graql-query).

<div class="note">
[Important]
Don't forget to `commit` after executing a `define` query. Otherwise, anything you have defined is NOT committed to the original keyspace that is running on the Grakn server.
When using one of the Grakn Clients, to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the Grakn Console, we use the `commit` command.
</div>

## Entity
An entity is a thing with a distinct existence in the domain. For example, `organisation`, `location` and `person`. The existence of each of these entities is independent of any other concept in the domain.

### Define an entity
To define a new entity, we use the `sub` keyword followed by `entity`.

<div class="tabs dark">

[tab:Graql]

```graql
define

person sub entity;
```

[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("person").sub("entity")
);
```

[tab:end]
</div>

<div class="note">
[Note]
Although, in the example above, we have assigned the `full-name` attribute to the `person` entity, it is yet to be defined. We soon learn how to [define an attribute](#define-an-attribute).
</div>

### Assign an attribute to an entity
We can assign any number of attributes to an entity. To do so, we use the `has` keyword followed by the attribute's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

person sub entity,
  has full-name,
  has nickname,
  has gender;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("person").sub("entity").has("full-name").has("nickname").has("gender")
);
```

[tab:end]
</div>

To assign a unique attribute to an entity, we use the `key` keyword followed by the attribute's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

person sub entity,
    key email;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("person").sub("entity").key("email")
);
```

[tab:end]
</div>

This guarantees that no instances of `email` may hold the same value among all instances of `person`.

<div class="note">
[Note]
Although, in the example above, we have assigned attributes to the `person` entity, they are yet to be defined. We soon learn how to [define an attribute](#define-an-attribute).
</div>


### Entity to play a role
An entity can play a role in a relation. To define the role played by an entity, we use the `plays` keyword followed by the role's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

person sub entity,
  plays employee;

organisation sub entity,
  plays employer;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("person").sub("entity").plays("employee"),
  type("organisation").sub("entity").plays("employer")
);
```

[tab:end]
</div>

<div class="note">
[Note]
We are yet to define the relation that relates to the roles `employer` and `employee`. We soon learn how to [define a relation](#define-a-relation).
</div>

### Subtype an entity
We can define an entity to inherit all attributes owned and roles played by another entity. Let's look at an example of subtyping the `media` entity.

<div class="tabs dark">

[tab:Graql]
```graql
define

post sub entity,
  plays replied-to,
  plays tagged-in,
  plays reacted-to;

comment sub post,
  has content,
  plays attached-to;

media sub post,
  has caption,
  has file,
  plays attached;

video sub media;

photo sub media;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("post").sub("entity").plays("replied-to").plays("tagged-in").plays("reacted-to"),
  type("comment").sub("post").has("content").plays("attached-to"),
  type("media").sub("post").has("caption").has("file").plays("attached"),
  type("video").sub("media"),
  type("photo").sub("media")
);
```

[tab:end]
</div>

As you can see in the example above, when defining entities, what follows the `sub` keyword can be a label previously given to another entity. By subtyping a parent entity, the children inherit all attributes owned and roles played by their parent.

In this example, `comment` and `media` are both considered to be subtypes of `post`. Similarly `video` and `photo` are subtypes of `media` and so are defined that way. Therefore, although not defined explicitly, we are right to assume that `comment`, `media`, `video` and `photo` all play the roles `replied-to`, `tagged-in` and `reacted-to`. However, the role `attached` and the attributes `caption` and `file` are played and owned only by the `media` entity and its subtypes. Similarly, the role `attached-to` and the attribute `content` are played and owned only by the `comment` entity.

<div class="note">
[Note]
We are yet to define the relations that relate to the roles as well as the attributes in the example above. We soon learn how to [define a relation](#define-a-relation) and [define an attribute](#define-an-attribute).
</div>

The ability to subtype entities not only helps mirror the reality of the dataset as perceived in the real world but also enables automated reasoning using type hierarchies.

### Define an abstract entity
There may be scenarios where a parent entity is only defined for other entities to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `abstract` keyword. Let's say in the example above, we would like to define both the `post` and `media` entity types to be abstract. By doing so, we are indicating that no data instances of the of these entity types are allowed to be created, leaving us only with instances of `comment`, `photo` and `video`.

<div class="tabs dark">

[tab:Graql]
```graql
define

post sub entity, abstract;

media sub post, abstract;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("post").sub("entity").isAbstract(),
  type("media").sub("post").isAbstract()
);
```

[tab:end]
</div>

## Relation
A relation describes how two or more things are in some way connected to each other. For example, `friendship` and `employment`. Each of these relations must relate to roles that are played by something else in the domain. In other words, relations are dependent on the existence of at least two other things.

### Define a relation
To define a new relation, we use the `sub` keyword followed by `relation`.

```graql
define

employment sub relation;
```

To complete the definition of a relation, we must determine the roles that it relates to. To do so, we use the `relates` keyword followed by the role's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

employment sub relation,
  relates employee,
  relates employer;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("employment").sub("relation").relates("employee").relates("employer")
);
```

[tab:end]
</div>

The roles `employee` and `employer` are now ready to be played by other concept types in the schema.

### Roleplayers of a relation
Entities, attributes, and even other relations can play a role in a relation. To do this we make use of the `plays` keyword followed by the role's label.

We have already seen how to [define an entity to play a role](#entity-to-play-a-role) and soon learn how to [define an attribute to play a role](#define-an-attribute-to-play-a-role) as well. But what about a relation that plays a role in another relation?

### Define a relation to play a role
Let's go through a simple example of how a relation can play a role in another relation.

<div class="tabs dark">

[tab:Graql]
```graql
define

friendship sub relation,
  relates friend,
  plays requested-friendship;

friend-request sub relation,
  relates requested-friendship,
  relates friendship-requester,
  relates friendship-respondent;

person sub entity,
  plays friend,
  plays friendship-requester,
  plays friendship-respondent;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("friendship").sub("relation").relates("friend").plays("requested-friendship"),
  type("friend-request").sub("relation").relates("requested-friendship").relates("friendship-requester").relates("friendship-respondent"),
  type("person").sub("entity").plays("friend").plays("friendship-requester").plays("friendship-respondent")
);
```

[tab:end]
</div>

In the example above, the `friendship` relation plays the role of the `requested-friendship` in the `friend-request` relation. The other two roleplayers in a `friend-request` are 1) the `person` who plays the `friendship-requester` role and 2) another `person` whole plays the `friendship-respondent` role.

Once the `friend-request` is accepted, then those two `person`s play the role of `friend` in the `friendship` relation.

### A relation with many roleplayers
A relation can relate to any number of roles. The example below illustrates a three-way relation.

<div class="tabs dark">

[tab:Graql]
```graql
define

reaction sub relation,
  relates reacted-emotion,
  relates reacted-to,
  relates reacted-by;

emotion sub attribute,
  datatype string,
  plays reacted-emotion;

post sub entity,
  plays reacted-to;

person sub entity,
  plays reacted-by;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("reaction").sub("relation").relates("reacted-emotion").relates("reacted-to").relates("reacted-by"),
  type("emotion").sub("attribute").datatype("string").plays("reacted-emotion"),
  type("post").sub("entity").plays("reacted-to"),
  type("person").sub("entity").plays("reacted-by")
);
```

[tab:end]
</div>

In the example above, the `reaction` relation relates to three roles:
1. `reacted-emotion` role played by an `emotion` attribute.
2. `reacted-to` role played by a `post` entity.
3. `reacted-by` role played by a `person` entity.

### Assign an attribute to a relation
We can assign any number of attributes to a relation. To do so, we use the `has` keyword followed by the attribute's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

friend-request sub relation,
  has approved-date,
  relates requested-friendship,
  relates friendship-requester,
  relates friendship-respondent;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("friend-request").sub("relation").has("approved-date").relates("requested-friendship").relates("friendship-requester").relates("friendship-respondent")
);
```

[tab:end]
</div>

To assign a unique attribute to a relation, we use the `key` keyword followed by the attribute's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

employment sub relation,
  key reference-id,
  relates employer,
  relates employee;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("employment").sub("relation").key("reference-id").relates("employer").relates("employee")
);
```

[tab:end]
</div>

This guarantees that no instances of `reference-id` may hold the same value among all instances of `employment`.

<div class="note">
[Note]
Although, in the example above, we have assigned the attributes to the `friend-request` and `employment` relations , they are yet to be defined. We soon learn how to [define an attribute](#define-an-attribute).
</div>

### Subtype a relation
We can define a relation to inherit all attributes owned, and roles related to and played by another relation. Let's take a look at an example of subtyping an `affiliation` relation.

<div class="tabs dark">

[tab:Graql]
```graql
define

location-of-everything sub relation,
  relates located-subject,
  relates subject-location;

location-of-birth sub location-of-everything,
  relates located-birth as located-subject,
  relates birth-location as subject-location;

location-of-residence sub location-of-everything,
  relates located-residence as located-subject,
  relates residence as subject-location;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("location-of-everything").sub("relation").relates("located-subject").relates("subject-location"),
  type("located-birth").sub("located-subject"),
  type("birth-location").sub("subject-location"),
  type("location-of-birth").sub("location-of-everything").relates("located-birth").relates("birth-location"),
  type("located-residence").sub("located-subject"),
  type("residence").sub("subject-location")
);
```

[tab:end]
</div>

As you can see in the example above, when defining relations, what follows the `sub` keyword can be a label previously given to another relation. By subtyping a parent relation, the children inherit all attributes owned and roles played by their parent.

In this example, `location-of-birth` and `location-of-residence` are both considered to be subtypes of `location-of-everything` and so are defined that way. Modelling these relations in this way, not only allows us to query for locations of birth and residence separately, but also allows us to query for all the associations that a given person has with a given location.

Note the use of the `as` keyword. This is necessary to determine the correspondence between the role of the child and that of the parent.

<div class="note">
[Important]
All roles defined to relate to the parent relation must also be defined to relate to the child relation using the `as` keyword.
</div>

The ability to subtype relations not only helps mirror the reality of the dataset as perceived in the real world but also enables automated reasoning using type hierarchies.

#### Define an abstract relation
There may be scenarios where a parent relation is only defined for other relations to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `abstract` keyword. Let's say in the example above, we would like to define the `location-of-everything` relation type to be abstract. By doing so, we are indicating that no data instances of the `location-of-everything` relation are allowed to be created, leaving us with instances of `location-of-birth` and `location-of-residence` only.

<div class="tabs dark">

[tab:Graql]
```graql
define

location-of-everything sub relation, abstract,
  relates located-subject,
  relates subject-location;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("location-of-everything").sub("relation").isAbstract().relates("located-subject").relates("subject-location")
);
```

[tab:end]
</div>


## Attribute
An attribute is a piece of information that determines the property of an element in the domain. For example, `name`, `language` and `age`. These attributes can be assigned to anything that needs them as a property.

### Define an attribute
To define a new attribute, we use the `sub` keyword followed by `attribute`, `datatype` and the type of the desired value.

<div class="tabs dark">

[tab:Graql]
```graql
define

name sub attribute,
	datatype string;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("name").sub("attribute").datatype("string")
);
```

[tab:end]
</div>

The `name` attribute is now ready to be owned by any other type in the schema.

The data types available in a Grakn knowledge graph are:
- `long`: a 64-bit signed integer.
- `double`: a double-precision floating point number, including a decimal point.
- `string`: enclosed in double `"` or single `'` quotes
- `boolean`: `true` or `false`
- `date`: a date or date-time in ISO 8601 format

**The same attribute can be owned by different concept types.**.

<div class="tabs dark">

[tab:Graql]
```graql
define

start-date sub attribute,
	datatype date;

residency sub relation,
  ## roles and other attributes
  has start-date;

travel sub relation,
  ## roles and other attributes
  has start-date;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("start-date").sub("attribute").datatype("date"),
  type("residency").sub("relation").has("start-date"),
  type("travel").sub("relation").has("start-date")
);
```

[tab:end]
</div>

<div class="note">
[Important]
Attributes in a Grakn knowledge graph are modeled differently to _columns_ in a relational database. In this example, the attribute `start-date` with the value of, for instance `2019-01-01`, exists only once in the knowledge graph and shared among any number of instances that may own it. This is useful when we need to query the knowledge graph for anything that has the `start-date` attribute with value `2019-01-01`. In this case, we would get all the residencies and travels that started on the first day of 2019. It's important to remember this when performing write operations on instances of an attribute type.
</div>

**A concept type can have any number of the same attribute that holds different values.** In other words, a concept type has a many-to-many relation with its attributes.

<div class="tabs dark">

[tab:Graql]
```graql
define

phone-number sub attribute,
	datatype string;

person sub entity,
  has phone-number;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("phone-number").sub("attribute").datatype("string"),
  type("person").sub("entity").has("phone-number")
);
```

[tab:end]
</div>

An instance of a `person` can have one instance of `phone-number`, or two or three, ... you get the idea.

### Restrict attribute's value by Regex
Optionally, we can specify a Regex that the values of an attribute type must conform to. To do this, we use the `regex` keyword followed by the Regex pattern at the end of the attribute's definition.

<div class="tabs dark">

[tab:Graql]
```graql
define

emotion sub attribute,
  datatype string,
  regex "[like, love, funny, shocking, sad, angry]";
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("emotion").sub("attribute").datatype("string").regex("[like, love, funny, shocking, sad, angry]")
);
```

[tab:end]
</div>

### Owners of an attribute
Entities, relations, and even attributes can own one or more attributes of their own. To do this we make use of the `has` keyword followed by the attributes's label.

We have already seen how to [assign an attribute to an entity](#assign-an-attribute-to-an-entity) and similarly to [assign an attribute to a relation](#assign-an-attribute-to-a-relation). But what about an attribute owning an attribute of its own?

### Assign an attribute to another attribute
Let's go through a simple example of how an attribute can own an attribute of its own.

<div class="tabs dark">

[tab:Graql]
```graql
define

content sub attribute, datatype string,
  has language;

language sub attribute,
	datatype string;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("content").sub("attribute").datatype("string").has("language"),
  type("language").sub("attribute").datatype("string")
);
```

[tab:end]
</div>

In this example, attribute `content` can be owned by, for instance, a `post` entity. What this example aims to showcase is that the `content` attribute, besides its own value, owns an attribute named `language` which holds the name of the language the text is written in.

### Define an attribute to play a role
An attribute can play a role in a relation. To define the role played by an attribute, we use the `plays` keyword followed by the role's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

language sub attribute, datatype string,
  plays spoken;

person sub entity,
  plays speaker;

speaking-of-language sub relation,
  relates speaker,
  relates spoken;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("language").sub("attribute").datatype("string").plays("spoken"),
  type("person").sub("entity").plays("speaker"),
  type("speaking-of-language").sub("relation").relates("speaker").relates("spoken")
);```

[tab:end]
</div>

### Subtype an attribute
We can define an attribute to inherit the datatype, attributes owned and roles played by another attribute.

<div class="tabs dark">

[tab:Graql]
```graql
define

event-date sub attribute,
	datatype date;
birth-date sub event-date;
start-date sub event-date;
end-date sub event-date;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("event-date").sub("attribute").datatype("date"),
  type("birth-date").sub("event-date"),
  type("start-date").sub("event-date"),
  type("end-date").sub("event-date")
);
```

[tab:end]
</div>

What this definition means is that `birth-date`, `start-date` and `end-date` are all inherently subtypes of `event-date`. They inherit the datatype of `event-name` as well as its contextuality.

The ability to subtype attributes not only helps mirror the reality of our dataset but also enables automated reasoning using type hierarchies.

#### Define an abstract attribute
There may be scenarios where a parent attribute is only defined for other attributes to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `abstract` keyword. Let's say in the example above, we would like to define the `event-date` attribute type to be abstract. By doing so, we are indicating that no data instances of the `event-date` attribute are allowed to be created, leaving us with instances of `birth-date`, `start-date` and `end-date`.

<div class="tabs dark">

[tab:Graql]
```graql
define

event-date sub attribute, abstract,
	datatype date;
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("event-date").sub("attribute").datatype("date")
);
```

[tab:end]
</div>

<!-- !!! synced with codeKeywordsToLink -->
## Undefine
As the name suggests, we use the `undefine` keyword to remove the definition of a type or its association with other types from the schema.

<div class="note">
[Important]
Don't forget to `commit` after executing an `undefine` statement. Otherwise, anything you have undefined is NOT committed to the original keyspace that is running on the Grakn server.
When using one of the [Grakn Clients](../03-client-api/00-overview.md), to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the [Grakn Console](../02-running-grakn/02-console.md), we use the `commit` command.
</div>

### Undefine an attribute's association
We can undefine the association that a type has with an attribute.

<div class="tabs dark">

[tab:Graql]
```graql
undefine

person has nickname;
```
[tab:end]

[tab:Java]
```java
GraqlUndefine query = Graql.undefine(
  type("person").has("nickname")
);
```

[tab:end]
</div>

The query above, removes the attribute `nickname` from the entity `person`.

<div class="note">
[Important]
It's important to note that `underfine [label] sub [type] has [attribute's label];` undefines the `label` itself, rather than its association with the attribute.
</div>

### Undefine a relation
Given the dependent nature of relations, before undefining the relation itself, we must first undefine the association of its roles with the relation as well as the association of the roleplayers with the roles. Given an `employment` relation, we would undefine it as shown below.

<div class="tabs dark">

[tab:Graql]
```graql
undefine

    speaking-of-language relates speaker; person plays speaker; speaker sub role;
    speaking-of-language relates spoken; language plays spoken; spoken sub role;
    speaking-of-language sub relation;
```
[tab:end]

[tab:Java]
```java
GraqlUndefine query = Graql.undefine(
  type("speaking-of-language").relates("speaker").relates("spoken"),
  type("person").plays("speaker"),
  type("language").plays("spoken"),
  type("speaker").sub("role"),
  type("spoken").sub("role"),
  type("speaking-of-language").sub("relation")
);
```
[tab:end]
</div>

### Undefine a Supertype
When the concept type to be undefined is a supertype to something else, we must first undefine all its subtypes before undefining the supertype itself.

## Summary
We learned that a Grakn schema is essentially a collection of Entities, Relations, and Attributes - what we call the Grakn Concept Types. It is the modularity of these concept types and how they interact with one another that allows us to model complex datasets in an intuitive way that represents their true nature.

In the next section, we learn about one last addition to the schema - [Graql Rules](../09-schema/03-rules.md).
