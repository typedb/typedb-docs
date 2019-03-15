---
sidebarTitle: Overview
pageTitle: Schema
permalink: /docs/schema/overview
---

## Why Use a Schema?

Schema isa a means to address the problems of managing and handling unstructured or loosely structured data.

![Unstructured problems](/docs/images/schema/unstructured-problems.png)

The common problems we encounter when dealing with unstructured or loosely structured data are:
- Integrity
- Accessibility and retrieval
- Maintenance
- Deferring responsibility

Consequently:
- When data is weakly tied to any particular structure it is hard or even impossible to control the state and validity of the data.
As a result we have no guarantees on data consistency and validity.

- With the lack of any high-level structure comes the lack of possibility to query the data meaningfully.
This is either because our data structure is too low level to express complex queries or that handling the complexity of such queries becomes a problem.
Consequently we might be forced to ask simple questions only.

- The problem of maintenance is directly coupled with the integrity problem.
When we have little control over the structure of our data it is hard to alter that structure over time as requirements change. As a consequence,
data changes need to be carried out with surgical precision or risk data pollution.

- Starting with loose or no schema only defers the responsibility of schema definition and enforcement in time.
In production systems we cannot afford to lose control over data. If the database doesn't take responsibility for schema definition and enforcement,
that means that the schema logic needs to be incorporated at the app level.

A Grakn schema is the blueprint of a Grakn knowledge graph. Using a highly flexible language, we define a schema to model a domain true to nature.
Highly interconnected data cannot be stored at scale without an underlying structure - one that is capable of expressing the complexity of the dataset, is easy to understand, and can be extended programmatically, at runtime.

The schema defines a specific, explicit, high-level structure of data that is enforced across the dataset.
This allows the database to provide logical integrity guarantees and consistency guarantees for our data
Any attempt to add data not conforming to the defined schema is a schema violation and is not allowed.

A well-constructed schema enables writing intuitive queries. Given such schema, you often find yourself writing queries that map seamlessly with how you form them as questions in your mind.

Last and certainly not least, the schema sets the basis for performing automated reasoning over the represented data.
It enables the extraction of implicit information from explicitly stored data - a powerful feature of Grakn that facilitates
knowledge discovery and the implementation of business logic inside the database.

## What is a Grakn schema
Grakn schema is an inherent part of the knowledge graph that describes how the data is and can be structured.

If you know a bit about other schema-first database knowledge systems, you know that normally database design involves three schemas:

  1. _A high-level conceptual schema_, that models your problem and usually involves some variation of the entity-relation model

  1. _A mid-level logical schema_, that depends on the database type you are using (for example if you are going relational, this would involve turning the conceptual model into tables and going over a series of normalisation steps of your schema)

  1. _A low level physical schema_, that requires you to optimise your schema according to how your physical resources are distributed

With Grakn, thanks to our high level knowledge model, your schema will closely resemble the conceptual schema, essentially avoiding the hassle of going through the other two modelling steps. The Grakn system will take care of those.

This greatly simplifies the design process, getting you what can be considered a highly normalised distributed schema without the need of going through the logical and physical modelling.

Let us have a look at the main components of a Grakn knowledge graph and schema.

## Grakn Data Model

### Concepts
Everything that describes our domain in a Grakn Knowledge Graph is a concept. This includes the elements of the schema (namely types and roles, which we call schema concepts) and the actual data instances. 
We refer to data instances as things - they can be thought of as instances of types defined in the schema.

### Types
Types constitute the core of your schema. They provide the necessary vocabulary to talk about our domain. They come in three flavours: [Entities](/docs/schema/concepts#entity), [Relationships](/docs/schema/concepts#relationship), and [Attributes](/docs/schema/concepts#attribute):

__Entities__ are the main actors in our domain. These are usually the type of things we want to know about. Entity types provide means of classifying the objects in our domain.

__Relations__ connect other things together. Each relation can connect a number of things.
The character of participation in a relation is characterised by a __role__ that can be played in that relation. Each relation is required to
have at least one role.

__Attributes__ are used to characterise concepts with small pieces of data (think of numbers, strings, dates etc.). Consequently, by defining attributes we can attach values of a specified datatype to our instances.

Apart from serving as a mean of classification, types also define behaviours of their instances. Consequently, types can define the following behaviours:

__has [attribute type]__ - the ability to have an attribute of a specified type attached to an instance.

__plays [role]__ - the ability to participate in relations that allow for that role to be played.

__relates [role]__ (only relation) - the ability of other instances to play this role in instances of this relation type.

### Type Hierarchies
Besides the modularity that the concept types provide, we are free to form subtype relationships between concept types. For a given child concept type subtyping a parent concept type, the child concept type inherits the attributes owned and roles played by the parent type.
The mechanism is analogous to subclassing in Object Oriented Programming. Each concept type can have only a single parent type - multiple inheritance is not supported. 
Subtyping not only allows us to mirror the true nature of a dataset as perceived in the real world, but also enables automated reasoning.

### Roles
_Roles_ specify the nature of the connection between instances. They are not types themselves: you cannot have a thing which is an instance of a role, but you will be able to have things playing a role in a specific relation.
In your schema, we will need to specify what role relates to each relation type and who can play this role.
Thanks to roles, you will be able to guarantee the logical integrity of your data, having a `marriage` between a `person` and a `building`, for example, unless you specifically allow such a thing in the schema.

### Rules
Lastly, the Grakn schema is completed with [**Graql Rules**](/docs/schema/rules). Rules are used for query-time capture of dynamic patterns in the data and performing deduction. Rules are the building blocks of automated reasoning in Grakn.


In the sections that follow, by looking at various real-world examples, we learn how these concepts can be defined in a schema to represent a dataset.


## (un)Define the schema programmatically
In the following sections, we learn how to define a schema using Graql code in a `schema.gql` file. However, defining a schema can also be done programmatically (at runtime) using one of the Grakn Clients - [Java](/docs/client-api/java#client-api-method-manipulate-the-schema-programatically), [Python](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) and [Node.js](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query).

## Load the schema
Once we have defined the schema, the next immediate step is to load it into Grakn. Learn how to [load the schema via the Grakn Console](/docs/running-grakn/console#console-options).

## Migrate Data
To learn about migrating a pre-existing dataset in CSV, JSON or XML formats to a Grakn knowledge graph, check out the [Migration Mechanism](...) followed by a comprehensive [tutorial](...) in the language of your choice.

## Query the schema
In the next section we learn how to [insert](/docs/query/insert-query), [get](/docs/query/get-query), [delete](/docs/query/delete-query), [update](/docs/query/update-data), [aggregate](/docs/query/aggregate-query) and [compute](/docs/query/compute-query) data represented by a schema.

## Reserved Keywords
The following keywords are reserved and meant to only be used by Graql in the schema.
<!-- test-ignore -->
```graql
## Datatypes
datatype
boolean, double, long, string, date
true, false
regex

## Schema definition
has,
abstract, isa,
key,
plays,
relates

## Rules definition
when, then
```

## Summary
The Grakn schema sets the foundation for a Grakn knowledge graph. When modelled thoroughly, the schema provides us with a knowledge graph that benefits from logical integrity, is flexible towards change, capable of automated reasoning, and enables writing intuitive queries.

In the next section, we learn about the members of a schema - [Concept Types](/docs/schema/concepts) and [Rules](/docs/schema/rules).