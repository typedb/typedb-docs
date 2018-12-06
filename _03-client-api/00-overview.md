---
title: Overview
keywords: client
tags: []
summary: ""
permalink: /docs/client-api/overview
---

## What is a Grakn Client?
A Grakn client, along with [Grakn Console](...), is an interface through which we can read from and write to a Grakn knowledge graph. If we are building an application that uses a Grakn knowledge graph as its database, we would need a Grakn client at our application layer to handle the database operations.

In this section and the following pages, we will learn the mechanism that a Grakn client uses to set up communication with the [keyspaces](...) running on the Grakn server as well as the methods available for executing queries and retrieving their answers.

## Architecture
All Grakn clients share a common architecture. Simply put, the main components of a Grakn client are the `client` itself, `session` and `transaction`.

### Client
A client is responsible for connecting to the [Grakn Server](...). This connection would then be used to manage keyspaces and creating sessions.

### Session
A session is responsible for connecting our application to a particular keyspace. This connection would then allow creating transactions. You can think of a session as a two-way long-lasting tunnel that connects our application to a particular keyspace on the Grakn server.

### Transaction
A transaction is responsible for performing write and read operations over both the data instances and schema concepts that exist in a targeted keyspace. When executing a query to retrieve data, an iterator is returned, which can then be consumed to execute a request on the server to return the next concrete result. Simply put, Grakn is lazy in retrieving answers.

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, regardless of their type, contain instances of concepts. We can then use the methods introduced bt the [Concept API](...) to obtain more information about that the targeted node based on its surroundings. Furthermore, the Concept API allows us to traverse the neighbours of specific instance to obtain more insights.

## Best Practices
To avoid running into issues and make the most of using a Grakn client keep in mind the following points.

**Keep one session open per keypsace**. A session creates a local copy of the keyspace. That means, if more than one session is opened on the same keyspace, the changes in one will not be reflected in the others. Therefore, it's best to always keep only one session opened on a particular keyspace.

**Close the session before creating another one on a different keyspace**. Although, it is possible and arguably sensible to have multiple sessions opened on a different keyspace, to utilise resources, it is recommended to keep only one session opened on a Grakn server, at a time.

**Keep number of operations per transaction minimal**. Although, it is technically possible to commit a write transaction once after many operations, it is not recommended. To avoid lengthy rollbacks, running out of memory and conflicting operations, it is best to keep the number of queries per transaction minimal, ideally to one query per transaction.

## Available Clients
Grakn currently supports clients for:
- [Java](/docs/client-api/java)
- [Node.js](/docs/client-api/nodejs)
- [Python](/docs/client-api/python)

## Building Your Own Grakn Client
Grakn clients are built using [gRPC](https://grpc.io/). Creating a new client is a straightforward task. In a blog post, [Joshua Send](https://blog.grakn.ai/@joshuasend) takes us through the process of building the Grakn Client Python as a comprehensive guide for [building a Grakn client of your own](https://blog.grakn.ai/grakn-python-driver-how-to-roll-your-own-b010bbd73023).

## Summary
A Grakn Client is meant to be used at the application layer for the purpose of managing and performing operations over keyspaces that live on the Grakn server.

Next, we will learn about how Grakn Clients are set up and used. Pick a language of your choice to continue - [Java](/docs/client-api/java), [Node.js](/docs/client-api/nodejs) or [Python](/docs/client-api/python).