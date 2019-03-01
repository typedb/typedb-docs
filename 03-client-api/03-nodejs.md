---
sidebarTitle: Node.js
pageTitle: Client Node.js
permalink: /docs/client-api/nodejs
---

## Dependencies

| Client Node.js | Grakn Core                  | Grakn KGMS   |  Node  |
| :------------: | :-------------------------: | :----------: | :----: |
| 1.5.0          | 1.5.0                       | N/A          | >= 6.5 |
| 1.3.1          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.3.0          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.9          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.8          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.7          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.6          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.5          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.4          | 1.3.0, 1.4.0, 1.4.2, 1.4.3  | 1.2.0        | >= 6.5 |
| 1.2.3          | 1.2.0                       | 1.2.0        | >= 6.5 |
| 1.2.2          | 1.2.0                       | 1.2.0        | >= 6.5 |
| 1.2.1          | 1.2.0                       | 1.2.0        | >= 6.5 |
| 1.2.0          | 1.2.0                       | 1.2.0        | >= 6.5 |

## Installation
```
npm install grakn
```

## Quickstart
First make sure, the [Grakn server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running..

In your source, require `grakn`.

<!-- test-standalone socialNetworkNodejsClientA.js -->
```javascript
const Grakn = require("grakn-client");
```

Instantiate a client and open a session.

<!-- test-standalone socialNetworkNodejsClientB.js -->
```javascript
const Grakn = require("grakn-client");

async function openSession (keyspace) {
	const client = new Grakn("localhost:48555");
	const session = await client.session(keyspace);
	// session is open
	await session.close();
	//session is closed
};

openSession("social_network");
```

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](/docs/management/users), into the initial constructor as a Javascript object.

<!-- test-ignore -->
```javascript
const client = new Grakn("localhost:48555", { "username": "<username>", "password": "<password>" });
```

Create transactions to use for reading and writing data.

<!-- test-standalone socialNetworkNodejsClientC.js -->
```javascript
const Grakn = require("grakn-client");

async function createTransactions (keyspace) {
	const client = new Grakn("localhost:48555");
	const session = await client.session(keyspace);

	// creating a write transaction
	const writeTransaction = await session.transaction(Grakn.txType.WRITE); // write transaction is open
	// to persist changes, write transaction must always be committed/closed
	await writeTransaction.commit();

	// creating a read transaction
	const readTransaction = await session.transaction(Grakn.txType.READ); // read transaction is open
	// read transaction must always be closed
	await readTransaction.close();
	// a session must always be closed
	await session.close();
}

createTransactions("social_network");
```

Running basic retrieval and insertion queries.

<!-- test-standalone socialNetworkNodejsClientD.js -->
```javascript
const Grakn = require("grakn-client");

async function runBasicQueries (keyspace) {
	const client = new Grakn("localhost:48555");
	const session = await client.session(keyspace);

	// Insert a person using a WRITE transaction
	const writeTransaction = await session.transaction(Grakn.txType.WRITE);
	const insertIterator = await writeTransaction.query('insert $x isa person, has email "x@email.com";');
	const concepts = await insertIterator.collectConcepts()
	console.log("Inserted a person with ID: " + concepts[0].id);
	// to persist changes, a write transaction must always be committed (closed)
	await writeTransaction.commit();

	// Retrieve persons using a READ only transaction
	const readTransaction = await session.transaction(Grakn.txType.READ);

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
}

runBasicQueries("social_network");
```

<div class="note">
[Important]
Remember that transactions always need to be closed. Committing a write transaction closes it. A read transaction, however, must be explicitly closed by calling the `close()` method on it.
</div>

Check out the [Concept API](/docs/concept-api/overview) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Node.js, head over to their dedicated documentation pages as listed below:
- [Insert](/docs/query/insert-query)
- [Get](/docs/query/get-query)
- [Delete](/docs/query/delete-query)
- [Aggregate](/docs/query/aggregate-query)
- [Compute](/docs/query/compute-query)

{% include client_api.html language = "javascript" %}
