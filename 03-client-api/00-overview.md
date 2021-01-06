---
pageTitle: Grakn Clients
keywords: grakn, client, api, grpc
longTailKeywords: grakn client api, grakn api, client api, grakn client architecture, grakn session, grakn transaction
Summary: All you need to know about the architecture of a Grakn Client.
---

## What is a Grakn Client?
A Grakn client, along with the [Grakn Console](../02-running-grakn/02-console.md) and the [Grakn Workbase](../07-workbase/00-overview.md), is an interface which we can use to read from and write to a Grakn knowledge graph. If we are building an application that uses a Grakn knowledge graph as its database, we would need a Grakn client at our application layer to handle the database operations.

In this section and the following pages, we learn the mechanism that a Grakn client uses to set up communication with [databases](../06-management/01-database.md) running on the Grakn server as well as the methods available for executing queries and retrieving their answers.

## Architecture
All Grakn Clients share a common architecture. Simply put, the main components of a Grakn client are the `client` itself, `session` and `transaction`.

### Client
A client is responsible for connecting to the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server). We would then use this connection to manage databases and open sessions.

### Session
A session is responsible for connecting our application to a particular database. This connection would then allow opening transactions to carry out queries. We can think of a session as a two-way long-lasting tunnel that connects our application to a particular database on the Grakn server.

### Transaction
A transaction is responsible for performing write and read operations over the concepts types and instances within the connected database. When executing a query to retrieve data, an iterator is returned, which can then be lazily consumed to execute a request on the server to return the next concrete result.

### Futures and Async Queries
Queries can be computed asynchronously on the grakn server whilst local processing takes place. In order to execute async queries, clients may wrap the result in an async task wrapping object, such as a Promise or Future, depending on the convention in the given language. 

<div class="note">
[Important]
When a transaction is committed or closed, all currently processing asynchronous queries are completed first.
</div>

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, regardless of their type, all contain concepts. We can then use the methods introduced by the [Concept API](../04-concept-api/00-overview.md) to obtain more information about the retrieved concept and its surroundings. Furthermore, the Concept API allows us to traverse the neighbours of a specific concept instance to obtain more insights.

## Best Practices
To avoid running into issues and make the most out of using a Grakn client, keep in mind the following points.

**Keep one session open per database per client**. A session creates a local copy of the database. That means, if more than one session is opened on the same database, the changes in one is not reflected in the others. Therefore, it's best to always keep only one session open on a particular database.

**Keep the number of operations per transaction minimal**. Although it is possible to commit a write transaction once after many operations, long transactions can lead to memory issues and computational overheads due to conflicting operations between transactions. It is best to keep the number of queries per transaction minimal, even one query per transaction where feasible. This also makes re-trying transactions that fail due to write-write conflicts much simpler in application code.

**Take advantage of asynchronous queries where possible.** This cuts down and masks network round-trip costs and increases your throughput. All queries can safely be made asynchronous, as async queries within a transaction are executed sequentially on the server-side.

## Available Clients
Grakn currently supports clients for:
- [Java](../03-client-api/01-java.md)
- [Node.js](../03-client-api/03-nodejs.md)
- [Python](../03-client-api/02-python.md)

## Building Your Own Grakn Client
Creating a new Grakn client is discussed [here](../03-client-api/04-new-client.md).

## Summary
A Grakn Client is meant to be used at the application layer for the purpose of managing and performing operations over databases that live on the Grakn server.

Next, we learn how to set up and use the Grakn Clients. Pick a language of your choice to continue - [Java](../03-client-api/01-java.md), [Node.js](../03-client-api/03-nodejs.md) or [Python](../03-client-api/02-python.md).
