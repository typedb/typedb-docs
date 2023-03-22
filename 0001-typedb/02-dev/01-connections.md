---
pageTitle: Connections
keywords: typedb, basics, connect, connection, session, database
longTailKeywords: basic concepts of typedb, typedb connection, typedb database, typedb session
summary: Brief description of connection to TypeDB.
toc: false
---

# Connections

## Clients

TypeDB server accepts remote connections from a number of [TypeDB clients](../../02-clients/00-clients.md) via 
[gRPC](https://en.wikipedia.org/wiki/GRPC) protocol.

Once connected, TypeDB clients can manage [databases](#databases) and [sessions](#sessions).

<div class="note">
[Note]
It’s recommended to instantiate a single client per application.
</div>

<div class="tabs dark">
[tab:TypeDB Console]

TypeDB Console

[tab:end]

[tab:Java]

Java

[tab:end]

[tab:Node.js]

Node.js

[tab:end]

[tab:Python]

```python
TypeDB.core_client(“0.0.0.0:1729”) as client:
```

[tab:end]
</div>


## Databases

TypeDB instances can contain multiple databases. A database consists of a [schema](../02-dev/02-schema.md) and 
[data](../02-dev/04-write.md) – and is both separate and independent of any other database. It is not possible to 
interact with one database from another. However, clients can connect to multiple databases simultaneously.

<div class="note">
[Note]
TypeDB is optimized for a small number of databases. It’s recommended to start with a single database, and add more as 
necessary (e.g., to support more applications). The **best practice** is to keep the number of databases **under 10**.
</div>

<div class="tabs dark">
[tab:TypeDB Console]

TypeDB Console

[tab:end]

[tab:Java]

Java

[tab:end]

[tab:Node.js]

Node.js

[tab:end]

[tab:Python]

```python
// create database
client.databases().create(‘test-db’)

// get database
client.databases().get(‘test-db’)

// get all databases
client.databases().all()

// check if database exists
client.databases().contains(‘test-db’)

// delete database
client.databases().get(‘test-db’).delete()
```

[tab:end]
</div>

## Sessions

There are two types of sessions: 

- SCHEMA sessions,
- DATA sessions. 

| Session type | Read data | Write data | Read schema  | Write schema |
|--------------|-----------|------------|--------------|--------------|
| DATA         | Yes       | Yes        | Yes          | Yes          |
| SCHEMA       |           | No         | Yes          | No           |

TypeDB clients should read and write data in DATA sessions.

TypeDB clients should read and write schema in SCHEMA sessions.

<div class="note">
[Note]
If a client needs to read both schema and data from a database, it can be done in any session type. But it is 
NOT possible to modify a schema and its data in the same session, regardless of the type. Write transactions are strict 
to the session types.
</div>

Once a session has been opened, clients can open and close transactions to read and write a database’s schema or data.

<div class="tabs dark">
[tab:TypeDB Console]

TypeDB Console

[tab:end]

[tab:Java]

Java

[tab:end]

[tab:Node.js]

Node.js

[tab:end]

[tab:Python]

```python
client.session(‘iam’, SessionType.SCHEMA) as session:
```

[tab:end]
</div>

<div class="note">
[Note]
It is recommended to avoid long-running sessions, because of possible network failures.
</div>

A good principle is that sessions group logically coherent transactions.

## Transactions

All queries to a TypeDB database are performed through transactions. TypeDB transactions provide full 
[ACID guarantees](#acid-guarantees) up to [snapshot isolation](#isolation).

There are two types of transactions: 

- READ transactions
- WRITE transactions

In addition, transactions must be explicit — clients must open and close transactions via an API.

<div class="tabs dark">
[tab:TypeDB Console]

TypeDB Console

[tab:end]

[tab:Java]

Java

[tab:end]

[tab:Node.js]

Node.js

[tab:end]

[tab:Python]

```python
// start transaction
with session.transaction(TransactionType.WRITE) as transaction:
    
    transaction.query().insert(typeql_insert_query_1)
    transaction.query().insert(typeql_insert_query_2)
    …
    transaction.query().insert(typeql_insert_query_N)

// commit transaction
    transaction.commit()
```
[tab:end]
</div>


<div class="note">
[Note]
TypeDB Studio lets developers commit/rollback transactions through its GUI.
</div>

TypeDB transactions use snapshot isolation and optimistic concurrency control to support concurrent, lock-free 
read/write transactions. 

### Configuration

TypeDB transactions will **time out** after a set period of time, **5 minutes by default**. However, the timeout can 
be changed via a client option. The timeout is intended to encourage short-lived transactions, prevent memory leaks 
caused by transactions which will not be completed and terminate unresponsive transactions.

### Best practices

- Avoid long-running transactions which can result in conflicts and resource contention.
- A good principle is that transactions group logically coherent queries.

## ACID guarantees

### Atomicity

TypeDB transactions are all or nothing. If a commit succeeds, all of its changes are persisted. If it fails, all of its 
changes will be rolled back.

### Consistency

TypeDB validates all changes to data and schemas. If changes to a database violate schema or data constraints, the 
transaction will fail and be rolled back.

### Isolation

TypeDB transactions use snapshot isolation and optimistic concurrency control to support simultaneous, lock-free 
read/write transactions. Thus, a transaction operates on its own snapshot of the data, independent of any other. All 
of its changes are hidden from other transactions. However, they will become visible immediately after a successful 
commit. 

If two transactions attempt to modify the same data, one will succeed on commit while the other will fail. However, 
one transaction can read data while another is writing it.

### Durability

TypeDB writes transactions to a write-ahead-log upon commit, ensuring they can be recovered if an unexpected failure 
(e.g., power outage) occurs before the data is modified.

<div class="note">
[Note]
TypeDB durability guarantees do not apply when storage devices become corrupt or damaged.
</div>

Successful write transactions are written to the write-ahead-log before returning a response to the client. If a 
transaction is not successful, all changes are rolled back.

For cluster installations of TypeDB Cloud transaction acknowledgement is sent to the client after majority of replicas 
replicated the transaction results. See [Replication](../03-admin/04-ha.md) for details.
