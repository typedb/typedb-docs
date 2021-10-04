---
pageTitle: Introduction
keywords: typedb, typeql, overview, introduction, modeling
longTailKeywords: thinking in typedb, thinking in typeql, learn typedb, learn typeql, typedb schema, typedb data model
summary: A birds-eye view of TypeQL and TypeDB
toc: false
---

# Welcome to TypeQL and TypeDB

TypeDB is a new kind of database, utilising type systems to help you break down complex problems
into meaningful and logical systems. Using TypeQL, TypeDB gives you powerful abstractions over low-level
and complex data patterns. By combining TypeQL and TypeDB, we can close the gap the language of your domain, 
and what the database can interpret and respond to. 

TypeDB guarantees data integrity and safety, while enabling data-level inferences within the database
itself. This new paradigm gives you a higher level of expressivity to simplify your work and
tackle domains that seemed impossibly complex before.

## Thinking in TypeQL and TypeDB

The backbone of any TypeDB database is the representation of your domain: the schema.
The schema is made up of a set of types and rules, which harness object-oriented principles and logical deduction.

Types defined in your schema are structured: some are entity types (representing the objects in your domain),
some are relation types (representing n-ary connections within your domain), and some are attribute types (representing values). [1]
When a relation type is used to connect types, each type must play a particular role. This is captured using a _role type_,
which provides context to your connections.

Rules defined in your schema are deductive logic -- encoded knowledge about your domain. They are when-then 
inferences that when applied to your data generate insights and new facts. 

Using these simple constructs, you can build a schema of domain-specific terminology and knowledge, in a way that is 
also understood by TypeDB. This also relieves you of the need to think in terms of tables, documents, or vertices/edges, 
and allows you to think at a higher level of abstraction, in a language familiar to you. 
Designing data models and managing data at this level of abstraction is one of the primary offerings of TypeQL and TypeDB.

If you are coming from an SQL background, you may be interested in a comparison with [modeling in SQL](../12-comparisons/00-sql-and-typeql.md#modelling-and-defining-schema).
If you are coming from property graphs, you may be interested in a comparison to [modeling with property graphs](../12-comparisons/02-graph-databases-and-typedb.md#modelling-and-defining-schema).

## Building with Entity-Relation-Attribute types

Let's look a bit deeper into these building blocks.

A database is made of schema, and data. Types in the schema are built using subtyping, similar to object-oriented
programming languages. Each database comes with some types built in: `entity`, `relation`, and `attribute`, 
which you will extend to create your schema.

What about the data? Well, all data elements loaded into your database are _instances_ of your types. 
Since your types are subtypes of `entity`, `relation`, or `attribute`, each data element will also be an 
(indirect) instance of `entity`, `relation`, or `attribute`. 
Deciding which of these to use when modeling your data is an important task when building your TypeDB schema.

### Entities

Entities are the main, distinguishable objects in _your domain_. Each entity type you create is a subtype of
the built-in abstract type `entity`. Some examples in a [social network](../00-general/04-quickstart.md) 
domain might be `person`, `timeline`, `school`, etc.

### Relations

Relations are intended to connect data throughout your domain. Each new relation type you create is a subtype of 
the built-in abstract type `relation`. 

In other databases, relations may be implemented with a join table (SQL), or an edge between two vertices (graph databases).
TypeDB relations generalise both: they flexibly relate one, two, or any number of data instances at the same time. 

This expanded idea of a relation is more powerful than either SQL or graph relations. However, we can further
improve; if we allow relations to not just specify which instances relate to each other, but also _how_ by adding
context.

We add this context by introducing _role types_. Role types are part of the definition of relation types, 
and define the interface between relations and other types. As role types are always specified as
part of a relation type, they have fully qualified names `<relation type>:<role type>`.

So if we have the following TypeDB schema:
```typeql
define
  employment sub relation, relates employee, relates employer; 
  person sub entity, plays employment:employee;
  company sub entity, plays employment:employer;
```

We can now create `employment` relations that connect `person` entities to `company` entities. When doing so,
a `person` must play the `employment:employee` role, while the `company` must play the `employment:employer` role.
We say that `person` and `company` are _role players_ in `employment` relations.

Which types can be a role player? In TypeDB, entities, relations, and attributes are first-class citizens. 
So, TypeDB allows any of these types to be role players!

What this means is that:
  - In the simplest case, relations connect entities to each other, when the entity is a role player in a relation.
  - Relations can connect attributes, because attributes can also be role players. 
  - Relations can be nested, because a relation can be a role player in another relation.
  - Relations can even relate to themselves, by being their own role players!

This makes for a flexible modeling language for building structure in your database.

### Attributes

Attribute types represent the only part of the database that can carry an actual value. 
They subtype the built-in abstract type `attribute`.

However, attribute types are first-class citizens of TypeDB, not just properties of entities or relations. So how
do we associate data with entities or relations? 

To do this, we allow types to "own" or "have" an attribute type, representing an association from the attribute owner, to the attribute (the value). 

As all types are first-class citizens in TypeQL and TypeDB, any type can be an attribute owner.

This means that:
  - In the simplest case, entities own attributes.
  - Relations can own attributes (useful when annotating connections with metadata, lineage, etc.)
  - Attributes can own attributes (useful for abbreviations, acronyms, nicknames, etc.)

These features allow flexibility when associating data values within your database.

#### Attribute Instances

In the data, attribute instances in TypeDB are _globally unique by type and value_, and _immutable_.
Being globally unique and immutable means your data is maximally [normalised](https://en.wikipedia.org/wiki/Database_normalization) at all times. 

What does this mean in practice? As an example, in a database of people with ages, there will be at most one instance of 
`age 10`, which can never be changed in-place.

So how do multiple people instances have the same age with value 10? We create an ownership of the attribute instance 
`age 10` by each person. 

We do this with the `has` keyword:
```typeql
match 
  $x isa person, has nickname "Beth"; 
  $y isa person, has nickname "Jill"; 
insert 
  $x has age 10; 
  $y has age 10;
```

This creates an association from the person with `nickname "Beth"` and person with `nickname "Jill"`, to the attribute instance `age 10`.
Thus, many people can have the age 10, by creating new associations to the attribute.

Given that attributes are immutable, and shared, it may not look easy to update a person's age. 
However, instead of changing the attribute, we replace the attribute ownership.
```typeql
match $x isa person, has nickname "Beth", has age $a; $a = 10;
delete $x has $a;
insert $x has age 11;
```

This leave Beth with a new age `11`, while all other people are unchanged.

## Inference 

To further simplify your models, TypeQL and TypeDB offer two types of inference: type inference, and rule inference.

### Type Inference and Inheritance

By basing our models on entities, relations, and attributes, blended with subtyping, we naturally introduce inheritance: 
a subtype will inherit properties (such as roles played, and attributes owned) from their parent types. This
has the same advantages as inheritance in programming languages, enabling reuse and more realistic representations
of data.

For example:
```typeql
define
  organisation sub entity, owns name;
  nonprofit sub organisation;
  name sub attribute, value string;
```

All `nonprofit` instances will be allowed to own a `name`, by inheritance. These inherited properties are transparently 
inferred at query time.

### Rule Inference

To build the most expressive models, you may desire to write deductive logic at the database level. To do this, you write rules,
which can at query time transparently infer new facts.

The following rule, for example, can automatically infer co-workers by detecting employees at the same company.

```typeql
define
  rule people-work-at-the-same-organisation:
  when {
    $e1 (employee: $p1, employer: $o) isa employment;
    $e2 (employee: $p2, employer: $o) isa employment;
    not { $p1 is $p2; };
  } then {
    (employee: $p1, employee: $p2, organisation: $o) isa mutual-employment;
  };
```

Rules allow you to embed domain knowledge in the database, and expose the outcomes as normal data, without being
persisted on disk.


## Summary

TypeQL and TypeDB allow you build a data model out of entity, relation, and attribute types. 
Inheritance allows subtypes to be defined simply and reduce complexity, while roles and rules further enhance your schema.
These abstractions provide a higher-level framework for you to build intuitive and understandable models.  

[1] If this seems like familiar terminology, it is likely because these terms correspond to the components of
an Entity-Relation-Attribute model, an extension of the well-known [ER model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model),
in which attributes (properties) also treated as first-class citizens.