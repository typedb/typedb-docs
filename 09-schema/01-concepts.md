---
sidebarTitle: Concepts
pageTitle: Schema Concepts
permalink: /docs/schema/concepts
---

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/java) or [Python](/docs/client-api/python)**: Executing a query that defines or undefines a a schema concept, is as simple as passing the Graql (string) query to the `query()` method available on the `transaction` object.
</div>

<!-- !!! synced with codeKeywordsToLink -->
## Define
As the name suggests, we use the `define` keyword to develop the [schema](/docs/schema/overview) which represents the dataset stored in a Grakn knowledge graph. We use `define` to add new entities, relationships, attributes and rules to the schema.

When defining the schema in a single `schema.gql` file, the keyword `define` needs to be included only once at the very top.

We can also use the `define` keyword in the interactive mode of the [Graql Console](/docs/running-grakn/console) as well as the Grakn Clients [Java](/docs/client-api/java#client-api-method-manipulate-the-schema-programatically), [Python](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) and [Node.js](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query).

<div class="note">
[Important]
Don't forget to `commit` after executing a `define` query. Otherwise, anything you have defined is NOT committed to the original keyspace that is running on the Grakn server.
When using one of the Grakn Clients, to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the Graql Console, we use the `commit` command.
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
DefineQuery query = Graql.define(
  label("person").sub("entity")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
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
  has bio,
  has gender;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("person").sub("entity").has("full-name").has("nickname").has("bio")
  .has("gender")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
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
DefineQuery query = Graql.define(
  label("person").sub("entity").key("email")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

This guarantees that no instances of `email` may hold the same value among all instances of `person`.

<div class="note">
[Note]
Although, in the example above, we have assigned attributes to the `person` entity, they are yet to be defined. We soon learn how to [define an attribute](#define-an-attribute).
</div>


### Entity to play a role
An entity can play a role in a relationship. To define the role played by an entity, we use the `plays` keyword followed by the role's label.

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
DefineQuery query = Graql.define(
  label("person").sub("entity").plays("employee"),
  label("organisation").sub("entity").plays("employer"),
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

<div class="note">
[Note]
We are yet to define the relationship that relates to the roles `employer` and `employee`. We soon learn how to [define a relationship](#define-a-relationship).
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
DefineQuery query = Graql.define(
  label("post").sub("entity").plays("replied-to").plays("tagged-in")
  .plays("reacted-to"),
  label("comment").sub("post").has("content").plays("attached-to"),
  label("media").sub("post").has("caption").has("file").plays("attached"),
  label("video").sub("media"),
  label("photo").sub("media")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

As you can see in the example above, when defining entities, what follows the `sub` keyword can be a label previously given to another entity. By subtyping a parent entity, the children inherit all attributes owned and roles played by their parent.

In this example, `comment` and `media` are both considered to be subtypes of `post`. Similarly `video` and `photo` are subtypes of `media` and so are defined that way. Therefore, although not defined explicitly, we are right to assume that `comment`, `media`, `video` and `photo` all play the roles `replied-to`, `tagged-in` and `reacted-to`. However, the role `attached` and the attributes `caption` and `file` are played and owned only by the `media` entity and its subtypes. Similarly, the role `attached-to` and the attribute `content` are played and owned only by the `comment` entity.

<div class="note">
[Note]
We are yet to define the relationships that relate to the roles as well as the attributes in the example above. We soon learn how to [define a relationship](#define-a-relationship) and [define an attribute](#define-an-attribute).
</div>

The ability to subtype entities not only helps mirror the reality of the dataset as perceived in the real world but also enables automated reasoning using type hierarchies.

### Define an abstract entity
There may be scenarios where a parent entity is only defined for other entities to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `is-abstract` keyword. Let's say in the example above, we would like to define both the `post` and `media` entity types to be abstract. By doing so, we are indicating that no data instances of the of these entity types are allowed to be created, leaving us only with instances of `comment`, `photo` and `video`.

<div class="tabs dark">

[tab:Graql]
```graql
define

post sub entity is-abstract;

media sub post is-abstract;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("post").sub("entity").isAbstract(),
  label("media").sub("post").isAbstract()
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

## Relationship
A relationship describes how two or more things are in some way connected to each other. For example, `friendship` and `employment`. Each of these relationships must relate to roles that are played by something else in the domain. In other words, relationships are dependent on the existence of at least two other things.

### Define a relationship
To define a new relationship, we use the `sub` keyword followed by `relationship`.

```graql
define

employment sub relationship;
```

To complete the definition of a relationship, we must determine the roles that it relates to. To do so, we use the `relates` keyword followed by the role's label.

<div class="tabs dark">

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

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

The roles `employee` and `employer` are now ready to be played by other concept types in the schema.

### Roleplayers of a relationship
Entities, attributes, and even other relationships can play a role in a relationship. To do this we make use of the `plays` keyword followed by the role's label.

We have already seen how to [define an entity to play a role](#entity-to-play-a-role) and soon learn how to [define an attribute to play a role](#define-an-attribute-to-play-a-role) as well. But what about a relationship that plays a role in another relationship?

### Define a relationship to play a role
Let's go through a simple example of how a relationship can play a role in another relationship.

<div class="tabs dark">

[tab:Graql]
```graql
define

friendship sub relationship,
  relates friend,
  plays requested-friendship;

friend-request sub relationship,
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
DefineQuery query = Graql.define(
  label("friendship").sub("relationship").relates("friend")
  .plays("requested-friendship"),
  label("friend-request").sub("relationship").relates("requested-friendship")
  .relates("friendship-requester").relates("friendship-respondent"),
  label("person").sub("entity").plays("friend").plays("friendship-requester)
  .plays("friendship-respondent")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

In the example above, the `friendship` relationship plays the role of the `requested-friendship` in the `friend-request` relationship. The other two roleplayers in a `friend-request` are 1) the `person` who plays the `friendship-requester` role and 2) another `person` whole plays the `friendship-respondent` role.

Once the `friend-request` is accepted, then those two `person`s play the role of `friend` in the `friendship` relationship.

### A relationship with many roleplayers
A relationship can relate to any number of roles. The example below illustrates a three-way relationship.

<div class="tabs dark">

[tab:Graql]
```graql
define

reaction sub relationship,
  relates reacted-emotion,
  relates reacted-to,
  relates reacted-by;

emotion sub attribute datatype string,
  plays reacted-emotion;

post sub entity,
  plays reacted-to;

person sub entity,
  plays reacted-by;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("reaction").sub("relationship").relates("reacted-emotion")
  .relates("reacted-to").relates("reacted-by"),
  label("emotion").sub("attribute").datatype(AttributeType.DataType.STRING)
  .plays("reacted-emotion"),
  label("post").sub("entity").plays("reacted-to"),
  label("person").sub("entity").plays("reacted-by")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

In the example above, the `reaction` relationship relates to three roles:
1. `reacted-emotion` role played by an `emotion` attribute.
2. `reacted-to` role played by a `post` entity.
3. `reacted-by` role played by a `person` entity.

### Assign an attribute to a relationship
We can assign any number of attributes to a relationship. To do so, we use the `has` keyword followed by the attribute's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

friend-request sub relationship,
  has approved-date,
  relates requested-friendship,
  relates friendship-requester,
  relates friendship-respondent;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("friend-request").sub("relationship")..has("approved-date")
  .relates("requested-friendship").relates("friendship-requester").
  relates("friendship-respondent")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

To assign a unique attribute to a relationship, we use the `key` keyword followed by the attribute's label.

<div class="tabs dark">

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
  label("employment").sub("relationship").key("reference-id").relates("employer")
  .relates("employee")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

This guarantees that no instances of `reference-id` may hold the same value among all instances of `employment`.

<div class="note">
[Note]
Although, in the example above, we have assigned the attributes to the `friend-request` and `employment` relationships , they are yet to be defined. We soon learn how to [define an attribute](#define-an-attribute).
</div>

### Subtype a relationship
We can define a relationship to inherit all attributes owned, and roles related to and played by another relationship. Let's take a look at an example of subtyping an `affiliation` relationship.

<div class="tabs dark">

[tab:Graql]
```graql
define

location-of-everything sub relationship,
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
DefineQuery query = Graql.define(
  label("location-of-everything").sub("relationship").relates("located-subject")
  .relates("subject-location"),
  label("located-birth").sub("located-subject"),
  label("birth-location").sub("subject-location"),
  label("location-of-birth").sub("location-of-everything").relates("located-birth")
  .relates("birth-location"),
  label("located-residence").sub("located-subject"),
  label("residence").sub("subject-location"),
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

As you can see in the example above, when defining relationships, what follows the `sub` keyword can be a label previously given to another relationship. By subtyping a parent relationship, the children inherit all attributes owned and roles played by their parent.

In this example, `location-of-birth` and `location-of-residence` are both considered to be subtypes of `location-of-everything` and so are defined that way. Modelling these relationships in this way, not only allows us to query for locations of birth and residence separately, but also allows us to query for all the associations that a given person has with a given location.

Note the use of the `as` keyword. This is necessary to determine the correspondence between the role of the child and that of the parent.

<div class="note">
[Important]
All roles defined to relate to the parent relationship must also be defined to relate to the child relationship using the `as` keyword.
</div>

The ability to subtype relationships not only helps mirror the reality of the dataset as perceived in the real world but also enables automated reasoning using type hierarchies.

#### Define an abstract relationship
There may be scenarios where a parent relationship is only defined for other relationships to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `is-abstract` keyword. Let's say in the example above, we would like to define the `location-of-everything` relationship type to be abstract. By doing so, we are indicating that no data instances of the `location-of-everything` relationship are allowed to be created, leaving us with instances of `location-of-birth` and `location-of-residence` only.

<div class="tabs dark">

[tab:Graql]
```graql
define

location-of-everything sub relationship is-abstract,
  relates located-subject,
  relates subject-location;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("location-of-everything").sub("relationship").isAbstract()
  .relates("located-subject").relates("subject-location")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
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

name sub attribute datatype string;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("name").sub("attribute").datatype(AttributeType.DataType.STRING)
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
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

start-date sub attribute datatype date;

residency sub relationship,
  ## roles and other attributes
  has start-date;

travel sub relationship,
  ## roles and other attributes
  has start-date;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("start-date").sub("attribute").datatype(AttributeType.DataType.STRING),
  label("residency").sub("entity").has("start-date"),
  label("travel").sub("entity").has("start-date")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

<div class="note">
[Important]
Attributes in a Grakn knowledge graph are modeled differently to _columns_ in a relational database. In this example, the attribute `start-date` with the value of, for instance `2019-01-01`, exists only once in the knowledge graph and shared among any number of instances that may own it. This is useful when we need to query the knowledge graph for anything that has the `start-date` attribute with value `2019-01-01`. In this case, we would get all the residencies and travels that started on the first day of 2019. It's important to remember this when performing write operations on instances of an attribute type.
</div>

**A concept type can have any number of the same attribute that holds different values.** In other words, a concept type has a many-to-many relationship with its attributes.

<div class="tabs dark">

[tab:Graql]
```graql
define

phone-number sub attribute datatype string;

person sub entity,
  has phone-number;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("phone-number").sub("attribute").datatype(AttributeType.DataType.STRING),
  label("person").sub("entity").has("phone-number"),
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

An instance of a `person` can have one instance of `phone-number`, or two or three, ... you get the idea.

### Restrict attribute's value by Regex
Optionally, we can specify a Regex that the values of an attribute type must conform to. To do this, we use the `regex` keyword followed by the Regex pattern at the end of the attribute's definition.

<div class="tabs dark">

[tab:Graql]
```graql
emotion sub attribute datatype string regex /[like, love, funny, shocking, sad, angry]/;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("emotion").sub("attribute").datatype(AttributeType.DataType.STRING).regex("/[like, love, funny, shocking, sad, angry]/")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

### Owners of an attribute
Entities, relationships, and even attributes can own one or more attributes of their own. To do this we make use of the `has` keyword followed by the attributes's label.

We have already seen how to [assign an attribute to an entity](#assign-an-attribute-to-an-entity) and similarly to [assign an attribute to a relationship](#assign-an-attribute-to-a-relationship). But what about an attribute owning an attribute of its own?

### Assign an attribute to another attribute
Let's go through a simple example of how an attribute can own an attribute of its own.

<div class="tabs dark">

[tab:Graql]
```graql
define

content sub attribute datatype string,
  has language;

language sub attribute datatype string;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("content").sub("attribute").datatype(AttributeType.DataType.STRING)
  .has("language"),
  label("language").sub("attribute").datatype(AttributeType.DataType.STRING)
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

In this example, attribute `content` can be owned by, for instance, a `post` entity. What this example aims to showcase is that the `content` attribute, besides its own value, owns an attribute named `language` which holds the name of the language the text is written in.

### Define an attribute to play a role
An attribute can play a role in a relationship. To define the role played by an attribute, we use the `plays` keyword followed by the role's label.

<div class="tabs dark">

[tab:Graql]
```graql
define

language sub attribute datatype string,
  plays spoken;

person sub entity,
  plays speaker;

speaking-of-language sub relationship,
  relates speaker,
  relates spoken;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("language").sub("attribute").datatype(AttributeType.DataType.STRING)
  .plays("spoken"),
  label("person").sub("entity").plays("speaker"),
  label("speaking-of-language").sub("relationship").relates("speaker").relates("spoken")
);
query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

### Subtype an attribute
We can define an attribute to inherit the datatype, attributes owned and roles played by another attribute.

<div class="tabs dark">

[tab:Graql]
```graql
define

event-date sub attribute datatype date;
birth-date sub event-date;
start-date sub event-date;
end-date sub event-date;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("event-date").sub("attribute").datatype(AttributeType.DataType.DATE),
  label("birth-date").sub("event-date"),
  label("start-date").sub("event-date"),
  label("end-date").sub("event-date")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

What this definition means is that `birth-date`, `start-date` and `end-date` are all inherently subtypes of `event-date`. They inherit the datatype of `event-name` as well as its contextuality.

The ability to subtype attributes not only helps mirror the reality of our dataset but also enables automated reasoning using type hierarchies.

#### Define an abstract attribute
There may be scenarios where a parent attribute is only defined for other attributes to inherit, and under no circumstance, do we expect to have any instances of this parent. To model this logic in the schema, we use the `is-abstract` keyword. Let's say in the example above, we would like to define the `event-date` attribute type to be abstract. By doing so, we are indicating that no data instances of the `event-date` attribute are allowed to be created, leaving us with instances of `birth-date`, `start-date` and `end-date`.

<div class="tabs dark">

[tab:Graql]
```graql
define

event-date sub attribute is-abstract datatype date;
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("event-date").sub("attribute").datatype(AttributeType.DataType.DATE),
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

<!-- !!! synced with codeKeywordsToLink -->
## Undefine
As the name suggests, we use the `undefine` keyword to remove the definition of a type or its association with other types from the schema.

<div class="note">
[Important]
Don't forget to `commit` after executing an `undefine` statement. Otherwise, anything you have undefined is NOT committed to the original keyspace that is running on the Grakn server.
When using one of the [Grakn Clients](/docs/client-api/overview), to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the [Graql Console](/docs/running-grakn/console), we use the `commit` command.
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
Graql.undefine(
  label("person").has("nickname")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

The query above, removes the attribute `nickname` from the entity `person`.

<div class="note">
[Important]
It's important to note that `underfine [label] sub [type] has [attribute's label];` undefines the `label` itself, rather than its association with the attribute.
</div>

### Undefine a relationship
Given the dependent nature of relationships, before undefining the relationship itself, we must first undefine the association of its roles with the relationship as well as the association of the roleplayers with the roles. Given an `employment` relationship, we would undefine it as shown below.

<div class="tabs dark">

[tab:Graql]
```graql
undefine
  
  employment relates employer; company plays employer; employer sub role;
  employment relates employee; person plays employee; employee sub role;
  employment sub relationship;
```
[tab:end]

[tab:Java]
```java
Graql.undefine(
  label("employment").relates("employer").relates("employee"),
  label("company").plays("employer"),
  label("person").plays("employee"),
  label("employer").sub("role"),
  label("employee").sub("role"),
  label("employment").sub("relationship")
);

query.withTx(transaction).execute();
transaction.commit();
```
<!-- 1.5 transaction.execute(query.toString()); -->
[tab:end]
</div>

### Undefine a Supertype
When the concept type to be undefined is a supertype to something else, we must first undefine all its subtypes before undefining the supertype itself.

## Summary
We learned that a Grakn schema is essentially a collection of Entities, Relationships, and Attributes - what we call the Grakn Concept Types. It is the modularity of these concept types and how they interact with one another that allows us to model complex datasets in an intuitive way that represents their true nature.

In the next section, we learn about one last addition to the schema - [Graql Rules](/docs/schema/rules).
