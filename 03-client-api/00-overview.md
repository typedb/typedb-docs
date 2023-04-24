---
pageTitle: TypeDB Clients
keywords: typedb, client, api, grpc
longTailKeywords: typedb client api, typedb api, client api, typedb client architecture, typedb session, typedb transaction
Summary: All you need to know about the architecture of a TypeDB Client.
---

## Start Developing with TypeDB

The following TypeDB client libraries are officially supported and actively maintained by Vaticle. They support new
TypeDB features and receive continuous bug fixes and improvements.

- [**Java**](../02-clients/java/01-java-overview.md)
- [**Node.js**](../02-clients/node-js/01-node-js-overview.md)
- [**Python**](../02-clients/python/01-python-overview.md)
- [**Other Languages**](../02-clients/06-other-languages.md)

## What is a TypeDB Client?
A TypeDB client, along with the [TypeDB Console](../02-console/01-console.md) and [TypeDB Studio](../07-studio/00-overview.md), 
is an interface which we can use to read from and write to a TypeDB knowledge graph. If we are building an application 
that uses a TypeDB knowledge graph as its database, we would need a TypeDB client at our application layer to handle the 
database operations.

![Structure of a TypeDB Client Application](../images/client-api/client-server-comms.png)

In this section and the following pages, we learn the mechanism that a TypeDB client uses to set up communication with [databases](../06-management/01-database.md) running on the TypeDB server as well as the methods available for executing queries and retrieving their answers.

## Architecture
All TypeDB Clients share a common architecture. Simply put, the main components of a TypeDB client are the `client` 
itself, `session` and `transaction`.

### Client
A client is responsible for connecting to the [TypeDB Server](/docs/typedb/install-and-run#start-the-typedb-server). We then use this connection to manage databases and open sessions. 

**Best Practices**

Use one client per application process.

### Session
A session holds a connection to a particular database. This connection then allows opening transactions to carry out queries. 

**Best Practices**

Because of intermittent network failures, it is recommended to keep sessions relatively short-lived. 
A good principle is that sessions group logically coherent transactions. For example, when loading a web page, one session should be used to open one or more transactions to load the page data.

### Transaction
A transaction performs queries or Concept API calls on the database. TypeDB transactions comply with [ACID](../06-management/02-acid.md) properties, up to snapshot isolation. 

Transactions automatically close after a configured timeout (default 5 minutes). This is to encourage shorter-lived transactions,
prevent memory leaks caused by forgotten unclosed client-side transactions, and kill potentially unresponsive transactions.

**Best Practices**

Keep transactions generally short-lived. Long-lived transactions are more likely to clash with others when committing, and pin resources in the server.

A good principle is that transactions group logically coherent queries. For example, when building an e-commerce platform, loading a user's purchase history page could be done using two transactions: one for retrieving the purchases, and another for retrieving the user's profile.

However, when leveraging the TypeDB reasoning engine, it is sometimes beneficial to reuse the same read transactions to warm up the reasoning caches.

### Async Queries
Invoking a TypeQL query sends the query to the TypeDB server, where it will be completed in the background. Local processing can take place while waiting for responses to be received. Take advantage of these asynchronous queries to mask network round-trip costs and increases your throughput. For example, if you are performing 10 match queries in a transaction, it's best to send them all to the server _before_ iterating over any of their answers.

Queries that return answers, such as [match](../11-query/01-match-clause.md), return them as Futures, Streams or Iterators depending on the language. These can then be awaited, or iterated, to retrieve the answers as they are computed.

<div class="note">
[Important]
When a transaction is committed or closed, all of its asynchronous queries are completed first.
</div>

### Investigating Answers
Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, regardless of their type, all contain concepts. We can then use the methods introduced by the [Concept API](../04-concept-api/00-overview.md) to obtain more information about the retrieved concept and its surroundings. Furthermore, the Concept API allows us to traverse the neighbours of a specific concept instance to obtain more insights.

## Summary
A TypeDB Client is meant to be used at the application layer for the purpose of managing and performing operations over databases that live on the TypeDB server.

Next, we learn how to set up and use the TypeDB Clients. Pick a language of your choice to continue - [Java](../02-clients/java/01-java-overview.md), [Node.js](../02-clients/node-js/01-node-js-overview.md) or [Python](../02-clients/python/01-python-overview.md).
