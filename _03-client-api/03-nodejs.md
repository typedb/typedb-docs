---
title: Client Node.js
keywords: grakn client, grakn driver, grakn nodejs
tags: []
summary: ""
permalink: /docs/client-api/nodejs
---

## Dependencies
Before installing the `grakn` node module, make sure the following dependencies are installed.

- [Grakn >= 1.3.0](https://github.com/graknlabs/grakn/releases)
- [Node >= 6.5.0](https://nodejs.org/en/download/)

## Installation
```
npm install grakn
```

## Quickstart
First make sure, the Grakn server is running. Learn more about [how to run the Grakn server]().

In your source, require `grakn`.

```javascript
const Grakn = require("grakn");
```

Instantiate a client and open a session.

```javascript
const client = new Grakn('localhost:48555');
const session = client.session('keyspace');
```

As specified above, Grakn's default gRPC port is `48555`. The port `4567` (previously used as the default REST endpoint) is deprecated for clients.

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](), into the initial constructor as a Javascript object.

```javascript
const client = grakn.Grakn("localhost:48555", { "username": "<username>", "password": "<password>" });
```

Create transactions to use for reading and writing data.

```javascript
const client = new Grakn('localhost:48555');
const session = client.session('keyspace');

// creating a write transaction
const wTx = await session.transaction(Grakn.txType.WRITE); // write transaction is open
// write transaction must always be committed (closed)
wTx.commit();

// creating a read transaction
const rTx = await session.transaction(Grakn.txType.READ); // read transaction is open
// read transaction must always be closed
rTx.close();
```

Running basic retrieval and insertion queries.

```javascript
const client = new Grakn('localhost:48555');
const session = client.session('keyspace');

async function runBasicQueries() {
  // creating a write transaction
  const wTx = await session.transaction(Grakn.txType.WRITE); // write transaction is open
  const insertIterator = await wTx.query("insert $x isa person has birth-date 2018-08-06");
  concepts = await insertIterator.collectConcepts()
  console.log("Inserted a person with ID: " + concepts[0].id);
  // write transaction must always be committed (closed)
  await wTx.commit();

  // creating a read transaction
  const rTx = await session.transaction(Grakn.txType.READ); // read transaction is open
  const answerIterator = await rTx.query("match $x isa person; limit 10; get;");
  // retrieve the first answer
  let aConceptMapAnswer = await answerIterator.next();
  // get the object of variables : concepts, retrieve variable 'x'
  person = aConceptMapAnswer.map()["x"];
  // we can also iterate using a `for` loop
  const somePeople = [];

  while ( aConceptMapAnswer != null) {
    // get the next `x`
    somePeople.push(aConceptMapAnswer.map().get("x"));
    break; // skip the iteration, we are going to try something else
    aConceptMapAnswer = await answerIterator.next();
  }
  const remainingPeople = answerIterator.collectConcepts()
  // read transaction must always be closed
  await rTx.close();
}
```

Check out the [Concept API]() to learn about the available read and write methods on an instance such as `person` in the example above.

To view examples of running various Graql queries using the Grakn Client Node.js, head over to their dedicated documentation pages as listed below:
- [Insert](/docs/query/insert-query)
- [Get](/docs/query/get-query)
- [Delete](/docs/query/delete-query)
- [Aggregate](/docs/query/aggregate-query)
- [Compute](/docs/query/compute-query)

{% include client_api_reference.html language = "javascript" %}
