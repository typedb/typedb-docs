# Welcome to TypeQL and TypeDB

TypeQL and TypeDB redefine the capabilities of a database. We believe that with TypeQL, a powerful, 
yet simple and high-level modeling language, we can massively close the gap between how you think, 
and what the database can interpret and respond to. 

Powered by TypeDB, this new paradigm will help you discover that you can not only more intuitively represent your data, 
but work with domains that were impossibly complex for databases before.

## Thinking in TypeQL and TypeDB

The backbone any TypeDB database is the representation of your domain: the schema - a set of types and rules you define via TypeQL.

The types in your schema are further structured: there are some objects, these objects have some connections between them, 
and they may have some properties. We refer to these as _entities_ (objects), _relations_ (connections), and _attributes_ (properties).  [1]

In practice, each of your user-defined schema types must be a direct or indirect subtype of the built-in types 
`entity`, `relation`, or `attribute`. Role types, part of your specification of relations, enable even finer control over
exactly how schema types may be related to one another. Using these simple constructs, you can build a schema filled 
with domain-specific terminology and knowledge, in a way that is also understood by TypeDB.  

Structuring domain models this way relieves you of the need to think in terms of columns, tables, documents, or vertices/edges, 
and allows you to think at a higher level of abstraction, in a language familiar to you. 
This is fundamentally what TypeQL and TypeDB offer.


## Building with Entity-Relation-Attribute types

To dive a bit deeper, all types in your schema be subtypes of either `entity`, `relation`, or `attribute`.
All data elements in your database will be _instances_ of some of your types. Based on subtyping, each of your data 
elements will also be an (indirect) instance of `entity`, `relation`, or `attribute`.

### Entities

Entities are the main, distinguishable objects in _your domain_. All entity types subtype the abstract type `entity`. 

### Relations

Relations are intended to interface concepts throughout your domain, and subtype the abstract type `relation`. 
TypeDB relations are actually hyper-relations, meaning they can connect any number of instances at the same time. 

Compare this to a binary edge in the graph database world, which connects exactly two instances at a time, or an SQL join table
which joins a fixed number of elements per row.

How relations connect instances together is via their _role types_. You can view roles as the interface between relations and other types. 

So if we have the following:
```typeql
define
  friendship sub relation, relates friend; 
  person sub entity, plays friendship:friend;
```

we can now create `friendship` relations that connect `person` entities to each other via the `friendship:friend` role type. 
We say that the `person` type is a _role player_ for the role type `friendship:friend`.

In TypeDB, entities, relations, and attributes are _all equal citizens_. So, we allow any of these types to be role players!

What this means is that:
  - In the simplest case, relations will connect entities to each other, when the entity plays a relation's role.
  - Relations can connect to attributes, because attributes can also play roles (extremely useful annotating an attribute ownership!)
  - Relations can be nested, because a relation can play a role in another relation.
  - Relations can even relate to themselves!

These are all hugely useful capabilities when developing domain models in your database. 

### Attributes

In TypeDB, attributes are the only data that may carry an actual value. We say that types can "own" or "have" an attribute type. 

Similarly to what we saw with role types, because all types are equal citizens in TypeQL and TypeDB, any type can be an attribute owner.

This means that:
  - in the simplest case, entities will own attributes
  - relations can own attributes (useful when annotating connections with metadata, lineage, etc.)
  - attributes can even own attributes (can be tricky, but has good use cases such as abbreviations, acronyms, nicknames, etc.)

Attributes in TypeDB are  also _globally unique by type and value_, and _immutable_.
Being globally unique and immutable means your data is maximally normalised at all times. 

What does this mean in practice? As an example, in a database of people with ages, there will be at most one instance of 
`age 10`, which can never be changed in-place.

So how do multiple people have the same age with value 10? We create an ownership of the `age 10` by each person. 

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

Given that attributes are immutable, and shared, it may not look easy at first to update a person's age! 
However, instead of changing the attribute, we replace the attribute ownership.
```typeql
match $x isa person, has name "Alice", as age $a; $a = 10;
delete $x has $a;
insert $x has age 11;
```

This leaves all the other people unchanged, still having the `age 10` attribute, while just Alice has a new attribute `age 11`.


## Inference 

To further simplify your models, TypeQL and TypeDB offer two types of inference: type inference, and rule inference.

### Type Inference and Inheritance

By basing our models on the Entity-Relation-Attribute model, blended with subtyping, we naturally introduce inheritance: 
a subtype will inherit properties (such as roles played, and attributes owned) from their parent types. 

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

TypeDB is designed to help you work as closely to your domain as possible. To do this, it gives you the maximum 
flexibility of an entity-relation-attribute model seamlessly blended with subtyping and inheritance, as well as rules. 
With these tools, you will be empowered to build more intuitive and advanced databases than ever before.

[1] If this seems like familiar terminology, it is likely because these terms correspond to the components of
an Entity-Relation-Attribute model, an extension of the well-known [ER model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model),
in which attributes (properties) also treated as first-class citizens.
