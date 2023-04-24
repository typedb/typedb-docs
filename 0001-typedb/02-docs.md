---
pageTitle: Documentation overview
keywords: typedb, typeql, documentation, overview, introduction
longTailKeywords: documentation overview, learn typedb, learn typeql, typedb schema, typedb data model
summary: A birds-eye view of TypeQL and TypeDB
toc: false
---

# Documentation overview

This is the TypeDB server documentation section. It has the following sections:

- **Getting started**
  - [Introduction](01-start/01-introduction.md) — a brief description of TypeDB capabilities.
  - [Installation](01-start/02-installation.md) — TypeDB server installation manual.
  - [Quickstart guide](01-start/03-quickstart.md) — a guide to quickly set up a TypeDB database.
  - [IAM schema explanation](01-start/04-iam-schema.md) — a brief description of IAM schema that widely used throughout 
    the documentation.
  - [Sample application](01-start/05-sample-app.md) — a simple example of how to use TypeDB with Java, Python, and 
    Node.js.
- **Development**
  - [Connect](02-dev/01-connect.md) — TypeDB server and database connections
  - [Schema](02-dev/02-schema.md) — types and rules definition
  - [Matching patterns](02-dev/03-match.md) — patterns design and matching data
  - [Writing data](02-dev/04-write.md) — data modification queries
  - [Reading data](02-dev/05-read.md) — data retrieval queries
  - [Inferring data](02-dev/06-infer.md) — data inference queries
  - [Response interpretation](02-dev/07-response.md) — parsing query response
  - [API and Drivers](02-dev/08-api.md) — brief description of Client API and TypeDB Drivers
  - [Best practise](02-dev/09-best.md) — schema and query design tips
- **Administration**
  - [Configuration](03-admin/01-configuration.md) — TypeDB server configuration parameters and how to change 
    configuration
  - [Export and import](03-admin/02-export-import.md) — exporting and importing database schema and data
  - [Upgrading](03-admin/03-update.md) — how to migrate to a newer version of TypeDB
  - [High availability](03-admin/04-ha.md) — description of TypeDB high availability features
  - [Security](03-admin/05-security.md) — description of TypeDB security features
- **Tutorials**
  - [Data migration](04-tutorials/01-data-migration.md) — How to load a dataset from an intermediate input format into 
    TypeDB database

## Thinking in TypeQL and TypeDB

<!-- #todo Change the link to TypeQL --->

The backbone of any TypeDB database is the representation of our domain: the [schema](02-dev/02-schema.md).
A TypeDB schema is the blueprint of a TypeDB database. Using [TypeQL](../11-query/00-overview.md) language, we 
define a schema to model a domain true to nature. The schema is made up of a set of types and rules, which harness 
object-oriented principles and logical deduction.

Types defined in a schema are all subtypes of the following basic ones: 

- Entities. Representing self-sufficient objects.
- Relations. Representing n-ary relationships.
- Attributes. Representing properties with a value: numeric, text string, boolean, or date&time.

<div class="note">
[Note]
These terms correspond to the components of an Entity-Relation-Attribute model, an extension of the well-known 
[ER model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model), in which attributes (properties) 
also treated as first-class citizens.
</div>

Rules defined in a schema represent deductive logic. They are defined as condition (when clause) and conclusion 
(then clause). Read queries with inference option enabled can generate insights based on the deductive logic 
described with rules. Those insights are transaction bound and are not persisted.
