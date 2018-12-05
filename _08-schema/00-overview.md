---
title: Overview
keywords: schema
tags: [graql]
summary: "An overview of the schema in a Grakn knowledge graph."
permalink: /docs/schema/overview
---

## Why The Schema?
A Grakn schema is the blueprint of a Grakn knowledge graph. It allows modelling the database to represent the dataset in its most true nature. No vast amount of highly interconnected data can scale without an underlying structure - one that is capable of expressing the complexity of the dataset, is easy to understand, and can be extended programmatically, at runtime. The data stored in a Grakn knowledge graph is no exception.

The schema enforces logical integrity and consistency across the dataset. In other words, it ensures that all data will always conform to the given structure. Any piece of data that violates the schema, stays out of the picture.

A well-constructed schema enables writing intuitive queries. Given such schema, you will often find yourself writing queries that map seamlessly with how you form them as questions in your mind.

Last and certainly not least, the schema sets the basis for performing [automated reasoning](...) over the represented data. It enables the extraction of implicit information from explicitly stored data - a powerful feature of Grakn that facilitates knowledge discovery and implementation of business logic, at the database level.

## Data Model
There are three Grakn Concepts that make up a schema: [Entity](/docs/schema/concepts#entity), [Relationship](/docs/schema/concepts#relationship), and [Attribute](/docs/schema/concepts#attribute).

An **entity** can have attributes and play different roles in different relationships.

An **attribute** can have attributes of its own and also play roles in relationships.

A **relationship** can too have attributes and play different roles in other relationships.

In th next section, by looking at various real-world examples, we will learn how these concepts can be defined in a schema, to represent a dataset.

At last, we have the [**Graql Rules**](/docs/schema/rules). Rules watch for schema-driven patterns in the data and infer queryable conclusions. Rules are one way to perform [automated reasoning](...) in a Grakn knowledge graph.

## (un)Defining the schema programmatically
In this the following sections, we will learn how to define a schema using Graql code in a `schema.gql` file. However, defining a schema can also be done programmatically (at runtime) using one of the Grakn Clients - [Java](/docs/client-api/java), [Python](/docs/client-api/python) and [Node.js](/docs/client-api/nodejs).

## Loading the schema
Once we have defined a schema, the next immediate step will be to load it into Grakn. Learn how to [load the schema via Grakn Console](...).

## Migrating Data
To learn about migrating a pre-existing dataset in CSV, JSON or XML formats to a Grakn knowledge graph, check out the [Migration Mechanism](...) followed by a comprehensive [tutorial](...) in the language of your choice.

## Querying the schema
In the next section we will learn how to [insert](/docs/query/insert-query), [get](/docs/query/get-query), [delete](/docs/query/delete-query), [update](/docs/query/update-data), [aggregate](/docs/query/aggregate-query) and [compute](/docs/query/compute-query) data represented by a schema.

## Summary
The Grakn schema sets the foundation for a Grakn knowledge graph. When modelled thoroughly, the schema provides us with a knowledge graph that benefits from logical integrity, is flexible towards change, capable of automated reasoning, and enables writing intuitive queries.

In the next section, we will learn about the members of a schema - [Concepts](/docs/schema/concepts) and [Rules](/docs/schema/rules).