# Welcome to TypeQL and TypeDB

TypeDB is a new kind of database, utilising type systems to help you break down complex problems
into meaningful and logical systems. Using TypeQL, TypeDB gives you powerful abstractions over low-level
and complex data patterns.

By combining TypeQL and TypeDB, we can close the gap between how you think, and what the database can interpret 
and respond to. TypeDB guarantees data integrity and safety, while enabling data-level inferences within the database
itself. Taken together, this paradigm gives you a new level of expressivity to simplify your work and
tackle domains that seemed impossibly complex before.

## Thinking in TypeQL and TypeDB

The backbone of any TypeDB database is the representation of your domain: the schema.
The schema is made a set of types and rules, which harness object-oriented principles and logical deduction.

Types defined in your schema are structured: some are objects, some represent connections between objects, 
and some are properties. We refer to these as _entity types_ (objects), _relation types_ (connections), and _attribute types_ (properties).  [1]
When a relation type is used to connect types, each type must play a particular role. This is captured using a _role type_.

Rules defined in your schema encode deductive logic: when-then consequences that when applied to your data
generate insights and new facts. Using rules, you can store knowledge directly in the database.

By structuring domain models with these simple constructs, you can build a schema filled with domain-specific terminology and knowledge, 
in a way that is also understood by TypeDB. This also relieves you of the need to think in terms of tables, documents, or vertices/edges, 
and allows you to think at a higher level of abstraction, in a language familiar to you. 
Designing models and managing data at this higher level of abstraction is one of the primary offerings of TypeQL and TypeDB.


## Building with Entity-Relation-Attribute types

Let's look a bit deeper into the building blocks of TypeQL and TypeDB. 

A database is made of schema, and data. Types in the schema are built using subtyping, like in object-oriented
programming languages. Each database comes with some types built in: `entity`, `relation`, and `attribute`, 
which you will extend to create your data model.

What about the data? Well, all data elements loaded into your database are _instances_ of your types. 
Since your types are subtypes of `entity`, `relation`, or `attribute`, each data element will also be an 
(indirect) instance of `entity`, `relation`, or `attribute`. 

This means, each data instance will either be usable as an object (`entity`), a connector (`relation`), or a property (`attribute`) - 
deciding which of these to use when modeling your data is an important task when building your TypeDB schema.

### Entities

Entities are the main, distinguishable objects in _your domain_. Each entity type you create is a subtype the built-in abstract type `entity`. 
Some examples in a social network domain might be `person`, `group`, `school`, etc.

### Relations

Relations are intended to connect data throughout your domain. Each new relation type you create is a subtype of 
the built-in abstract type `relation`. 

In other databases, relations may be implemented with a join table (SQL), or an edge between two vertices (graph databases).
TypeDB relations generalise both: they flexibly relate one, two, or a huge number of data instances at the same time. 

This expanded idea of a relation is more powerful than either SQL or graph relations. However, we can further
improve. If we allow relations to not just specify which instances relate to each other, but also _how_, we can
produce ever better safety guarantees in the database.

We can do this by introducing _role types_. Role types are part of the definition of relation types, 
and essentially define the interface between relations and other types. As role types are always specified as
part of a relation type, they have fully qualified names of `<relation type>:<role type>`.

So if we have the following TypeDB schema:
```typeql
define
  employment sub relation, relates employee, relates employer; 
  person sub entity, plays employment:employee;
  company sub entity, plays employment:employer;
```

we can now create `employment` relations that connect `person` entities to `company` entities. When doing so,
a `person` must play the `employment:employee` role, while the `company` must play the `employment:employer` role. 
We say that the `person` type is a _role player_ for the role type `employment:employee`, and `company` is a role player
for the role type `employment:employer`. 

Which types can be a role player? In TypeDB, entities, relations, and attributes are all equal citizens. 
So, we allow any of these types to be role players!

What this means is that:
  - In the simplest case, relations will connect entities to each other, when the entity plays a relation's role.
  - Relations can connect to attributes, because attributes can also play roles (extremely useful annotating an attribute ownership!)
  - Relations can be nested, because a relation can play a role in another relation.
  - Relations can even relate to themselves!

These are all hugely useful capabilities when developing domain models in your database. 

### Attributes

Attribute types represent the only part of the database that can carry an actual value. They subtype the built-in abstract type `attribute`.

However, attribute types are first-class citizens of TypeDB, not just properties of entities or relations. So how
do we then connect a type to the actual data, the attribute instances? 

To do this, we allow types to "own" or "have" an attribute type, representing a connection from the attribute owner, to the attribute. 

Similarly to what we saw with role types, because all types are equal citizens in TypeQL and TypeDB, any type can be an attribute owner.

This means that:
  - in the simplest case, entities will own attributes
  - relations can own attributes (useful when annotating connections with metadata, lineage, etc.)
  - attributes can even own attributes (can be tricky, but has good use cases such as abbreviations, acronyms, nicknames, etc.)


#### Attribute Instances

In the data, attribute instances in TypeDB are _globally unique by type and value_, and _immutable_.
Being globally unique and immutable means your data is maximally [normalised](https://en.wikipedia.org/wiki/Database_normalization) at all times. 

What does this mean in practice? As an example, in a database of people with ages, there will be at most one instance of 
`age 10`, which can never be changed in-place.

So how do multiple people instances have the same age with value 10? We create an ownership of the `age 10` by each person. 

We do this with a `has`:
```typeql
match 
  $x isa person, has name "Alice"; 
  $y isa person, has name "Jill"; 
insert 
  $x has age 10; 
  $y has age 10;
```

This creates a connection from the person with `name "Alice"` and person with `name "Jill"`, to the attribute `age 10`.
Thus, many people can have the age 10, by creating new connections to the attribute.

Given that attributes are immutable, and shared, it may not look easy to update a person's age! 
However, instead of changing the attribute, we replace the attribute ownership.
```typeql
match $x isa person, has name "Alice", has age $a; $a = 10;
delete $x has $a;
insert $x has age 11;
```

This leaves all the other people unchanged, still having the `age 10` attribute, while just Alice has a new attribute `age 11`.


## Inference 

To further simplify your models, TypeQL and TypeDB offer two types of inference: type inference, and rule inference.

### Type Inference and Inheritance

By basing our models on the Entity-Relation-Attribute model, blended with subtyping, we naturally introduce inheritance: 
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

The following rule, for example, can automatically infer indirect employment based on company ownerships.

```typeql
define
  rule transitive-employment:
  when {
    $parent is company; $child isa company;
    (owner: $parent, owned: $child) isa ownership;
    (employee: $person, employer: $child) isa employment;
  } then {
    (employee: $person, employer: $parent) isa employment;
  };
```

Rules allow you to embed rich domain knowledge in the database, and expose the outcomes as normal data.


## Summary

Hopefully, we have introduced you to the idea of building a database schema out of entity, relation, and attribute types. 
As you start to develop your database, keep this framework in mind and maximise it to build intuitive and understandable
models. Over time, you will see its potential for handling the next level of complexity in your data domain as well.

[1] If this seems like familiar terminology, it is likely because these terms correspond to the components of
an Entity-Relation-Attribute model, an extension of the well-known [ER model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model),
in which attributes (properties) also treated as first-class citizens.
