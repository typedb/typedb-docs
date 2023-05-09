---
pageTitle: Java Driver tutorial
keywords: typedb, client, java
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: Tutorial for TypeDB Node.js Driver.
---

# Node.js Driver tutorial

## Prerequisites

Make sure to install the Java Driver as per [Installation](02-node-js-install.md) page. The TypeDB server is also 
needs to be installed and running.

## Importing

Use the `require` keyword with the `typedb-client`.

<!-- test-example socialNetworkNodejsClientA.js -->
```javascript
const { TypeDB } = require("typedb-client");
```

## Connecting

Instantiate a TypeDB Core client and open a [session](../../0001-typedb/02-dev/01-connect.md#sessions) to a 
[database](../../0001-typedb/02-dev/01-connect.md#databases). 

<div class="note">
[Note]
If you don't have a database, you can find how to create one on the 
[Quickstart](../0001-typedb/01-start/03-quickstart.md#create-a-database) page.

The name for the database should be `social_network`.
</div>

Instantiate a client and open a session.

<!-- test-example socialNetworkNodejsClientB.js -->
```javascript
const { TypeDB, SessionType } = require("typedb-client");

async function openSession (database) {
	const client = TypeDB.coreClient("localhost:1729");
	const session = await client.session(database, SessionType.DATA);
	// session is open
	await session.close();
	//session is closed
	client.close();
};

openSession("social_network");
```

## Creating transactions

Create transactions to use for reading and writing data.

<!-- test-example socialNetworkNodejsClientC.js -->
```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");

async function createTransactions (database) {
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

## Querying

Running basic retrieval and insertion queries.

<!-- test-example socialNetworkNodejsClientD.js -->
```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");

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
	persons.forEach( conceptMap => {
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

Check out the [Concept API](../../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to TypeQL queries.

To view examples of running various queries using the Node.js client, head over to their dedicated documentation pages as listed below:
- [Insert](../../11-query/03-insert-query.md)
- [Get](../../11-query/02-get-query.md)
- [Delete](../../11-query/04-delete-query.md)
- [Update](../../11-query/05-update-query.md)
- [Aggregate](../../11-query/06-aggregate-query.md)

## Where to go next

Check out the [Response](04-node-js-api-ref.md#response-section) section of API reference page to learn about the available 
methods on the concepts retrieved as the answers to queries.

To view examples of various TypeQL queries, head over to 
[Writing data](../../0001-typedb/02-dev/04-write.md) and
[Reading data](../../0001-typedb/02-dev/05-read.md) pages.

For some more Python Driver examples — see the 
[Python implementation](../../0001-typedb/01-start/05-sample-app.md#nodejs-implementation) on the Sample application 
page.
