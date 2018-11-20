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
In your source, require `grakn`.

```javascript
const Grakn = reqruire("grakn");
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
  const aConceptMapAnswer = await answerIterator.next();
  // get the object of variables : concepts, retrieve variable 'x'
  person = aConceptMapAnswer.map()["x"];
  // we can also iterate using a `for` loop
  const somePeople = [];
  for (conceptMap in answerIterator) {
    // get 'x' again, without going through .map()
    somePeople.push(conceptMap["x"]);
    // skip the iteration, we are going to try something else
    break;
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

## API Reference

### grakn.Grakn(URI) {#api-table-13}

| Method                                      | Return type      | Description                                           |
| ------------------------------------------- | ---------------- | ----------------------------------------------------- |
| `session(String keyspace)`                  | Session          | Creates a new Session bound to the specified keyspace |
| `async keyspaces().retrieve()`              | Array of String  | Retrieves all available keyspaces                     |
| `async keyspaces().delete(String keyspace)` | void             | Deletes the given keyspace                            |

### Session {#api-table-14}

| Method                            | Return type | Description                                                      |
| --------------------------------- | ----------- | ---------------------------------------------------------------- |
| `async transaction(Grakn.TxType)` | Transactio  | Creates a new Transaction bound to the Session's keyspace        |
| `close()`                         | void        | Terminates the Session and closes the communication with server. |

### Transaction {#api-table-15}

| Method                                             | Return type         | Description                                                                                                                  |
| -------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `async query(String graql_query, { infer: true })` | Iterator of Answer  | Executes a given Graql query on the Session's keyspace. `infer` indicates if inference is enabled (set to `True` by default) |
| `async commit()`                                   | void                | Commits and closes the Transaction, persisting changes in the keyspace                                                       |
| `async close()`                                    | void                | Closes the Transaction without committing                                                                                    |

### Iterator {#api-table-16}

| Method                    | Return type               | Description                                                              |
| ------------------------- | ------------------------- | ------------------------------------------------------------------------ |
| `async next()`            | IteratorElement or null   | Retrieves the next element or returns null if no more available          |
| `async collect()`         | Array of IteratorElement  | Consumes the the iterator and collects all the elements as an arrat      |
| `async collectConcepts()` | Array of Concept          | Consumes the entire iterator at once and returns a array of all Concepts |

_NOTE_: these iterators represent a lazy evaluation of a query or method on the Grakn server, and will be created very quickly. The actual work is performed when the iterator is consumed, creating an RPC to the server to obtain the next concrete `Answer` or `Concept`.

### Transaction continued {#api-table-17}

| Method                                                  | Return type            | Description                                                                                 |
| ------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------- |
| `async getConcept(String conceptId)`                    | Concept or null        | Retrieves a Concept by id                                                                   |
| `async getSchemaConcept(String label)`                  | SchemaConcept or null  | Retrieves a SchemaConcept by label                                                          |
| `async getAttributesByValue(value, grakn.DataType)`     | Iterator of Attribute  | Retrieves all Attributes holding the value provided, if any exists                          |
| `async putEntityType(String label)`                     | EntityType             | Creates a new EntityType, or retrieves an existing one with the given label                 |
| `async putRelationshipType(String label)`               | RelationshipType       | Creates a new RelationshipType, or retrieves an existing one with the given label           |
| `async putAttributeType(String label, grakn.DataType)`  | AttributeType          | Creates a new AttributeType, or retrieves an existing one with the given label and DataType |
| `async putRole(String label)`                           | Role                   | Creates a Role, or retrieves an existing one with the given label                           |
| `async putRule(String label, String when, String then)` | Rule                   | Creates a Rule, or retrieves an existing one with the given label                           |

The methods above are called on a transaction to manipulate the schema. More on such methods in the [Concept API]().

### Answer {#api-table-18}
This object represents a query answer and it is contained in the Iterator returned by `transaction.query()` method.
Based on the type of query exectued, an Answer may have one of the following types.

| Query Type                             | Answer Type       |
|--------------------------------------- |-----------------: |
| `define`                               | ConceptMap        |
| `undefine`                             | ConceptMap        |
| `get`                                  | ConceptMap        |
| `insert`                               | ConceptMap        |
| `delete`                               | ConceptMap        |
| `aggregate count/min/max/sum/mean/std` | Value             |
| `aggregate group`                      | AnswerGroup       |
| `compute count/min/max/sum/mean/std`   | Value             |
| `compute path`                         | ConceptList       |
| `compute cluster`                      | ConceptSet        |
| `compute centrality`                   | ConceptSetMeasure |

#### ConceptMap {#api-table-7}

| Method          | Return type              | Description                                                                                       |
| --------------- | ------------------------ | ------------------------------------------------------------------------------------------------- |
| `map()`         | Object of str to Concept | Retrieves the result as an object where a `key` isa the variable name and a value is the Concepts |
| `explanation()` | Explanation or null      | Retrieves an Explanation object if the Answer is inferred, null otherwise                         |

#### Value {#api-table-8}

| Method          | Return type          | Description                                                                |
| --------------- | -------------------- | -------------------------------------------------------------------------- |
| `number()`      | int or float         | Retrieves the numeric value of the Answer                                  |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise  |

#### ConceptList {#api-table-8}

| Method          | Return type          | Description                                                                |
| --------------- | -------------------- | -------------------------------------------------------------------------- |
| `list()`        | Array of String      | Retrieves the array of Concept IDs                                         |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise  |

#### ConceptSet {#api-table-9}

| Method          | Return type          | Description                                                                |
| --------------- | -------------------- | -------------------------------------------------------------------------- |
| `set()`         | Set of String        | Retrieves the set containing Concept IDs                                   |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise  |

#### ConceptSetMeasure {#api-table-10}

| Method          | Return type          | Description                                                                            |
| --------------- | -------------------- | -------------------------------------------------------------------------------------- |
| `measurement()` | int or float         | Retrieves the numeric value associated to the set of Concepts contained in the Answer  |
| `set()`         | Set of String        | Retrieves the set containing Concept IDs                                               |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise              |

#### AnswerGroup {#api-table-11}

| Method          | Return type          | Description                                                               |
| --------------- | -------------------- | ------------------------------------------------------------------------- |
| `owner()`       | Concept              | Retrieves the Concept that is the group owner                             |
| `answers()`     | Array of Answer      | Retrives the array of Answers that belongs to this group                   |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise |

### Explanation {#api-table-12}

| Method           | Return type     | Description                                                               |
| ---------------- | --------------- | ------------------------------------------------------------------------- |
| `query_pattern()`| String          | Retrieves a query pattern that describes how the inference was made       |
| `answers()`      | Array of Answer | Retrueves set of deducted/factual answers that led to the Answer          |