---
title: Overview
keywords: schema
tags: [graql]
summary: "An overview of Schema in a Grakn knowledge graph."
permalink: /docs/schema/overview
---

## Motivation
A Grakn Schema is the blueprint of a Grakn knowledge graph. It allows you to model the knowledge graph in order to represent the dataset in its most true nature. No database can scale without an underlying structure and a Grakn knowledge graph is no exception.

The schema enforces logical integrity and consistency across the dataset. In other words, it ensures that all data will always conform to the given structure. Any piece of data that violates the schema stays out of the picture.

A well-constructed schema enables writing intuitive queries. Given such schema, you will often find yourself writing queries that map seamlessly with how you form their corresponding question in mind.

Last and certainly not least, the schema sets the basis for [automated reasoning](...) over the represented data. It enables the extraction of implicit information from explicitly stored data - an extreamly powerful feature of Grakn that results in storing contexualised knowlwedge as opposed to raw data.

## Data Model
There are three Grakn Concepts that make up a schema: [Entity](/docs/schema/concepts#entity), [Relationship](/docs/schema/concepts#relationship), and [Attribute](/docs/schema/concepts#attribute). With these concepts and the interaction they have with each other, one can model any dataset as perceived in the real world.

An entity can have an attribute and play a role in a relationship.
An attribute can have an attribute of its own and also play a role in a relationship.
A relationship can also have an attribute and any number of roleplayers which can be entities, attributes or even other relationships.

At last, we have the [Graql Rules](/docs/schema/rules). A simple yet extreamly powerful tool that allows us to build an intelligent database for an intelligent system. Rules are one way to perform [automated reasoning](...) in a Gtakn knowledge graph.

## Defining the Schema programmatically
In this section, we will learn how to define a schema using Graql code in a `schema.gql` file. However, defining a schema can also be done programmatically (at runtime) using one of the Grakn Clients - [Java](...), [Python](...) and [Node.js](...).


## Loading the Schema
Once we have defined a schema, the next immediate step will be to load that schema into Grakn. Learn how this is done using the Grakn Console <<link>>.

## Querying the Schema
Once we have loaded the schema into Grakn, we are able to [query the schema](...) as we wish.

## Migrating Data
To learn how to migrate a pre-existing dataset in CSV, JSON or XML format into a Grakn knowledge graph, check out the [Migration Mechanism](...) followed by a comprehensive [tutorial](...) in the language of your choice.