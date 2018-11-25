---
title: Client Python
keywords: grakn client, grakn driver, grakn python
tags: []
summary: ""
permalink: /docs/client-api/python
---

## Dependencies
Before installing the Python `grakn` package, make sure the following dependencies are installed.

- [Grakn >= 1.3.0](https://github.com/graknlabs/grakn/releases)
- [Python >= 2.7](https://www.python.org/downloads/)
- [PIP package manager](https://pip.pypa.io/en/stable/installing/)

## Installation
```
pip3 install grakn
```

## Quickstart
First make sure, the Grakn server is running. Learn more about [how to run the Grakn server]().

In the interpreter or in your source, import `grakn`.

```python
import grakn
```

Instantiate a client and open a session.

```python
client = grakn.Grakn(uri="localhost:48555")
with client.session(keyspace="mykeyspace") as session:
  ## session is open
```

As specified above, Grakn's default gRPC port is `48555`. The port `4567` (previously used as the default REST endpoint) is deprecated for clients.

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](), into the initial constructor as a dictionary.

```python
client = grakn.Grakn(uri="localhost:48555", credentials={"username": "<username>", "password": "<password>"})
```

Create transactions to use for reading and writing data.

```python
client = grakn.Grakn(uri="localhost:48555")

with client.session(keyspace="mykeyspace") as session:
  ## creating a write transaction
  with session.transaction(grakn.TxType.WRITE) as w_tx:
    ## write transaction is open
    ## write transaction must always be committed (closed)
    w_tx.commit()

  ## creating a read transaction
  with session.transaction(grakn.TxType.READ) as r_tx:
    ## read transaction is open
    ## if not using a `with` statement, then we must always close the read transaction like so
    # r_tx.close()
```

Running basic retrieval and insertion queries.

```python
client = grakn.Grakn(uri="localhost:48555")

with client.session(keyspace="mykeyspace") as session:
  ## creating a write transaction
  with session.transaction(grakn.TxType.WRITE) as w_tx:
    insert_iterator = w_tx.query("insert $x isa person has birth-date 2018-08-06;")
    concepts = insert_iterator.collect_concepts()
    print("Inserted a person with ID: {0}".format(concepts[0].id))
    ## write transaction must be committed (closed)
    tx.commit()

  ## creating a read transaction
  with session.transaction(grakn.TxType.READ) as r_tx:
    answer_iterator = tx.query("match $x isa person; limit 10; get;")

    ## retrieve the first answer
    done = object()
    a_concept_map_answer = next(answer_iterator, done)
    ## get the dictionary of variables : concepts, retrieve variable 'x'
    person = a_concept_map_answer.map()["x"]

    ## we can also iterate using a `for` loop
    some_people = []

    while (a_concept_map_answer is not done):
      ## get 'x' again, without going through .map()
      some_people.append(aConceptMapAnswer.map().get("x"))
      break ## skip the iteration, we are going to try something else
      a_concept_map_answer = next(answer_iterator, done)


    ## extract the rest of the people in one go
    remaining_people = answer_iterator.collect_concepts()

    ## if not using a `with` statement, then we must always close the read transaction
    # tx.close()
```

Check out the [Concept API]() to learn about the available read and write methods on an instance such as `person` in the example above.

To view examples of running various Graql queries using the Grakn Client Python, head over to their dedicated documentation pages as listed below:
- [Insert](/docs/query/insert-query)
- [Get](/docs/query/get-query)
- [Delete](/docs/query/delete-query)
- [Aggregate](/docs/query/aggregate-query)
- [Compute](/docs/query/compute-query)

## API Reference

### grakn.Grakn(URI) {#api-table-1}

| Method                                | Return type      | Description                                           |
| ------------------------------------- | ---------------- | ----------------------------------------------------- |
| `session(String keyspace)`            | `Session`        | Creates a new Session bound to the specified keyspace |
| `keyspaces().retrieve()`              | List of `String` | Retrieves all available keyspaces                     |
| `keyspaces().delete(String keyspace)` | `None`           | Deletes the specified keyspace                        |

### Session {#api-table-2}

| Method                      | Return type   | Description                                                      |
| --------------------------- | ------------- | ---------------------------------------------------------------- |
| `transaction(grakn.TxType)` | `Transaction` | Creates a new Transaction bound to the Session's keyspace        |
| `close()`                   | `None`        | Terminates the Session and closes the communication with server. |

### Transaction {#api-table-3}

| Method                                  | Return type        | Description                                                                                                                  |
| --------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `query(String graql_query, infer=True)` | Iterator of Answer | Executes a given Graql query on the Session's keyspace. `infer` indicates if inference is enabled (set to `True` by default) |
| `commit()`                              | None               | Commits and closes the Transaction, persisting changes in the keyspace                                                       |
| `close()`                               | None               | Closes the Transaction without committing                                                                                    |

### Iterator {#api-table-4}

| Method               | Return type     | Description                                                             |
| -------------------- | --------------- | ----------------------------------------------------------------------- |
| `collect_concepts()` | List of Concept | Consumes the entire iterator at once and returns a list of all Concepts |

_NOTE_: these iterators represent a lazy evaluation of a query or method on the Grakn server, and will be created very quickly. The actual work is performed when the iterator is consumed, creating an RPC to the server to obtain the next concrete `Answer` or `Concept`.

### Transaction continued {#api-table-5}

| Method                                             | Return type            | Description                                                                                 |
| -------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------- |
| `get_concept(String concept_id)`                   | Concept or None        | Retrieves a Concept by id                                                                   |
| `get_schema_concept(String label)`                 | SchemaConcept or None  | Retrieves a SchemaConcept by label                                                          |
| `get_attributes_by_value(value, grakn.DataType)`   | Iterator of Attribute  | Retrieves all Attributes holding the value provided, if any exists                          |
| `put_entity_type(String label)`                    | EntityType             | Creates a new EntityType, or retrieves an existing one with the given label                 |
| `put_relationship_type(String label)`              | RelationshipType       | Creates a new RelationshipType, or retrieves an existing one with the given label           |
| `put_attribute_type(String label, grakn.DataType)` | AttributeType          | Creates a new AttributeType, or retrieves an existing one with the given label and DataType |
| `put_role(String label)`                           | Role                   | Creates a Role, or retrieves an existing one with the given label                           |
| `put_rule(String label, String when, String then)` | Rule                   | Creates a Rule, or retrieves an existing one with the given label                           |

The methods above are called on a transaction to manipulate the schema. More on such methods in the [Concept API]().


### Answer {#api-table-6}
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

| Method          | Return type            | Description                                                                                          |
| --------------- | ---------------------- | ---------------------------------------------------------------------------------------------------- |
| `map()`         | Dict of str to Concept | Retrieves the result as a dictionary where a `key` isa the variable name and a value is the Concepts |
| `explanation()` | Explanation or null    | Retrieves an Explanation object if the Answer is inferred, null otherwise                            |

#### Value {#api-table-8}

| Method          | Return type          | Description                                                                |
| --------------- | -------------------- | -------------------------------------------------------------------------- |
| `number()`      | int or float         | Retrieves the numeric value of the Answer                                  |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise  |

#### ConceptList {#api-table-8}

| Method          | Return type          | Description                                                                |
| --------------- | -------------------- | -------------------------------------------------------------------------- |
| `list()`        | Array of String      | Retrieves the list of Concept IDs                                          |
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
| `answers()`     | List of Answer       | Retrives the list of Answers that belongs to this group                   |
| `explanation()` | Explanation or null  | Retrieves an Explanation object if the Answer is inferred, null otherwise |

### Explanation {#api-table-12}

| Method           | Return type     | Description                                                               |
| ---------------- | --------------- | ------------------------------------------------------------------------- |
| `query_pattern()`| String          | Retrieves a query pattern that describes how the inference was made       |
| `answers()`      | List of Answer  | Retrueves set of deducted/factual answers that led to the Answer          |