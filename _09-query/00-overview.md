---
title: Overview
keywords: graql, overview
tags: [graql]
summary: "An introduction to Graql"
permalink: /docs/query/overview
---

## Graql Instructions
Graql is the language for the Grakn knowledge graph. Whether it's through the [Grakn Console](...) or one of the [Grakn Clients](/docs/client-api/overview), Grakn accepts instructions and provides answers only in its own language - Graql.

**Graql is declarative**. In simple terms, when writing Graql code, you simply describe _what_ you would like to achieve, rather than _how_ it's going to get there. The implementation of a Graql query is hidden under the hood and will never affect you as the developer.

**Graql is intuitive**. Graql queries can look a lot like questions the same way as they are formed in mind, as opposed to a complicated series of statements that are difficult to follow and, at scale, become confusing even to the author. It's important to note that the intuitiveness of a Graql query originates from the [schema](/docs/schema/overview). The better the knowledge graph represents the reality of its dataset via its schema, the more intuitive writing and reading Graql queries become.

In this section, we will learn how a Graql query can be written to:
- [Match](/docs/query/match) specific patterns in the data and schema
- [Insert](/docs/query/insert) new data into the knowledge graph
- [Get](/docs/query/get) back desrired data/knowledge
- [Aggregate](/docs/query/aggregate) values over a set of data
- [Delete](/docs/query/delete) data from the knowledge graph
- [Compute](/docs/query/compute) distributed analytics over a large set of data
- [Update](/docs/query/update) data

## Graql Answers
Some Graql queries such as `get`, `aggregate` and `compute` are expected to return an answer. Depending on the type of query, the data structure of the answer may be different (more on Answer types in the [Client API](/docs/client-ap) section). As a part of the [Concept API](...), various methods can be called on the concepts contained in an answer to retrieve more explicit and implicit knowledge about their surrounding concepts.

## Summary
Graql is a powerful language that is easy to learn, write and read.

In the sections that follow, we will learn about how we can use Graql to query and modify the data instances as well as the underlying schema.