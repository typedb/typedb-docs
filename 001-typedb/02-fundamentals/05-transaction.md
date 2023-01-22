---
pageTitle: Transaction
keywords: typedb, transaction
longTailKeywords: typedb transaction
summary: TypeDB transaction concept.
toc: false
---

<!--- 
Define ACID and describe each section (can be obtained from previous docs). Write transactions can fail their commit with isolation violation errors that means users should re-try. Can be opened with transaction-wide options (also inherits session options).
-->

# Transaction (ACID Guarantees)

A transaction performs queries or Concept API calls on the database. TypeDB transactions comply with 
[ACID](../../06-management/02-acid.md) properties, up to snapshot isolation.

Transactions automatically close after a configured timeout (default 5 minutes). This is to encourage shorter-lived transactions,
prevent memory leaks caused by forgotten unclosed client-side transactions, and kill potentially unresponsive transactions.

**Best Practices**

Keep transactions generally short-lived. Long-lived transactions are more likely to clash with others when committing, and pin resources in the server.

A good principle is that transactions group logically coherent queries. For example, when building an e-commerce platform, loading a user's purchase history page could be done using two transactions: one for retrieving the purchases, and another for retrieving the user's profile.

However, when leveraging the TypeDB reasoning engine, it is sometimes beneficial to reuse the same read transactions to warm up the reasoning caches.