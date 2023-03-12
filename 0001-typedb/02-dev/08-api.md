---
pageTitle: API reference
keywords: api, typedb, typeql, concept, reference
longTailKeywords: TypeDB API, api reference, concept api, client api
Summary: Reference for the TypeDB API.
---

# API reference

## API structure

TypeDB have "smart" client architecture, meaning [TypeDB Clients](../../02-clients/00-clients.md) perform validation 
of queries, load balancing and some other operations transparent for users.

There is a part of TypeDB API that is specific for every TypeDB Client. It's called TypeDB Client API.

But there is a common part of TypeDB API that sometimes called the TypeDB Concept API.

## Concept Architecture

Anything in TypeDB (other than [Rule](../../09-schema/03-rules.md)), whether a concept type or a data instance, is a 
[Concept](../../04-concept-api/01-concept.md). The diagram below, illustrates how the Concept superclass is 
inherited by 
its direct and indirect descendants.

![Concept Hierarchy](../../images/client-api/overview_hierarchy.png)

**Type** refers to a Concept Type as defined in the [schema](../../09-schema/00-overview.md#typedb-data-model).

**Thing** refers to an instance of data that is an instantiation of a Concept Type.

## Local and Remote Concept API

The Concept API architecture is implemented in 2 ways in each client: **local** and **remote**. The concepts share the same overall structure, but only a small set of methods are available on the *local* concepts.

The difference is that local concept methods do not require a call to the server, while calls to methods on the *remote* concept API must make at least one full round-trip to the server to fetch a result. The execution time will include at least the network latency between your client and the TypeDB server.

<div class="note">
[Note]
As an example, if you were to make 1,000 Remote Concept API calls and your latency (ping) from client to server is 10ms, you would spend a total of 10 seconds waiting for network round-trips.

Where efficiency is a concern, especially when dealing with large numbers of results, we recommend that you include the required information to fetch in the query, rather than using the Remote Concept API.
</div>

Queries always return local concepts. Local concepts must be [converted](#converting-local-concepts-to-remote-concepts) to remote concepts before remote methods are available.

### Local Concept API

Local Concept methods do not perform network operations. Local concepts are not bound to a transaction, so they can be safely used even after the transaction, session or client has been closed; however, the information contained may go out of date if another transaction modifies the Concepts on the server.

In the Concept API documentation, the **(Local)** tag indicates that a method is available on *both local and remote* concepts. All other methods are only available on remote concepts.

### Remote Concept API

The remote concept API allows a user to make simple requests to the TypeDB server to discover information connected to a specific concept, or modify a concept. **All** remote concept operations require a network call to the TypeDB server.

Remote concepts must be linked to a **Transaction** in order to make calls. When remote concepts are returned by a Transaction method or a Remote Concept API method, they will inherit the same Transaction as the transaction/concept the method was called on. *When the Transaction is closed, the remote concept methods can no longer be used.

Some remote concept methods are update, insert or delete operations, and will therefore fail if used on a concept that is linked to a *read* transaction.

<div class="note">
[Important]
The interaction behaviour between remote concepts and results streaming is not well defined: this means that streamed query or method results may or may not see updates made using the concept API.
</div>

### Converting Local Concepts to Remote Concepts

All local concepts have the method `asRemote(tx)`, where the `tx` parameter is a Transaction to use for the remote concept version of this local concept, and the returned value is the remote concept. See the `asRemote` method documentation for more details.

In the sections that follow, we learn about the methods available on [Concept](../../04-concept-api/01-concept.md), 
[Type](../../04-concept-api/02-type.md#type-methods), [ThingType](../../04-concept-api/02-type.md#thingtype-methods), 
[EntityType](../../04-concept-api/02-type.md#entitytype-methods), 
[AttributeType](../../04-concept-api/02-type.md#attributetype-methods), 
[RelationType](../../04-concept-api/02-type.md#relationtype-methods), 
[RoleType](../../04-concept-api/02-type.md#roletype-methods), 
[Thing](../../04-concept-api/04-thing.md#thing-methods), 
[Attribute](../../04-concept-api/04-thing.md#attribute-methods), 
[Relation](../../04-concept-api/04-thing.md#relation-methods) and [Rule](../../04-concept-api/03-rule.md).
