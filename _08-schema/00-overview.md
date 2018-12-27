---
sidebarTitle: Overview
pageTitle: Schema

permalink: /docs/schema/overview
---

## Why Use a Schema?
A Grakn schema is the blueprint of a Grakn knowledge graph. Using a highly flexible language, we define a schema to model a domain true to nature. Highly interconnected data cannot be stored at scale without an underlying structure - one that is capable of expressing the complexity of the dataset, is easy to understand, and can be extended programmatically, at runtime.

The schema enforces logical integrity and consistency across the dataset. In other words, it ensures that all data will always conform to the given structure. Any attempt to add data that violates the schema will be disallowed.

A well-constructed schema enables writing intuitive queries. Given such schema, you will often find yourself writing queries that map seamlessly with how you form them as questions in your mind.

Last and certainly not least, the schema sets the basis for performing automated reasoning over the represented data. It enables the extraction of implicit information from explicitly stored data - a powerful feature of Grakn that facilitates knowledge discovery and implementation of business logic inside the database.

## Data Model
There are three Grakn Concepts that make up a schema: [Entity](/docs/schema/concepts#entity), [Relationship](/docs/schema/concepts#relationship), and [Attribute](/docs/schema/concepts#attribute).

An **entity** can have attributes and play roles in relationships.

An **attribute** expresses a *value* of a specified *datatype*. It can have attributes of its own and play roles in relationships.

A **relationship** has at least one roleplayer, can have attributes and play roles in other relationships.

In the sections that follow, by looking at various real-world examples, we will learn how these concepts can be defined in a schema to represent a dataset.

Lastly, we have the [**Graql Rules**](/docs/schema/rules). Rules watch for schema-driven patterns in the data and infer queryable conclusions. Rules are one way to perform automated reasoning in a Grakn knowledge graph.

## Type Hierarchy
Besides the modularity that the concept types provide, we can define any concept to subtype another. A concept type that subtypes another, inherits tha attributes owned and roles related to or played by the parent type. Subtyping not only allows us to mirror the true nature of a dataset as perceived in the realword, but also enables automated reasoning.

## (un)Define the schema programmatically
In the following sections, we will learn how to define a schema using Graql code in a `schema.gql` file. However, defining a schema can also be done programmatically (at runtime) using one of the Grakn Clients - [Java](/docs/client-api/java#client-api-method-manipulate-the-schema-programatically), [Python](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) and [Node.js](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query).

## Load the schema
Once we have defined the schema, the next immediate step is to load it into Grakn. Learn how to [load the schema via the Graql Console](/docs/running-grakn/console#console-options).

## Migrate Data
To learn about migrating a pre-existing dataset in CSV, JSON or XML formats to a Grakn knowledge graph, check out the [Migration Mechanism](...) followed by a comprehensive [tutorial](...) in the language of your choice.

## Query the schema
In the next section we will learn how to [insert](/docs/query/insert-query), [get](/docs/query/get-query), [delete](/docs/query/delete-query), [update](/docs/query/update-data), [aggregate](/docs/query/aggregate-query) and [compute](/docs/query/compute-query) data represented by a schema.

## Summary
The Grakn schema sets the foundation for a Grakn knowledge graph. When modelled thoroughly, the schema provides us with a knowledge graph that benefits from logical integrity, is flexible towards change, capable of automated reasoning, and enables writing intuitive queries.

In the next section, we will learn about the members of a schema - [Concept Types](/docs/schema/concepts) and [Rules](/docs/schema/rules).