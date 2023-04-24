---
pageTitle: Python Driver tutorial
keywords: typedb, client, python
longTailKeywords: typedb python client, typedb client python, client python, python client
Summary: Tutorial for TypeDB Python Driver.
---

# Python Driver tutorial

## Prerequisites

Make sure to install the Python Driver as per [Installation](02-python-install.md) page. The TypeDB server is also 
needs to be installed and running.

## Importing

In the interpreter or in your source code, import everything from `typedb.client`.

<!-- test-example social_network_python_client_a.py -->
```python
from typedb.client import *
```

## Connecting

Instantiate a TypeDB Core client and open a [session](../../0001-typedb/02-dev/01-connect.md#sessions) to a 
[database](../../0001-typedb/02-dev/01-connect.md#databases). 

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

## Creating transactions

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

## Querying

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
Remember that transactions always need to be closed. The safest way is to use the `with ...` syntax which auto-closes 
at the end of the `with` block. Otherwise, remember to call `transaction.close()` explicitly.
</div>

## Where to go next

Check out the [Response](04-python-api-ref.md#response) section of API reference page to learn about the available 
methods on the concepts retrieved as the answers to queries.

To view examples of various TypeQL queries, head over to 
[Writing data](../../0001-typedb/02-dev/04-write.md) and
[Reading data](../../0001-typedb/02-dev/05-read.md) pages.

For some more Python Driver examples — see the 
[Python implementation](../../0001-typedb/01-start/05-sample-app.md#python-implementation) on the Sample application 
page.
