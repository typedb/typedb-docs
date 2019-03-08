---
sidebarTitle: Hierarchical Schema
pageTitle: Define a Hierarchical Schema
permalink: /docs/schema/hierarchical-schema
---

## Introduction

In this section we are going to expand the schema we defined in the [Basic Schema documentation](./basic-schema), which we recommend you read before starting here. 
You may also find it helpful to refer to the [Schema Overview](/docs/schema/overview) and [Schema Concepts](/docs/schema/concepts) documentation.
We are going to introduce the idea of making schemas deeper and more meaningful by defining a hierarchy of types. The technique is in a way analogous to subclassing classes in Object Oriented Programming.

When we left off, our schema looked as follows:

```graql
define

#Entities

person sub entity,
    has name,
    has gender,
    has phone-number,
    key email,
    plays parent,
    plays child,
    plays spouse;

 # Attributes

name sub attribute, datatype string;
phone-number sub attribute, datatype string;
email sub attribute, datatype string;
gender sub attribute, datatype string;

 # Roles and Relations

marriage sub relation,
	relates spouse;
	

parentship sub relation,
  	relates parent,
	relates child;
```
This schema represents a simple social network schema. This is a very simplistic schema with plenty of room for extension, so let's begin!

## Hierarchies of Entity Types

It is possible to define entity types more granularly. Think of sub-categories that enable additional details to be embedded in the schema or subclasses in OOP.
For example, if we have an entity type called `vehicle`, we can break that down further by differentiating between `cars` and `motorbikes`. This can be done as follows:

```graql
define

vehicle sub entity;
car sub vehicle;
motorbikes sub vehicle;
```    

In the above example we are saying that a `car` is a subtype (a specialised type) of a `vehicle`. This means that when adding data to our knowledge graph, when we know we have a `vehicle`, we can also differentiate between a `car` and a `motorbike`.

So how can we use this technique to improve our existing social network schema?

We could specialise the `person` entity into `man` and `woman` for example. However, for the sake of making things more interesting, we are going to introduce a new entity to the knowledge graph. 

Since the end goal is to model a social network, we want to be able to quantify the online social presence of people somehow. In that way we introduce entities of type `post` and `media` as well as their specialised subtypes.

We can model this as follows:

```graql
define

post sub entity,
    abstract,
    key identifier;

status-update sub post,
    has content;

comment sub post,
	has content;

album sub post,
	has title,
	has published-date;

media sub post,
	abstract,
	has caption,
	has file;

video sub media;
photo sub media;

content sub attribute, datatype string;
title sub attribute, datatype string;
published-date sub attribute, datatype date;

```

Notice that for the `post` and `media` entity type we added an `abstract` keyword. Similarly to OOP, This is an optional restriction to ensure that we do not create any instances of `post` or `media`, but instead use the most granular definitions provided, i.e. `comment`, `video`, etc . . .  

## Hierarchies of Relationship Types and Roles

Grakn also allows you to design hierarchies of relationship types and role types, enabling the schema to be deeper and more expressive. For example, if we have a relationship type called `partnership` between two people we can expand on this by defining more detailed partnerships; `civil-partnership`, `marriage`, `unions`, etc.

Now lets take a look at expanding our social network schema. When modelling a domain there are many ways of doing so. 
We will first expand our `marriage` relationship type so that it can provide more meaning:

```graql
define

relatives sub relationship
  is-abstract;

marriage sub relation
  relates spouse
  relates husband as spouse
  relates wife as spouse
  has event-date;

```

We have defined a new super type called `relatives` which enables us to link generic relatives together, and we have said that marriage is a type of relative relationship. We have also expanded on the roles which make up a marriage, enabling us to be more expressive and detailed about the domain we are modelling.
From now on, we can be clear if a person is a `husband` or a `wife` or just a `spouse` in a marriage. Note that, when we query for people who play the role of a `spouse` we will get all the `husbands` and `wives` as well.

Let's expand this even further:

```graql
define

parentship sub relatives
  relates parent
  relates mother as parent
  relates father as parent
  relates child
  relates son as child
  relates daughter as child;

```

Please note that the role specialisation happens via the `as` keyword. The following definition:

```graql
parentship sub relation,
  	relates parent,
	relates father as parent;
```

is equivalent to defining:

```graql
parentship sub relation,
  	relates parent,
	relates father;
father sub parent;
```

Now we have provided more detail about being a parent. We have also said that being a parent is a `relatives` relationship. This is quite useful because when we ask for all relatives we will be getting relatives via birth and via marriage.

## Wrapping up

We could go into far more detail regarding our genealogy knowledge graph but I will leave that to you.
For the moment here is our more complex schema to get you started on making your own deeper ontologies.

```graql-test-ignore

define

# Entities

  person sub entity
    has gender
    has birth-date
    has death-date
    has identifier
    has firstname
    has middlename
    has surname
    plays spouse
    plays parent
    plays child;

    gender sub attribute datatype string;
    birth-date sub event-date;
    death-date sub event-date;
    name sub attribute datatype string;
    firstname sub name;
    middlename sub name;
    surname sub name;
    identifier sub attribute datatype string;

  event sub entity
    is-abstract
    has degree
    has confidence
    has event-date
    has identifier
    has notes
    has conclusion
    has happening;

  wedding sub event;

  funeral sub event
    has death-date;

  christening sub event
    has birth-date;

  birth sub event
    has firstname
    has middlename
    has surname
    has gender
    has birth-date;

  death sub event
    has death-date;   	    

## Relations

  relatives sub relationship
    is-abstract;

  marriage sub relatives
    relates spouse
    relates spouse1 as spouse
    relates spouse2 as spouse
    relates husband as spouse
    relates wife as spouse
    has event-date;

  parentship sub relatives
    relates parent
    relates mother as parent
    relates father as parent
    relates child
    relates son as child
    relates daughter as child;

## Attributes
  event-date sub attribute datatype date;
  notes sub attribute datatype string;
  happening sub attribute datatype string;
  degree sub attribute datatype string;
  conclusion sub attribute datatype string;
  confidence sub attribute datatype string;

```



## Where Next?

We will continue to explore the development of a schema in the next section on defining a [rule-driven schema](./rule-driven-schema).