---
sidebarTitle: Basic Schema
pageTitle: Define a Basic Schema
permalink: /docs/schema/basic-schema
---

## Introduction

In this section we are going to go through the construction of a basic schema. We recommend that you refer to the [schema](/docs/schema/overview) documentation before reading this page and possibly to the [Schema Concepts](/docs/schema/concepts) page as you go through. 
The process we are about ti follow is a general guideline as to how you may start designing a schema.

The schema we will be building is a social network one describing typical relations among a network of people. 
You can find the complete schema, the dataset and rules that accompany it, on Github in our [docs repository](https://github.com/graknlabs/docs/blob/master/files/social-network-schema.gql).


## Identifying Entity Types

The first step is about identifying the categories of things that will be in your knowledge graph.
For example if you are modelling a retail store, valid categories may be `product`, `electronics`, `books`, etc.  It is up to you to decide the granularity of your categories.

For our social network knowledge graph we know that it will mostly be filled with people. So we can create an entity type:

```graql
define
  person sub entity;
```

Naturally, we could break this up into `man` and `woman` but for this example we are going to keep things simple.  

## Describing Entity Types

Grakn provides you with the ability to attach resources to entity types. For example a `car` could have an `engine`, a `licence number`, and a `transmission type` as resources that help to describe it.

So what helps describe a `person`?
Philosophical debates aside let us go with something simple. A `person` typically has a `full-name`, a `nickname`, and a `gender`. We can model this and other resources that identify a person with:

```graql
define

person sub entity,
    has full-name,
    has nickname,
    has gender,
    has phone-number,
    key email;

name sub attribute, datatype string;
full-name sub name;
nickname sub name;
phone-number sub attribute, datatype string;
email sub attribute, datatype string;
gender sub attribute, datatype string;
```

Two important things here to note are that we treat `full-name` and `nickname` as a special type of `name` by making them subtypes of `name`. Another important things is that we define `email` to be a `key` for person. What it means is that
emails for persons are unique - each person has to have one and exactly one email which is validated during data creation.

## Identifying Relationships and Roles

The next step is to ask how your data is connected, that is, what are the relationships between your data.

The relationhips can be between different entity types, for example, a `person` **drives** a `car`, or even between the same entity types, for example, a `person` **marries** another `person`.

In Grakn, n-ary relationships are also possible. For example, a `person` has a `child` with another `person`.

In our example, we will add `marriage` and `parentship` relationships. The `marriage` relationship has a single `spouse` role, whereas the `parentship` relationship is characterised
by two roles of `parent` and `child`. 

```graql
define

marriage sub relation,
	relates spouse;
	

parentship sub relation,
  	relates parent,
	relates child;
```

## Allowing Roles to be Played

The next step is to give our entity types permission to play specific roles. We do this explicitly so that we don't accidentally relate data which should not be related. For example, this will prevent us from accidentally saying that a `dog` and a `person` can be married.

In the current example we have only one entity type, which can play all our current roles, so we explicitly state that with:  

```graql
define

person sub entity,
    plays parent,
    plays child,
    plays spouse;
```    

We have now completed our basic social network schema.

## The Complete Schema

The final schema will now look something like this:

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

## Summary

In this tutorial we described our entity type `person` across separate steps. This was done to demonstrate the typical thought process when creating a schema. It is typically good practice to group entity type definitions together as above.

It is worth noting that the schema does not need to be completely finalised before loading data. The schema of a Grakn knowledge graph can be expanded even after loading data.

## Where Next?

We will continue to explore the development of a schema in the next section on defining a [hierarchical schema](./hierarchical-schema).
