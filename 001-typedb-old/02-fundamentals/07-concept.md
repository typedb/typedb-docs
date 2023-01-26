---
pageTitle: Concept
keywords: typedb, concept
longTailKeywords: typedb concept
summary: TypeDB concept.
toc: false
---

<!--- 
Queries return Answers - either numerical or structures of Concept. Concept represents either a Type (from schema), Thing (from data), or Value (from computation). Client-side concepts can be used as mini-ORMs 
-->

# Concept

Anything in TypeDB (other than [Rules](../09-schema/03-rules.md)), whether it's a type or a data instance, is a
[Concept](../04-concept-api/01-concept.md) (see the diagram below).

![Concept Hierarchy](../../images/client-api/overview_hierarchy.png)

<!--- #todo Set image size and align constraints -->

## Schema and types

Types in the [schema](../../09-schema/00-overview.md) are built using subtyping, like in some object-oriented
programming languages. Each database comes with the same default types built in:

- `entity`
- `relation`
- `attribute`

The most cool part is that we can create our own types based on any other types in the schema, default or not.

<div class="note">
[Note]
The attentive reader may have noticed one more concept on the diagram above. Role is an internal type, used for 
relations. How exactly Role type is used we will explore [later](../../09-schema/00-overview.md#roles).
</div>

## Data and things

All [data](../../11-query/00-overview.md) elements loaded into your database are _instances_ of your types (like
objects are instances of classes in [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming)). Since your types
are subtypes of built-in default types each data element will also be an (indirect) instance of one of the default type: `entity`, `relation`, or `attribute`. Any instance of any type can be called a Thing.