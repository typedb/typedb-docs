---
pageTitle: Documentation overview
keywords: typedb, typeql, documentation, overview, introduction
longTailKeywords: documentation overview, learn typedb, learn typeql, typedb schema, typedb data model
summary: A birds-eye view of TypeQL and TypeDB
toc: false
---

# Documentation overview

Every product has a separate documentation block in the navigation menu on the left:

- [TypeDB](../001-typedb-old/01-overview.md) — our main product. It is a strongly typed database.
- [TypeDB Cluster](../05-running-typedb-cluster/01-install-and-run.md) — enterprise version of the database with 
  replication, backups and other premium functions.
- [TypeDB Studio](../07-studio/00-overview.md) — our IDE designed for TypeDB and TypeQL.
- [TypeDB Clients & APIs](../03-client-api/00-overview.md) — ways to communicate with TypeDB.
- [TypeQL](../11-query/00-overview.md) — query language for TypeDB.

At the end of the navigation menu you can find some additional info:

- [Examples](../08-examples/00-overview.md) — examples of TypeDB usage.
- Tutorials — advanced use case tutorials.
- Migrating to TypeDB — materials on migrating from other databases to TypeDB. Including comparison of TypeDB to other 
  popular database types:
  - [SQL](../12-comparisons/00-sql-and-typeql.md)
  - [Semantic web](../12-comparisons/01-semantic-web-and-typedb.md)
  - [Graph](../12-comparisons/02-graph-databases-and-typedb.md)

## Thinking in TypeQL and TypeDB

The backbone of any TypeDB database is the representation of your domain: the [schema](../09-schema/00-overview.md).
A TypeDB schema is the blueprint of a TypeDB knowledge graph. Using [TypeQL](../11-query/00-overview.md) language, we 
define a schema to model a domain true to nature. The schema is made up of a set of types and rules, which harness 
object-oriented principles and logical deduction.

Types defined in a schema are all subtypes of the following basic ones: 
- Entities. Representing the objects in your knowledge domain.
- Relations. Representing n-ary relationships within your domain.
- Attributes. Representing values.

<div class="note">
[Note]
These terms correspond to the components of an Entity-Relation-Attribute model, an extension of the well-known 
[ER model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model), in which attributes (properties) 
also treated as first-class citizens.
</div>

Rules defined in your schema are deductive logic — encoded knowledge about your domain. They are when-then
inferences that when applied to your data generate insights and new facts.
