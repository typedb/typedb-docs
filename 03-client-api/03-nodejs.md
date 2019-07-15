---
pageTitle: Client Node.js
keywords: grakn, client, node.js
longTailKeywords: grakn node.js client, grakn client node.js, client node.js, python node.js
Summary: API Reference of Grakn Client Node.js.
---

## Dependencies

| Client Node.js | Grakn Core                  | Grakn KGMS   |  Node  |
| :------------: | :-------------------------: | :----------: | :----: |
| 1.5.3          | 1.5.2 to 1.5.7              | 1.5.2        | >= 6.5 |
| 1.5.1          | 1.5.0                       | N/A          | >= 6.5 |
| 1.2.4 to 1.3.1 | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.0 to 1.2.2 | 1.2.0                       | 1.2.0        | >= 6.5 |

## Installation
```
npm install grakn-client
```

## Quickstart
First make sure, the [Grakn server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running..

In your source, require `grakn-client`.

<!-- test-example socialNetworkNodejsClientA.js -->
```javascript
const GraknClient = require("grakn-client");
```

Instantiate a client and open a session.

<!-- test-example socialNetworkNodejsClientB.js -->
```javascript
const GraknClient = require("grakn-client");

async function openSession (keyspace) {
	const client = new GraknClient("localhost:48555");
	const session = await client.session(keyspace);
	// session is open
	await session.close();
	//session is closed
	client.close();
};

openSession("social_network");
```

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](../06-management/02-users.md), into the initial constructor as a Javascript object.

<!-- test-ignore -->
```javascript
const client = new GraknClient("localhost:48555", { "username": "<username>", "password": "<password>" });
```

Create transactions to use for reading and writing data.

<!-- test-example socialNetworkNodejsClientC.js -->
```javascript
const GraknClient = require("grakn-client");

async function createTransactions (keyspace) {
	const client = new GraknClient("localhost:48555");
	const session = await client.session(keyspace);

	// creating a write transaction
	const writeTransaction = await session.transaction().write(); // write transaction is open
	// to persist changes, write transaction must always be committed/closed
	await writeTransaction.commit();

	// creating a read transaction
	const readTransaction = await session.transaction().read(); // read transaction is open
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
const GraknClient = require("grakn-client");

async function runBasicQueries (keyspace) {
	const client = new GraknClient("localhost:48555");
	const session = await client.session(keyspace);

	// Insert a person using a WRITE transaction
	const writeTransaction = await session.transaction().write();
	const insertIterator = await writeTransaction.query('insert $x isa person, has email "x@email.com";');
	const concepts = await insertIterator.collectConcepts()
	console.log("Inserted a person with ID: " + concepts[0].id);
	// to persist changes, a write transaction must always be committed (closed)
	await writeTransaction.commit();

	// Retrieve persons using a READ only transaction
	const readTransaction = await session.transaction().read();

	// We can either query and consume the iterator lazily
	let answerIterator = await readTransaction.query("match $x isa person; get; limit 10;");
	let aConceptMapAnswer = await answerIterator.next();
	while (aConceptMapAnswer != null) {
		// get the next `x`
		const person = aConceptMapAnswer.map().get("x");
		console.log("Retrieved person with id "+ person.id);
		aConceptMapAnswer = await answerIterator.next();
	}

	// Or query and consume the iterator immediately collecting all the results
	answerIterator = await readTransaction.query("match $x isa person; get; limit 10;");
	const persons = await answerIterator.collectConcepts();
	persons.forEach( person => { console.log("Retrieved person with id "+ person.id) });

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

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Node.js, head over to their dedicated documentation pages as listed below:
- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)
- [Compute](../11-query/07-compute-query.md)

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.grakn language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="javascript" %}

{% include api/generic.html data=site.data.03_client_api.references.iterator language="javascript" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="javascript" %}

