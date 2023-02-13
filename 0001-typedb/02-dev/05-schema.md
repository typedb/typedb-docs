---
pageTitle: Schema
keywords: typeql, schema, type hierarchy, reserved keywords
longTailKeywords: typeql schema, typeql type hierarchy, typeql data model, typeql reserved keyword
Summary: Introduction to the TypeDB Schema.
---

# Schema

TypeDB database stores data and schema. 

TypeDB schema is a blueprint of a database. It describes how the data can be structured: 

- All user-defined types. 
- Type hierarchy. 
- Data constraints. 
- Inference rules. 

With TypeDB, thanks to our high-level knowledge model, the schema closely resembles 
[conceptual schema](https://en.wikipedia.org/wiki/Conceptual_schema). TypeDB takes care of the hassle of going through
other modelling steps. This greatly simplifies the design process, providing us with, what can be considered, a highly 
normalised distributed schema without the need of going through logical and physical modelling.

![Diagram of concepts in TypeDB](../../images/client-api/overview_hierarchy.png)

**Type** refers to a Concept Type as defined in the schema.

**Thing** refers to an instance of data that is an instantiation of a Concept Type.

## Types

Types constitute the core of the schema. They provide the necessary vocabulary to talk about our domain. They come in 
three flavours: 
- [Entity](../../09-schema/01-concepts.md#entity)
- [Relation](../../09-schema/01-concepts.md#relation)
- [Attribute](../../09-schema/01-concepts.md#attribute)

### Entity 

**Entities** are the main actors in our knowledge domain. These are usually the type of things we want to know about. 
Entity types provide means of classifying the objects in our domain. 

An entity is a thing with a distinct existence in the domain. For example, `organisation`, `location` and `person`.
The existence of each of these entities is independent of any other concept in the domain.

### Relation

**Relations** connect concepts together. Each relation can connect a number of things. A thing's participation in a 
relation is characterised by a **role** that can be played in that relation. Each relation is required to have at least 
one role.

**plays [role]** - the ability to participate in relations that allow for that [role](#roles) to be played.

**relates [role]** (only relations can have this) - the ability for other instances to play the given role in instances 
of the defined relation type.

### Attribute

**Attributes** are used to characterise concepts with small pieces of data (think of numbers, strings, dates etc.). Consequently, by defining attributes we can attach values of a specified value type to our instances.

**owns [attribute type]** - the ability to have an attribute of a specified type attached to an instance.

## Type Hierarchies

We are free to create subtypes of existing types. For a given child type that subtypes a parent type, the child 
type inherits the attributes owned and roles played by the parent type. The mechanism is analogous to subclassing in 
Object Oriented Programming. Each type can have only a single parent type — multiple inheritance is not supported.
Subtyping not only allows us to mirror nature of a dataset as perceived in the real world but also enables automated 
reasoning.

## Roles

_Roles_ are capabilities belonging to relations, that specify the nature of the connection between instances. 
They are not types themselves. That means, we cannot have a thing which is an instance of a role, but we can have things
playing a role in a specific relation. However, roles can also be subtyped (with `as` keyword) and queried similarly to 
regular schema types. 

In the schema, we need to specify what role relates to each relation type and who can play this role. Thanks to roles, 
we are able to guarantee the logical integrity of our data, disallowing a `marriage` between a `person` and a 
`building`, for example. Unless we specifically allow such a relationship in the schema.

## Rules

Lastly, the TypeDB schema is completed with [**TypeQL Rules**](../../09-schema/03-rules.md). Rules are used for 
query-time capture of patterns in the data and performing deduction. Rules are the building blocks of automated 
reasoning in TypeDB.

## Load the schema

Once we have defined the schema, the next immediate step is to load it into TypeDB. We can do this using:

- TypeDB Studio.
- TypeDB Console.
- TypeDB drivers.

### With TypeDB Console

With the TypeDB Console that comes in the TypeDB distribution run: 

```
$ typedb console --command="transaction <database-name> schema write" --command="source <path-to-schema.tql>" --command="commit"
```

This will access database with the name of `<database-name>` in the schema write mode and apply a TypeQL script in the
`<path-to-schema.tql>` file.

### With the TypeDB Studio

See the [TypeDB Studio documentation](../../02-clients/01-studio.md#write-a-schema).

### With TypeDB drivers (programmatically)

Defining a schema can also be done programmatically (at runtime) using one of the 
[TypeDB Clients](04-clients.md).

<!---
Concepts and rules
-->

## Reserved Keywords

The following keywords are reserved and meant to only be used by TypeQL.
<!-- test-ignore -->
```typeql
## Native types
thing, entity, attribute, relation, role

## Data types
long, double, string, boolean, datetime

## Query commands
define, undefine, match, get, insert, delete;

## Delete and get query modifiers
offset, limit, group, sort, asc, desc

## Statement properties
abstract, as, iid, type, isa, isa!, sub, sub!, owns, has, plays, relates, value, regex, rule, when, then

## Operators
or, not, like, is

## Literal values
true, false
```

## Summary

The TypeDB schema sets the foundation for a TypeDB data. When modelled thoroughly, the schema provides us 
with a knowledge graph that benefits from logical integrity, is flexible towards change, capable of automated reasoning,
and enables writing intuitive queries.
