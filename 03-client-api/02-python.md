---
pageTitle: Client Python
keywords: grakn, client, python
longTailKeywords: grakn python client, grakn client python, client python, python client
Summary: API Reference of Grakn Client Python.
---

## Dependencies

| Client Python  | Grakn Core                  | Grakn KGMS     | Python |
| :------------: | :-------------------------: | :----------:   | :----: |
| 1.6.0          | 1.6.0 to 1.6.2              | N/A            | >= 2.7 |
| 1.5.4          | 1.5.8, 1.5.9                | 1.5.8          | >= 2.7 |
| 1.5.3          | 1.5.2 to 1.5.7              | 1.5.2 to 1.5.7 | >= 2.7 |
| 1.5.2          | 1.5.2, 1.5.3                | 1.5.2          | >= 2.7 |
| 1.5.1          | 1.5.0                       | N/A            | >= 2.7 |
| 1.4.2          | 1.3.0 to 1.4.3              | 1.2.0, 1.4.3   | >= 3.6 |
| 1.3.0 to 1.3.2 | 1.3.0                       | 1.4.3          | >= 3.6 |

## Installation
```
pip install grakn-client
```
If multiple Python versions are available, you may wish to use
```
pip3 install grakn-client
```

## Quickstart
First make sure, the [Grakn server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

In the interpreter or in your source, import `GraknClient` from `grakn.client`.

<!-- test-example social_network_python_client_a.py -->
```python
from grakn.client import GraknClient
```

Instantiate a client and open a session.

<!-- test-example social_network_python_client_b.py -->
```python
from grakn.client import GraknClient

with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace="social_network") as session:
        ## session is open
        pass
    ## session is closed
## client is closed
```

We can also pass the credentials, as specified when [configuring authentication via Grakn Console](../06-management/02-users.md), into the client constructor as a dictionary.

<!-- test-ignore -->
```python
client = GraknClient(uri="localhost:48555", credentials={"username": "<username>", "password": "<password>"})
```

Create transactions to use for reading and writing data.

<!-- test-example social_network_python_client_c.py -->
```python
from grakn.client import GraknClient

with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace="social_network") as session:
        ## creating a write transaction
        with session.transaction().write() as write_transaction:
            ## write transaction is open
            ## write transaction must always be committed (closed)
            write_transaction.commit()

        ## creating a read transaction
        with session.transaction().read() as read_transaction:
            ## read transaction is open
            ## if not using a `with` statement, we must always close the read transaction like so
            # read_transaction.close()
            pass
```

Running basic retrieval and insertion queries.

<!-- test-example social_network_python_client_d.py -->
```python
from grakn.client import GraknClient

with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace="social_network") as session:
        ## Insert a Person using a WRITE transaction
        with session.transaction().write() as write_transaction:
            insert_iterator = write_transaction.query('insert $x isa person, has email "x@email.com";')
            concepts = insert_iterator.collect_concepts()
            print("Inserted a person with ID: {0}".format(concepts[0].id))
            ## to persist changes, write transaction must always be committed (closed)
            write_transaction.commit()

        ## Read the person using a READ only transaction
        with session.transaction().read() as read_transaction:
            answer_iterator = read_transaction.query("match $x isa person; get; limit 10;")

            for answer in answer_iterator:
                person = answer.map().get("x")
                print("Retrieved person with id " + person.id)

        ## Or query and consume the iterator immediately collecting all the results
        with session.transaction().read() as read_transaction:
            answer_iterator = read_transaction.query("match $x isa person; get; limit 10;")
            persons = answer_iterator.collect_concepts()
            for person in persons:
                print("Retrieved person with id "+ person.id)

        ## if not using a `with` statement, then we must always close the session and the read transaction
        # read_transaction.close()
        # session.close()
        # client.close()
```
<div class="note">
[Important]
Remember that transactions always need to be closed. The safest way is to use the `with ...` syntax which auto-closes at the end of the `with` block. Otherwise, remember to call `transaction.close()` explicitly.
</div>

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Python, head over to their dedicated documentation pages as listed below.

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)
- [Compute](../11-query/07-compute-query.md)

<hr style="margin-top: 40px;" />

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.grakn language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.iterator language="python" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="python" %}

