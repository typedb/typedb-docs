---
pageTitle: ACID
keywords: typedb, ACID, guarantees, atomicity, consistency, isolation, durability
longTailKeywords: TypeDB ACID guarantees
summary: Description of TypeDB ACID guarantees.
toc: false
---

# ACID Guarantees

## Definition of ACID

ACID guarantees define the properties of a transactional database. The four parts are:

`A`: Atomicity. Either all operations in a transaction succeed, or none are applied.

`C`: Consistency. The database only moves from a correct state to a correct state when a transaction is committed.

`I`: Isolation. Concurrent transactions operate as if they were run sequentially.

`D`: Durability. Data is not lost or corrupted in the event of hardware or power failure.

For more detail please read [ACID](https://en.wikipedia.org/wiki/ACID).

## Overview

TypeDB delivers ACID guarantees up to a slightly relaxed form of isolation known as 
[Snapshot Isolation](https://en.wikipedia.org/wiki/Snapshot_isolation).

<div class="note">
[Note]
Consistency guarantees were implemented in TypeDB version 2.1.0.
</div>

### Atomicity

TypeDB transactions operate under a snapshot model. If an error occurs in the transaction, none of the operations will 
be applied to the persisted data. If a commit succeeds, all the changes are guaranteed to be immediately visible to 
following transactions.

### Consistency

The server will throw errors during commit if the transaction would violate consistency guarantees.
There are two primary types of data-level conflicts which could violate consistency:

1. `modify-delete`: a transaction extends or adds to a concept that a concurrent transaction deletes
2. `key`: a transaction adds a key-ownership (which must be unique) at the same time as another transaction.

In both cases, one transaction will be picked to successfully commit, and the other will be rejected. It is common
to build a re-try mechanism when loading data that relies on key conflicts to load data in parallel.

### Isolation

Like many established databases, we relax the "full" isolation guarantee (called `serialisability`) to 
`snapshot isolation`.

When a transaction is opened, the database is snapshotted and no further changes from other transactions will be visible
until a new transaction is opened.

After commit, all of the changes from the transaction are immediately visible to new transactions.

This mode of isolation guarantees that transactions that operate concurrently, on overlapping snapshots of the database, 
will conflict and fail at commit time if they were to lead to consistency violations.

### Durability

Durability is guaranteed with the use of a write-ahead-log (WAL) at the storage layer. This means under crashes or power 
failures, all data that finished committing will be available on reboot.

<div class="note">
[Note]
Unrecoverable failures of persistent storage like corrupt drives or physical damage are not considered as part of 
durability guarantees.
</div>
