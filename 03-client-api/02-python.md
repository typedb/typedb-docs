---
sidebarTitle: Python
pageTitle: Client Python
permalink: /docs/client-api/python
---

## Dependencies
Before installing the Python `grakn` package, make sure the following dependencies are installed.

- [Grakn >= 1.3.0](https://github.com/graknlabs/grakn/releases)
- [Python >= 2.7](https://www.python.org/downloads/)
- [PIP package manager](https://pip.pypa.io/en/stable/installing/)

## Installation
```
pip install grakn
```
If multiple Python versions are available, you may wish to use
```
pip3 install grakn
```

## Quickstart
First make sure, the [Grakn server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

In the interpreter or in your source, import `grakn`.

```lang-python
import grakn
```

Instantiate a client and open a session.

```lang-python
client = grakn.Grakn(uri="localhost:48555")
with client.session(keyspace="mykeyspace") as session:
  ## session is open
  pass
## session is closed
```

As specified above, Grakn's default gRPC port is `48555`. The port `4567` (previously used as the default REST endpoint) is deprecated for clients.

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](/docs/management/users), into the client constructor as a dictionary.

```lang-python
client = grakn.Grakn(uri="localhost:48555", credentials={"username": "<username>", "password": "<password>"})
```

Create transactions to use for reading and writing data.

```lang-python
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

```lang-python
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
<div class="note">
[Important]
Remember that transactions always need to be closed. The safest way is to use the `with ...` syntax which auto-closes at the end of the `with` block. Otherwise, remember to call `transaction.close()` explicitly.
</div>

Check out the [Concept API](/docs/concept-api/overview) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Python, head over to their dedicated documentation pages as listed below.

- [Insert](/docs/query/insert-query)
- [Get](/docs/query/get-query)
- [Delete](/docs/query/delete-query)
- [Aggregate](/docs/query/aggregate-query)
- [Compute](/docs/query/compute-query)

{% include client_api.html language = "python" %}
