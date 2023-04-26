---
pageTitle: Client Node.js
keywords: typedb, client, node.js
longTailKeywords: typedb node.js client, typedb client node.js, client node.js, python node.js
Summary: API Reference of TypeDB Client Node.js.
---

## Installation

#### To use this client, you need a compatible TypeDB Server running. Visit our [Compatibility Table](#version-compatibility)

```
npm install typedb-client
```

### Resources

- [Client Node.js on GitHub](https://github.com/vaticle/typedb-client-nodejs)
- [Releases](https://github.com/vaticle/typedb-client-nodejs/releases)
- [Examples](https://github.com/vaticle/typedb-examples)

## Quickstart

First make sure that the [TypeDB server](/docs/running-typedb/install-and-run#start-the-typedb-server) is running.

In your source, require `typedb-client`.

<!-- test-example socialNetworkNodejsClientA.js -->
```javascript
const {TypeDB} = require("typedb-client");
```

Instantiate a client and open a session.

<!-- test-example socialNetworkNodejsClientB.js -->
```javascript
const {TypeDB, SessionType} = require("typedb-client");

async function openSession(database) {
    const client = TypeDB.coreClient("localhost:1729");
    const session = await client.session(database, SessionType.DATA);
    // session is open
    await session.close();
    //session is closed
    client.close();
};

openSession("social_network");
```

Create transactions to use for reading and writing data.

<!-- test-example socialNetworkNodejsClientC.js -->
```javascript
const {TypeDB, SessionType, TransactionType} = require("typedb-client");

async function createTransactions(database) {
    const client = TypeDB.coreClient("localhost:1729");
    const session = await client.session(database, SessionType.DATA);

    // creating a write transaction
    const writeTransaction = await session.transaction(TransactionType.WRITE); // write transaction is open
    // to persist changes, write transaction must always be committed/closed
    await writeTransaction.commit();

    // creating a read transaction
    const readTransaction = await session.transaction(TransactionType.READ); // read transaction is open
    // read transaction must always be closed
    await readTransaction.close();
    // a session must always be closed
    await session.close();
    // a client must always be closed
    client.close();
}

createTransactions("social_network");
```

Running basic retrieval and insertion queries.

<!-- test-example socialNetworkNodejsClientD.js -->
```javascript
const {TypeDB, SessionType, TransactionType} = require("typedb-client");

async function runBasicQueries(database) {
    const client = TypeDB.coreClient("localhost:1729");
    const session = await client.session(database, SessionType.DATA);

    // Insert a person using a WRITE transaction
    const writeTransaction = await session.transaction(TransactionType.WRITE);
    const insertStream = await writeTransaction.query.insert('insert $x isa person, has email "x@email.com";');
    const conceptMaps = await insertStream.collect();
    console.log("Inserted a person with ID: " + conceptMaps[0].get("x").iid);
    // to persist changes, a write transaction must always be committed (closed)
    await writeTransaction.commit();

    // Retrieve persons using a READ only transaction
    const readTransaction = await session.transaction(TransactionType.READ);

    // We can either query and consume the iterator lazily
    let answerStream = await readTransaction.query.match("match $x isa person; get $x; limit 10;");
    for await (const aConceptMapAnswer of answerStream) {
        const person = aConceptMapAnswer.get("x");
        console.log("Retrieved person with id " + person.iid);
    }

    // Or query and consume the iterator immediately collecting all the results
    answerStream = await readTransaction.query.match("match $x isa person; get $x; limit 10;");
    const persons = await answerStream.collect();
    persons.forEach(conceptMap => {
        person = conceptMap.get("x");
        console.log("Retrieved person with id " + person.iid);
    });

    // a read transaction must always be closed
    await readTransaction.close();
    // a session must always be closed
    await session.close();
    // a client must always be closed
    client.close();
}

runBasicQueries("social_network");
```

<div class="note">
[Important]
Remember that transactions always need to be closed. Committing a write transaction closes it. A read transaction, however, must be explicitly closed by calling the `close()` method on it.
</div>

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts
retrieved as the answers to TypeQL queries.

To view examples of running various queries using the Node.js client, head over to their dedicated documentation pages
as listed below:

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Update](../11-query/05-update-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.typedb language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.options language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="javascript" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.query_future language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.stream language="javascript" %}

## Version Compatibility

| Client Node.js  |      TypeDB      |  TypeDB Cluster  |   Node    |
|:---------------:|:----------------:|:----------------:|:---------:|
|     2.17.0      |      2.17.0      |      2.17.0      | \>= 14.15 |
|     2.16.1      |      2.16.1      |      2.16.1      | \>= 14.15 |
|     2.14.2      | 2.12.0 to 2.15.0 | 2.13.0 to 2.15.0 | \>= 14.15 |
| 2.9.0 to 2.11.1 | 2.9.0 to 2.11.1  | 2.9.0 to 2.11.2  | \>= 14.15 |
|      2.8.0      |      2.8.0       |       N/A        | \>= 14.15 |
| 2.6.0 to 2.6.2  |  2.6.0 to 2.7.1  |       N/A        | \>= 14.15 |
| 2.4.0 to 2.5.0  |  2.1.2 to 2.5.0  |      2.5.0       | \>= 14.15 |
| 2.1.0 to 2.2.0  |  2.1.2 to 2.5.0  |  2.1.2 to 2.3.0  | \>= 14.15 |
|      2.0.1      |      2.0.2       |      2.0.2       | \>= 14.15 |
|      2.0.0      |   2.0.0, 2.0.1   |   2.0.0, 2.0.1   | \>= 14.15 |
|      1.8.0      |  1.8.0 to 1.8.4  |       N/A        |  \>= 6.5  |
