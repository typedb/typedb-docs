---
pageTitle: ACID
keywords: grakn, acid, transactionality, atomicity, consistency, isolation, durability 
longTailKeywords: transactional guarantees
Summary: Grakn's transactional guarantees (ACIDity)
toc: false
---

## What is ACID?

ACID defines the properties of a transactional database under error or failure states. The four parts are:

`A`: Atomicity. Either all operations in a transaction succeed, or none are applied.
`C`: Consistency. The database only moves from a correct state to a correct state when a transaction is committed.
`I`: Isolation. Concurrent transactions operate as if they were run sequentially.
`D`: Durability. Data is not lost or corrupted in the event of hardware or power failure.

For more detail please read [ACID](https://en.wikipedia.org/wiki/ACID).

This page addresses Grakn's transactionality.

## Overview

Grakn 2.0 aims to deliver ACID guarantees up to a slightly relaxed form of isolation known as [Snapshot Isolation](https://en.wikipedia.org/wiki/Snapshot_isolation).

At the current time, Atomicity, Snapshot Isolation, and Durability are already guaranteed. However, under specific race conditions, Consistency 
guarantees may be violated. We are actively working towards fixing this.

### Atomicity

Grakn 2.0 transactions operate under a snapshot model. If an error occurs in the transaction, none of the operations will be applied
to the persisted data. If a commit succeeds, all the changes are guaranteed to be immediately visible to following transactions.

### Consistency

As noted, there are two specific conditions which can lead to known consistency violations.

1. Concurrently inserting attribute ownership as keys. The expected behaviour is: two concurrent transactions
inserting an instance of type `T` with the same key, only one transaction should succeed. This preserves the guarantee that only
1 instance of `T` with the given key exists. Under specific conditions, it is currently possible to end up with two concepts with the key.
2. Concurrent insert and delete. When adding or extending a relation, or inserting an attribute ownership, connected to an existing concept
while in a concurrent transaction deleting the concept, it is possible commit both. This results in relations or attribute ownerships
containing or pointing at concepts which longer exist. 

Both of these cases are being addressed in the short term.

### Isolation

Like many established databases, we relax the "full" isolation guarantee (called `serialisability`) to `snapshot isolation`.

When a transaction is opened, the database is snapshotted and no further changes from other transactions will be visible 
until a new transaction is opened.

After commit, all of the changes from the transaction are immediately visible to new transactions.

This mode of isolation guarantees that transactions that operate concurrently, on overlapping snapshots of the database, will
conflict and fail at commit time if they were to lead to consistency violations.

### Durability

Durability is guaranteed with the use of a write-head-log at the storage layer. This means under crashes or power failures,
all data that finished committing will be available on reboot.

Note that un-recoverable failures like corrupt drives or physical damage are not considered as part of durability guarantees.