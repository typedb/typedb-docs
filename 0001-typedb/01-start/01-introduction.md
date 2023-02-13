---
pageTitle: TypeDB Introduction
keywords: typedb, database, documentation, introduction, overview
longTailKeywords: typedb introduction, typedb overview, learn typedb, learn typeql, typedb schema, typedb data model
summary: A birds-eye view of TypeDB
toc: false
---

# TypeDB Introduction

## Brief intro

TypeDB:

- Is a strongly typed database. Unique in many ways:
  - Has its own special [strong type system](../04-concept-api/00-overview.md). Supports subtyping and inheritance like 
    object-oriented programming languages.
  
  <!--- #todo add link to the types article -->
  - Uses [Entity-Relationship model](../09-schema/00-overview.md#typedb-data-model), extended with Attributes and Rules.
  - Uses its own query language: [TypeQL](../11-query/00-overview.md).
  - Queries are declarative: you set the requirements for results but not how to achieve it.
- Is a transactional ([OLTP](https://en.wikipedia.org/wiki/Online_transaction_processing)) database.
- Has data separated by [databases](02-fundamentals/02-database.md), each one having its own [schema](../09-schema/00-overview.md).

You can find interesting a comparison with most common types of databases:
- [SQL](../12-comparisons/00-sql-and-typeql.md)
- [Semantic web](../12-comparisons/01-semantic-web-and-typedb.md)
- [Graph](../12-comparisons/02-graph-databases-and-typedb.md)

We have prepared a [Quickstart guide](../001-typedb/03-quickstart.md) if you want to start with some practice.

## Introduction

TypeDB is a new kind of database, that utilizes type systems to help you break down complex problems into a meaningful 
and logical system. Its own query language, TypeQL, gives you powerful abstractions over low-level and complex data 
patterns. By combining TypeQL and TypeDB, we can close the gap between the language of your domain, and what the 
database can interpret and respond to.

TypeDB guarantees data integrity and safety while enabling data-level inferences within the database. This new paradigm 
gives you a higher level of expressivity to simplify your work and tackle domains that seemed impossibly complex before.

TypeQL and TypeDB allow you to build a data model out of entity, relation, and attribute types. Inheritance allows 
subtypes to be defined simply and reduce complexity, while roles and rules further enhance your schema. These 
abstractions provide a higher-level framework for you to build intuitive and understandable models.

You can use the power of [hypergraphs](../12-comparisons/02-graph-databases-and-typedb.md#hypergraph-theory) 
without the need to understand graphs! In other databases, relations may be implemented with a join table 
([SQL](../12-comparisons/00-sql-and-typeql.md)), or an edge between two vertices 
([graph](../12-comparisons/02-graph-databases-and-typedb.md) databases). TypeDB relations generalize both: they 
flexibly relate one, two, or any number of data instances at the same time.

This expanded idea of a relation is more powerful than either SQL or graph relations. However, we can further
improve: if we allow relations to not just specify which instances relate to each other, but also _how_ by adding
context.
