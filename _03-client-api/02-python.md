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

```cpython
import grakn
```

Instantiate a client and open a session.

```cpython
client = grakn.Grakn(uri="localhost:48555")
with client.session(keyspace="mykeyspace") as session:
  ## session is open
```

As specified above, Grakn's default gRPC port is `48555`. The port `4567` (previously used as the default REST endpoint) is deprecated for clients.

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](), into the initial constructor as a dictionary.

```cpython
client = grakn.Grakn(uri="localhost:48555", credentials={"username": "<username>", "password": "<password>"})
```

Create transactions to use for reading and writing data.

```cpython
client = grakn.Grakn(uri="localhost:48555")

with client.session(keyspace="mykeyspace") as session:
  ## creating a write transaction
  with session.transaction(grakn.TxType.WRITE) as write_transaction:
    ## write transaction is open
    ## write transaction must always be committed (closed)
    write_transaction.commit()

  ## creating a read transaction
  with session.transaction(grakn.TxType.READ) as read_transaction:
    ## read transaction is open
    ## if not using a `with` statement, we must always close the read transaction like so
    # read_transaction.close()
```

Running basic retrieval and insertion queries.

```cpython
client = grakn.Grakn(uri="localhost:48555")

with client.session(keyspace="mykeyspace") as session:
  ## creating a write transaction
  with session.transaction(grakn.TxType.WRITE) as write_transaction:
    insert_iterator = write_transaction.query("insert $x isa person has birth-date 2018-08-06;")
    concepts = insert_iterator.collect_concepts()
    print("Inserted a person with ID: {0}".format(concepts[0].id))
    ## write transaction must be committed (closed)
    write_transaction.commit()

  ## creating a read transaction
  with session.transaction(grakn.TxType.READ) as read_transaction:
    answer_iterator = read_transaction.query("match $x isa person; limit 10; get;")

    ## retrieve the first answer
    a_concept_map_answer = next(answer_iterator)
    ## get the dictionary of variables : concepts, retrieve variable 'x'
    person = a_concept_map_answer.map()["x"]

    ## we can also iterate using a `for` loop
    some_people = []

    for answer in answer_iterator:
      some_people.append(answer.map().get("x"))
      break ## skip the iteration, we are going to try something else

    ## extract the rest of the people in one go
    remaining_people = answer_iterator.collect_concepts()

    ## if not using a `with` statement, then we must always close the read transaction
    # read_transaction.close()
```

Check out the [Concept API]() to learn about the available read and write methods on an instance such as `person` in the example above.

To view examples of running various Graql queries using the Grakn Client Python, head over to their dedicated documentation pages as listed below. Note that these examples, assume a transaction object has been instantiated and will be committed/closed after the operation is complete:
- [Insert](/docs/query/insert-query)
- [Get](/docs/query/get-query)
- [Delete](/docs/query/delete-query)
- [Aggregate](/docs/query/aggregate-query)
- [Compute](/docs/query/compute-query)

{% include client_api/main.html language = "cpython" %}