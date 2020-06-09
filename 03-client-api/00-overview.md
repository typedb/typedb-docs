---
pageTitle: Grakn Clients
keywords: grakn, client, api, grpc
longTailKeywords: grakn client api, grakn api, client api, grakn client architecture, grakn session, grakn transaction
Summary: All you need to know about the architecture of a Grakn Client.
---

## What is a Grakn Client?
A Grakn client, along with the [Grakn Console](../02-running-grakn/02-console.md) and the [Grakn Workbase](../07-workbase/00-overview.md), is an interface which we can use to read from and write to a Grakn knowledge graph. If we are building an application that uses a Grakn knowledge graph as its database, we would need a Grakn client at our application layer to handle the database operations.

In this section and the following pages, we learn the mechanism that a Grakn client uses to set up communication with [keyspaces](../06-management/01-keyspace.md) running on the Grakn server as well as the methods available for executing queries and retrieving their answers.

## Architecture
All Grakn Clients share a common architecture. Simply put, the main components of a Grakn client are the `client` itself, `session` and `transaction`.

### Client
A client is responsible for connecting to the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server). We would then use this connection to manage keyspaces and open sessions.

### Session
A session is responsible for connecting our application to a particular keyspace. This connection would then allow opening transactions to carry out queries. We can think of a session as a two-way long-lasting tunnel that connects our application to a particular keyspace on the Grakn server.

### Transaction
A transaction is responsible for performing write and read operations over the concepts types and instances within the connected keyspace. When executing a query to retrieve data, an iterator is returned, which can then be lazily consumed to execute a request on the server to return the next concrete result.

### Futures and Async Queries
Queries can be computed asynchronously on the grakn server whilst local processing takes place. In order to execute async queries, clients may wrap the result in an async task wrapping object, such as a Promise or Future, depending on the convention in the given language. When a transaction is committed or closed, all currently processing asynchronous queries are completed first.

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, regardless of their type, all contain concepts. We can then use the methods introduced by the [Concept API](../04-concept-api/00-overview.md) to obtain more information about the retrieved concept and its surroundings. Furthermore, the Concept API allows us to traverse the neighbours of a specific concept instance to obtain more insights.

## Best Practices
To avoid running into issues and make the most out of using a Grakn client, keep in mind the following points.

**Keep one session open per keypsace per client**. A session creates a local copy of the keyspace. That means, if more than one session is opened on the same keyspace, the changes in one is not reflected in the others. Therefore, it's best to always keep only one session open on a particular keyspace.

**Close the session on keyspace A before creating another one on keyspace B**. Although it is possible and arguably sensible to have multiple sessions opened on different keyspaces, to utilise resources, it is recommended to keep only one session opened at a time on a Grakn server.

**Keep the number of operations per transaction minimal**. Although it is technically possible to commit a write transaction once after many operations, it is not recommended. To avoid lengthy rollbacks, running out of memory and conflicting operations, it is best to keep the number of queries per transaction minimal, ideally to one query per transaction.

**Take advantage of asynchronous queries where possible.** This cuts down on network round-trip time and increase your throughput where possible. All queries can safely be made asynchronous, as they will automatically wait for previous queries to finish on the server-side.

## Available Clients
Grakn currently supports clients for:
- [Java](../03-client-api/01-java.md)
- [Node.js](../03-client-api/03-nodejs.md)
- [Python](../03-client-api/02-python.md)

## Building Your Own Grakn Client
Creating a new Grakn client is discussed [here](../03-client-api/04-new-client.md).

## Summary
A Grakn Client is meant to be used at the application layer for the purpose of managing and performing operations over keyspaces that live on the Grakn server.

Next, we learn how to set up and use the Grakn Clients. Pick a language of your choice to continue - [Java](../03-client-api/01-java.md), [Node.js](../03-client-api/03-nodejs.md) or [Python](../03-client-api/02-python.md).