---
pageTitle: TypeDB Clients
keywords: typedb, client, api, grpc
longTailKeywords: typedb client api, typedb api, client api, typedb client architecture, typedb session, typedb transaction
Summary: All you need to know about the architecture of a TypeDB Client.
---

## What is a TypeDB Client?
A TypeDB client, along with the [TypeDB Console](../03-console/01-console.md) and the [TypeDB Workbase](../07-workbase/00-overview.md), is an interface which we can use to read from and write to a TypeDB knowledge graph. If we are building an application that uses a TypeDB knowledge graph as its database, we would need a TypeDB client at our application layer to handle the database operations.

In this section and the following pages, we learn the mechanism that a TypeDB client uses to set up communication with [databases](../06-management/01-database.md) running on the TypeDB server as well as the methods available for executing queries and retrieving their answers.

## Architecture
All TypeDB Clients share a common architecture. Simply put, the main components of a TypeDB client are the `client` itself, `session` and `transaction`.

### Client
A client is responsible for connecting to the [TypeDB Server](/docs/running-typedb/install-and-run#start-the-typedb-server). We then use this connection to manage databases and open sessions.

### Session
A session is responsible for connecting our application to a particular database. This connection then allows opening transactions to carry out queries. We can think of a session as a two-way long-lasting tunnel that connects our application to a particular database on the TypeDB server.

### Transaction
A transaction is responsible for performing write and read operations over the concept types and instances within the connected database. When executing a query to retrieve data, an iterator is returned, which can then be lazily consumed to execute a request on the server to return the next concrete result.

### Async Queries
Invoking a TypeQL query sends the query to the TypeDB server, where it will be completed in the background. Local processing can take place while waiting for responses to be received.

Queries that return answers, such as [match](/docs/query/match-clause), return them as Futures, Streams or iterators depending on the language. These can then be awaited, or iterated, to retrieve the answers as they are computed.

Queries are always executed on the server in the order they were invoked in the client.

<div class="note">
[Important]
When a transaction is committed or closed, all of its asynchronous queries are completed first.
</div>

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, regardless of their type, all contain concepts. We can then use the methods introduced by the [Concept API](../05-concept-api/00-overview.md) to obtain more information about the retrieved concept and its surroundings. Furthermore, the Concept API allows us to traverse the neighbours of a specific concept instance to obtain more insights.

## Best Practices
To avoid running into issues and make the most out of using a TypeDB client, keep in mind the following points.


**Keep one session open per database per client**. If more than one session is opened on the same database, the changes in one are not reflected in the others. Therefore, it's best to always keep only one session open on a particular database.

**Keep the number of operations per transaction minimal**. Although it is possible to commit a write transaction once after many operations, long transactions can lead to memory issues and computational overheads due to conflicting operations between transactions. It is best to keep the number of queries per transaction minimal, even one query per transaction where feasible. This also makes re-trying transactions that fail due to write-write conflicts much simpler in application code.

**Take advantage of asynchronous queries where possible.** This cuts down and masks network round-trip costs and increases your throughput. For example, if you are performing 10 match queries in a transaction, it's best to send them all to the server _before_ iterating over any of their answers.

## Available Clients
TypeDB currently supports clients for:
- [Java](../04-client-api/01-java.md)
- [Node.js](../04-client-api/03-nodejs.md)
- [Python](../04-client-api/02-python.md)

## Building Your Own TypeDB Client
Creating a new TypeDB client is discussed [here](../04-client-api/04-new-client.md).

## Summary
A TypeDB Client is meant to be used at the application layer for the purpose of managing and performing operations over databases that live on the TypeDB server.

Next, we learn how to set up and use the TypeDB Clients. Pick a language of your choice to continue - [Java](../04-client-api/01-java.md), [Node.js](../04-client-api/03-nodejs.md) or [Python](../04-client-api/02-python.md).
