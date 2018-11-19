---
title: Overview
keywords: client
tags: []
summary: ""
permalink: /docs/client-api/overview
---

## What is a Grakn Client?
A Grakn client, along with [Grakn Console](...), is an interface through which we can read from and write to a Grakn knowledge graph. If we are building an application that uses a Grakn knowledge graph as its database, we would need a Grakn client at our application layer to handle the database operations.

In this section and the following pages, we will learn the mechanism that a Grakn client uses to set up communication with the Grakn server as well as the methods available for executing queries and retrieving their answers.

## Architecture
All Grakn clients share a common architecture. Simply put, the main components of a Grakn client are `client`, `session` and `transaction`.

### Client
A client is responsible for connecting to the [Grakn Server]. This connection would then allow to manage the keyspaces and creating a session.

### Session
A session is responsible for connecting to a particular keyspace. This connection would then allows to create transactions. You can think of a session as a two-way long-lasting tunnle that connects our application to a particular keyspace on Grakn server.

### Transaction
A transaction is responsible for performing write and read operations over both the data instances and schema elements that exist in the targetted keyspace. When exectuting a query to retrieve data, an iterator is returned, which can then be consumed to exectute a request on the server to return the next concrete result. Simply put, Grakn is lazy in retrieving answers.

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers.

To obtain more relevant information about a specific answer, we use the [Concept API](). The methods available on different types of instance and schema elements provide insights originating from a specific node as well as the ability to manipulate its surrounding neighbours.

## Best Practices
To avoid running to issues and make the most of using a Grakn client keep in mind the following points.

**Keep one session open per keypsace**. A session creates a local copy of the keyspace. That means, if more than one session is opened on one keyspace, the changes in one will not be reflected in the others. Therefore, it's best to always keep only one session opened on a particular keyspace.

**Close the session before creating another one on a different keyspace**. Although, it is possible and arguable sensible to have multiple sessions, each opened on a different keyspace, to utilise resources, it's recomonded to keep only one session opened on one server instance.

**Keep number of operations per transaction minimal**. Although, it is technically possible to commit a write transaciton after executing a large number of queries in a single transaction, it is not recommonded. To avoid lengthy rollbacks, running out of memory and conflicting operations, it is best to keep the number of queries per transaction minimal, idealy to one query per transaction.

## Available Clients
Grakn currently supports clients for:
- [Java](/docs/client-api/java)
- [Node.js](/docs/client-api/nodejs)
- [Python](/docs/client-api/python)

## Building Your Own Grakn Client
Grakn clients are built using [gRPC](https://grpc.io/). Creating a new client is a straightfowrard task. In a blog post, [Joshua Send](https://blog.grakn.ai/@joshuasend) takes us through the process of building the Grakn Client Python and a comprehensive guide for [building a Grakn client of your own](https://blog.grakn.ai/grakn-python-driver-how-to-roll-your-own-b010bbd73023).

## Summary
A Grakn Client is meant to be used at the application layer for the purpose of  performing operations over a keyspace that lives on the Grakn server.

Next, we will learn about how Grakn Clients are setup and used at the application layer. Pick a language of your choice to continue - [Java](/docs/client-api/java), [Node.js](/docs/client-api/nodejs) or [Python](/docs/client-api/python).