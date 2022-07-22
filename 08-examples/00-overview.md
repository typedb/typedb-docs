---
pageTitle: TypeDB Examples
keywords: typedb, examples, migration, queries, schema
longTailKeywords: typedb examples, typedb migration, typedb query examples, typedb schema example
Summary: TypeDB examples showcasing schema definition, data migration and retrieval queries
---

## Examples

[**Telecoms - Phone Calls (Java, JS, Python):**](https://github.com/vaticle/typedb-examples/tree/master/phone_calls) a database of customers of a fictional telecom company and calls they make.

[**Gaming - XCOM 2 (Java):**](https://github.com/vaticle/typedb-examples/tree/master/xcom) a database of interdependent research tasks in the game XCOM 2, featuring automatic inference of available research based on completed tasks and available items.

[**Biology - Catalogue of Life (Java):**](https://github.com/vaticle/typedb-examples/tree/master/catalogue_of_life) a database containing the information about the taxonomy of life on Earth, showcasing (semi-)automatic loading of data using [TypeDB-Loader.](https://github.com/typedb-osi/typedb-loader)

[**Software Dev - GitHub (Kotlin):**](https://github.com/vaticle/typedb-examples/tree/master/github) Load data from a live repository on GitHub or from a Vaticle GitHub snapshot, and get results via a custom GUI interface that uses the Java client to fetch the requested data.

## A hands-on walkthrough

To get a better idea of how you can use TypeDB, we'll take a closer look at the [`phone_calls` example.](https://github.com/vaticle/typedb-examples/tree/master/phone_calls)
The database we'll be working on in this series contains a dataset of **people** who **call** each other. Those who have a **contract** with the **company** also have their **name**, **age**, and the **city** they reside in recorded within the database.

In the following three sections, we together:

1. Define the [schema](../08-examples/01-phone-calls-schema.md) for our `phone_calls` database
2. Migrate csv, json or xml data to the database using clients [Java](../08-examples/02-phone-calls-migration-java.md), [Node.js](../08-examples/03-phone-calls-migration-nodejs.md) and [Python](../08-examples/04-phone-calls-migration-python.md)
3. [Query](../08-examples/05-phone-calls-queries.md) the database

