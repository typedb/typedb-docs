TypeDB Data Model

When approaching building databases with TypeDB, we strongly encourage you to think of the types you define as components of an Entity-Relation-Attribute model. This is an extension of the well-known ER model (https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model), with Attributes also treated as first-class citizens.

We find the Entity-Relation-Attribute model to be the closest approximation of real world domains that need to be represented in the database. It can be a mental shift from thinking of terms of columns, tables, documents, and vertices/edges, but in our experience the end result is that you (the database designer or user) can massively reduce the gap between how you think, and what the database can interpret and respond to. And by adding subtyping and inheritance, we end up with an expressive system that blends the classic idea of typing at the programming language level, seamlessly with entities, relations, and attributes.

Entities

Entities are intended to represent an object in your domain. Importantly, these are the main actors in _your domain_. All entity types subtype the initial type `entity`.

Relations


Relations are intended to interface concepts throughout your domain, and subtype the initial type `relation`. TypeDB relations are actually hyper-relations, meaning they can connect any number of instances at the same time. Compare this to a binary edge in the graph database world, which connects exactly two instances at a time.

How they connect instances together is via _roles_. You can view roles as the interface between relations and role players. So if we have the following:
```
define
  friendship sub relation, relates friend;
  person sub entity, plays friendship:friend;
```

we are now allowed to create `friendship` relations that connect `person` entities to each another via the `friendship:friend` role.

Let's remind ourselves that entities, relations, and attributes are all equal citizens in TypeDB. So, we allow _any_ of these types can play roles!
What this means is that:
In the basic case, relations will connect entities to each other, when the entity plays a relation's role.
Relations can connect to attributes, because attributes can play also roles (this is extremely useful if you need to annotate an attribute ownership!)
Relations are nestable, because a relation can play a role in another relation.
Relations can even relate to themselves!

These facts are all massively useful when developing domain models in your database, and derive from treating all three categories of types equally at the database level.

Attributes

In TypeDB, attributes are the only data that may carry an actual value. Attributes in TypeDB are further globally unique by type and value, and immutable.
As an example, there will only ever be one instance of `age 10` in a database of people with ages, and can never be changed in-place.

So how do multiple people have the same age with value 10? We create an ownership of the age 10 by each person. We do this with a `has`:
`match $x isa person, has name "Alice"; $y isa person, has name "Jill"; insert $x has age 10; $y has age 10;`
This creates a connection from the person with `name "Alice"` and person with `name "Jill"`, to the attribute `age 10`.
Thus, many people can have the age 10, by creating new connections to the attribute.

Given that attributes are immutable, and shared, it may not look easy at first to update a person's age! However, instead of changing the attribute, we replace the attribute ownership.
```
match $x isa person, has name "Alice", as age $a; $a = 10;
delete $x has $a;
insert $x has age 11;
```

This leaves all the other people unchanged, still having the `age 10` attribute, while just Alice has a new attribute `age 11`.

Similarly to what we saw with roles, because of the fact that entities, relations, and attributes are all equal citizens in TypeDB, any of these types can own attributes.
This means that:
in the basic case, entities will own attributes
relations can own attributes (useful when annotating connections)
and even attributes can own attributes (can be tricky to use, but also has good use cases such as abbreviations, acronyms, nicknames, etc.)


Summary

The TypeDB data model is designed to help you, as the user, to work as closely to your domain as possible. To do this, we allow the maximum flexibility of an entity-relation-attribute model,
where each is treated as a first-class citizen of the database. In practice, this means any type can play a relation's role or own an attribute. And when combined with subtyping, we create an amazing breadth of domains
that can be modeled elegantly.

