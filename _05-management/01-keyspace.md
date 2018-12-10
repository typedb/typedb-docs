---
title: Keyspace
keywords:
tags: []
summary: ""
permalink: /docs/management/keyspace
---

## What is a Keyspace?
A keyspace is the outermost container for data in a Grakn knowledge graph, corresponding closely to a relational _database_. As per a relational database, it is commonly known to be good practice to create a single keyspace per application, but it is absolutely fine to create as many keyspaces as your application needs. As a rule of thumb, it is recommended to start off with one keyspace and create more if the requirement arises.

Keyspaces are isolated from one another. Even when running on the same Grakn Server, it is not possible to perform operations from one keyspace on another one.

### Creating a Keyspace
We can create a new a keyspace via the Grakn Clients [Java](/docs/client-api/java#client-api-method-creating-a-session/keyspace), [Node.js](/docs/client-api/nodejs#client-api-method-creating-a-session/keyspace) and [Python](/docs/client-api/python#client-api-method-creating-a-session/keyspace), as well as [Workbase]() and [Graql Console](/docs/running-grakn/console#selecting/creating-a-keyspace).

### Listing All Keyspaces
We can list all keyspaces of the running Grakn server via the Grakn Clients [Node.js](/docs/client-api/nodejs#client-api-method-deleting-a-keyspace) and [Python](/docs/client-api/python#client-api-method-deleting-a-keyspace), as well as [Workbase]().

### Cleaning a Keyspce
Cleaning the keyspace, to not be confused with deletion, wipes out both the data and the schema contained within the keyspace. We can clean a keyspace via [Graql Console](/docs/running-grakn/console#deleting-the-entire-knowledge-graph)

### Deleting a Keyspace
We can delete a keyspace via the Grakn Clients [Java](/docs/client-api/java#client-api-method-deleting-a-keyspace), [Node.js](/docs/client-api/nodejs#client-api-method-deleting-a-keyspace) and [Python](/docs/client-api/python#client-api-method-deleting-a-keyspace), as well as [Workbase]().

### Renaming a Keyspace
Once a keyspace has been created, its name can no longer be changed. The only way to achieve a renamed keyspace is to migrate the data from the keyspace with the old name to the newly created one.