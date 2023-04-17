---
pageTitle: Client Python
keywords: typedb, client, python
longTailKeywords: typedb python client, typedb client python, client python, python client
Summary: API Reference of TypeDB Client Python.
---
## Installation

#### To use this client, you need a compatible TypeDB Server running. Visit our [Compatibility Table](#version-compatibility)


```
pip install typedb-client
```
If multiple Python versions are available, you may wish to use
```
pip3 install typedb-client
```

### Resources

- [Client Python on GitHub](https://github.com/vaticle/typedb-client-python)
- [Releases](https://github.com/vaticle/typedb-client-python/releases)
- [Examples](https://github.com/vaticle/typedb-examples)

## Quickstart
First make sure, the [TypeDB server](/docs/typedb/install-and-run#start-the-typedb-server) is running and that you have **created the social network database** as detailed in the [quickstart](00-general/04-quickstart.md#download-and-load-the-complete-schema) example before running the following.

In the interpreter or in your source, import everything from `typedb.client`.

<!-- test-example social_network_python_client_a.py -->
```python
from typedb.client import *
```

Instantiate a client and open a session.

<!-- test-example social_network_python_client_b.py -->
```python
from typedb.client import *

with TypeDB.core_client("localhost:1729") as client:
    with client.session("social_network", SessionType.DATA) as session:
        ## session is open
        pass
    ## session is closed
## client is closed
```

Create transactions to use for reading and writing data.

<!-- test-example social_network_python_client_c.py -->
```python
from typedb.client import *

with TypeDB.core_client("localhost:1729") as client:
    with client.session("social_network", SessionType.DATA) as session:
        ## creating a write transaction
        with session.transaction(TransactionType.WRITE) as write_transaction:
            ## write transaction is open
            ## write transaction must always be committed (closed)
            write_transaction.commit()

        ## creating a read transaction
        with session.transaction(TransactionType.READ) as read_transaction:
            ## read transaction is open
            ## if not using a `with` statement, we must always close the read transaction like so
            # read_transaction.close()
            pass
```

Running basic retrieval and insertion queries.

<!-- test-example social_network_python_client_d.py -->
```python
from typedb.client import *

with TypeDB.core_client("localhost:1729") as client:
    with client.session("social_network", SessionType.DATA) as session:
        ## Insert a Person using a WRITE transaction
        with session.transaction(TransactionType.WRITE) as write_transaction:
            insert_iterator = write_transaction.query().insert('insert $x isa person, has email "x@email.com";')
            concepts = [ans.get("x") for ans in insert_iterator]
            print("Inserted a person with ID: {0}".format(concepts[0].get_iid()))
            ## to persist changes, write transaction must always be committed (closed)
            write_transaction.commit()

        ## Read the person using a READ only transaction
        with session.transaction(TransactionType.READ) as read_transaction:
            answer_iterator = read_transaction.query().match("match $x isa person; get $x; limit 10;")

            for answer in answer_iterator:
                person = answer.get("x")
                print("Retrieved person with id " + person.get_iid())

        ## Or query and consume the iterator immediately collecting all the results
        with session.transaction(TransactionType.READ) as read_transaction:
            answer_iterator = read_transaction.query().match("match $x isa person; get $x; limit 10;")
            persons = [ans.get("x") for ans in answer_iterator]
            for person in persons:
                print("Retrieved person with id " + person.get_iid())

        ## if not using a `with` statement, then we must always close the session and the read transaction
        # read_transaction.close()
        # session.close()
        # client.close()
```
<div class="note">
[Important]
Remember that transactions always need to be closed. The safest way is to use the `with ...` syntax which auto-closes at the end of the `with` block. Otherwise, remember to call `transaction.close()` explicitly.
</div>

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to TypeQL queries.

To view examples of running various queries using the Python client, head over to their dedicated documentation pages as listed below.

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Update](../11-query/05-update-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)

<hr style="margin-top: 40px;" />

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.typedb language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.options language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="python" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="python" %}

{% include api/generic.html data=site.data.03_client_api.references.query_future language="python" %}


## Version Compatibility

|  Client Python  |      TypeDB      |  TypeDB Cluster  |     Python     |
|:---------------:|:----------------:|:----------------:|:--------------:|
|     2.12.0      | 2.12.0 to 2.14.3 | 2.13.0 to 2.14.1 |    \>= 3.6     |
| 2.9.0 to 2.11.1 | 2.9.0 to 2.11.1  | 2.9.0 to 2.11.2  |    \>= 3.6     |
|      2.8.0      |      2.8.0       |       N/A        |    \>= 3.6     |
| 2.6.0 to 2.6.3  |  2.6.0 to 2.7.1  |       N/A        |    \>= 3.6     |
| 2.4.0 to 2.5.0  |  2.1.2 to 2.5.0  |      2.5.0       |    \>= 3.6     |
|      2.2.0      |  2.1.2 to 2.5.0  |  2.1.2 to 2.3.0  |    \>= 3.6     |
|      2.1.1      |      2.1.2       |      2.1.2       |    \>= 3.6     |
|      2.1.0      |      2.1.0       |      2.1.0       |    \>= 3.6     |
|      2.0.1      |      2.0.2       |      2.0.2       |    \>= 3.6     |
|      2.0.0      |  2.0.0 to 2.0.1  |  2.0.0 to 2.0.1  |    \>= 3.6     |
|      1.8.0      |  1.8.0 to 1.8.4  |       N/A        | \>= 3.5, < 3.8 |
