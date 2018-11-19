---
title: Overview
keywords: graql, overview
tags: [graql]
summary: "An introduction to Graql"
permalink: /docs/query/overview
---

## Graql Instructions
Graql is the language for the Grakn knowledge graph. Whether it's through the [Grakn Console](...) or one of the [Grakn Clients](...), Grakn accepts instructions and provides answers only in its own language - Graql.

**Graql is declarative**. In simple terms, when writing Graql code, you simply describe _what_ you would like to achieve, rather than _how_ it's going to get there. The implementation of a Graql query is hidden under the hood and will never concern you as the developer.

**Graql is intuitive**. Graql queries can look a lot like questions the same way they are formed in your mind, as opposed to a complicated series of statements that are difficult to follow and, at scale, become confusing even for the author. It's important to note that the intuitiveness of a Graql query originates from the [schema](/docs/schema/overview). The better the knowledge graph represents the reality of its dataset via its schema, the more intuitive writing and reading Graql queries become.

In this section, we will learn how a Graql query can be written to:
- [Match](/docs/query/match) specific patterns in the data and its schema
- [Insert](/docs/query/insert) new data into the knowledge graph
- [Get](/docs/query/get) back desrired data/knowledge
- [Aggregate](/docs/query/aggregate) values over a set of data
- [Delete](/docs/query/delete) data from the knowledge graph
- [Compute](/docs/query/compute) distributed analytics over a large set of data
- [Update](/docs/query/update) data

## Graql Answers
Some Graql queries such as `get` are expected to return an answer. The answers are returned in pairs of an instance and its corresponding concept. Both the instance and its concept can then be investigated to find more insights. In a dedicated section, we learn more about the methods available concepts/instances available via Graql answers.

## Summary
Graql is a powerful language that is easy to learn, write and read.

In the next section, we will learn about how it can be used to query and modify the data and the schema concepts.