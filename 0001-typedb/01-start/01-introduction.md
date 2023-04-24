---
pageTitle: TypeDB introduction
keywords: typedb, database, documentation, introduction, overview
longTailKeywords: typedb introduction, typedb overview, learn typedb, learn typeql, typedb schema, typedb data model
summary: A birds-eye view of TypeDB.
toc: false
---

# TypeDB introduction

## Brief intro

TypeDB:

- Is a strongly typed database. Unique in many ways:
  - Has its own special [strong type system](../02-dev/02-schema.md#types). Supports subtyping and inheritance like 
    object-oriented programming languages.
  
  <!--- #todo add link to the types article -->
  - Uses [Entity-Relationship model](../02-dev/02-schema.md#entity-types), extended with 
    [Attributes](../02-dev/02-schema.md#attribute-types) and Rules.
  - Uses declarative queries with its own query language: [TypeQL](../02-dev/03-match.md#patterns-overview). We set the 
    requirements for results but not how to achieve it.
- Is a transactional ([OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing)) database with 
  [ACID](../02-dev/01-connect.md#acid-guarantees) guarantees.
- Has data separated by [databases](../02-dev/01-connect.md#databases), each one having its own 
  [schema](../02-dev/02-schema.md).

Comparison of TypeDB with most common types of databases:
- [SQL](../../12-comparisons/00-sql-and-typeql.md)
- [Semantic web](../../12-comparisons/01-semantic-web-and-typedb.md)
- [Graph](../../12-comparisons/02-graph-databases-and-typedb.md)

We have prepared a [Quickstart guide](../01-start/03-quickstart.md) to start with some practice and deploy an 
environment for exploring TypeDB.

## Introduction

TypeDB is a new kind of database, that utilizes type systems to help us break down complex problems into a meaningful 
and logical system. Its own query language, TypeQL, gives us powerful abstractions over low-level and complex data 
patterns. By combining TypeQL and TypeDB, we can close the gap between the language of our domain, and what the 
database can interpret and respond to.

TypeDB guarantees data integrity and safety while enabling data-level inferences within the database. This new paradigm 
gives a higher level of expressivity to simplify our work and tackle domains that seemed impossibly complex before.

TypeQL and TypeDB allow us to build a data model out of entity, relation, and attribute types. Inheritance allows 
subtypes to be defined simply and reduce complexity, while roles and rules further enhance our schema. These 
abstractions provide a higher-level framework to build intuitive and understandable models.

We can use the power of [hypergraphs](https://en.wikipedia.org/wiki/Hypergraph) 
without the need to understand graphs! In other databases, relations may be implemented with a join table 
([SQL](../../12-comparisons/00-sql-and-typeql.md)), or an edge between two vertices 
([graph](../../12-comparisons/02-graph-databases-and-typedb.md) databases). TypeDB relations generalize both: they 
flexibly relate one, two, or any number of data instances at the same time.

This expanded idea of a relation is more powerful than either SQL or graph relations. However, we can further
improve: if we allow relations to not just specify which instances relate to each other, but also _how_ by adding
context.
