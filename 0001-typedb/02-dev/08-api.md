---
pageTitle: API & Drivers
keywords: api, typedb, typeql, concept
longTailKeywords: TypeDB API, concept api, client api
Summary: TypeDB API and Drivers description.
---

# API & Drivers

TypeDB servers accept gRPC calls from [TypeDB Clients](../../02-clients/00-clients.md). This connection has "smart" 
client architecture, meaning TypeDB Clients perform validation of queries, load balancing, and some other operations 
transparent for users.

To access all features of TypeDB and TypeDB Clients use the default interface provided by the clients:

* GUI from [TypeDB Studio](../../02-clients/01-studio.md),
* CLI from [TypeDB Console](../../02-clients/02-console.md),
* API from TypeDB Drivers: 
    * [Java](../../02-clients/java/01-java-overview.md) API, 
    * [Python](../../02-clients/python/01-python-overview.md) API, 
    * [Node.js](../../02-clients/node-js/01-node-js-overview.md) API, 
    * or [other clients](../../02-clients/06-other-languages.md).

TypeDB Studio and TypeDB Console control sessions, transactions, and queries, as well as process the responses 
automatically to present the results (in GUI and CLI respectively) to the user. 

<div class="note">
[Note]
Both TypeDB Studio and TypeDB Console built on the base of the Java TypeDB Driver.
</div>

[TypeDB Drivers](../../02-clients/00-clients.md#typedb-drivers) provide greater flexibility and integration with 
popular programming languages/frameworks at the cost of the requirement to perform session, transaction and data 
manipulation manually. To interact with a TypeDB Driver use TypeDB Client API. There are slight differences between 
Client APIs of different TypeDB Clients, including syntax, but they are very similar to each other by design.

Client API provide access to most functions of TypeDB Client and thus — most functions of TypeDB. The following is 
the description of similar parts of APIs of different client. For more information on API methods — use the specific 
TypeDB Driver documentation.

## API structure

Any Client API divided into two big sections:

* Query — classes and methods to connect to a TypeDB Server, manage sessions and transactions, send different types 
  of queries.
* Response — classes to store and provide processing methods for all concepts (types and instances) from a database.

### Query

To send a query to a TypeDB server a TypeDB Client needs to:

* establish a server [connection](01-connect.md#clients),
* open a [Session](01-connect.md#sessions),
* open a [Transaction](01-connect.md#transactions),
* prepare TypeQL query string,
* send the string as a proper typo of query.

These operations are done using the special classes and methods provided by TypeDB Driver. See some examples 
of how to do that with different TypeDB Drivers [Connections](01-connect.md), 
[Sample Application](../01-start/05-sample-app.md) pages, or [TypeDB Clients](../../02-clients) documentation.

All queries are written in TypeQL, but for some languages there are libraries to build the TypeQL queries in a more 
native way. Like TypeQL [library for Java](https://github.com/vaticle/typeql/tree/master/java). 

The exact syntax for these operations might be different in different languages. See the exact TypeDB Client 
documentation for more information: [Java](../../02-clients/java/01-java-overview.md), [Python](../../02-clients/python/01-python-overview.md), 
[Node.js](../../02-clients/node-js/01-node-js-overview.md).

### Response

In response to a query TypeDB server sends a response to the TypeDB Client. Client interprets the response and provides 
either a processed result (TypeDB Studio and TypeDB Console) or a special objects and methods to process the results 
(TypeDB Drivers). For every kind of query there is a predefined type of expected response and objects. 

For more information on types(classes) of available objects and response types see the 
[Response interpretation](07-response.md) page.

For more information on types of response objects and their **methods** please see the [API reference](08-api.md) for 
the specific driver/language type.

## Local and remote methods

Any Client API has two types of methods: 

* local
* remote

The difference is that local concept methods do not require a call to the server, while calls to **remote** methods 
on the Client API must make at least one full round-trip to a TypeDB server to fetch a result. The execution time 
will include at least the network latency between TypeDB Client and TypeDB server.

<div class="note">
[Note]
For example, to make 1,000 Remote Client API calls and with latency (ping) from client to server being 10ms, we would 
spend a total of 10 seconds waiting for network round-trips.

When dealing with large numbers of results, we recommend to use a query to fetch all required information, rather than 
using the Remote methods of Client API.
</div>

Queries always return **local** concepts. Local concepts must be 
[explicitly converted](#converting-local-concepts-to-remote-concepts) to **remote** concepts to make remote **methods** 
available.

### Local concepts

Local concept methods do not perform network operations. Local concepts are not bound to a transaction, so they can 
be safely used even after the transaction, session or client has been closed; however, the information contained may 
go out of date if another transaction modifies the concepts on the server.

In the TypeDB Drivers documentation, the **Local** tag indicates that a method is available on **both** local and 
remote concepts. All other methods are **only** available on remote concepts.

### Remote concepts

The remote concept methods allows a user to make simple requests to the TypeDB server to discover information 
connected to a specific concept, or modify a concept. **All** remote concept operations require a network call to a 
TypeDB server.

Remote concepts must be linked to a **Transaction** in order to make calls. When remote concepts are returned by a 
Transaction method or a Remote Client API method, they will inherit the same Transaction as the transaction/concept 
the method was called on. When the Transaction is closed, the remote concept methods can no longer be used.

Some remote concept methods are update, insert or delete operations, and will therefore fail if used on a concept 
that is linked to a **read** transaction.

<div class="note">
[Warning]
Streamed query or method results (that were already being streamed at the time of remote method call) may or may not 
see updates made using the Client API.
</div>

### Converting Local Concepts to Remote Concepts

All local concepts have the method `asRemote(tx)`, where the `tx` parameter is a Transaction to use for the remote 
concept version of this local concept, and the returned value is the remote concept. See the `asRemote` method 
documentation for more details: 
[Java](../../02-clients/java/04-java-api-ref.md#concept-methods), 
[Python](../../02-clients/python/04-python-api-ref.md#concept-methods), 
[Node.js](../../02-clients/node-js/04-node-js-api-ref.md#concept-methods).
