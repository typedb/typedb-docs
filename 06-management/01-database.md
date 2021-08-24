---
pageTitle: Managing Databases
keywords: typedb, database
longTailKeywords: typedb database
Summary: Creating, listing, cleaning and deleting TypeDB Databases.
toc: false
---

## What is a Database?
A database is the outermost container for data in a TypeDB knowledge graph. As per a relational database, it is commonly known to be good practice to create a single database per application, but it is absolutely fine to create as many databases as your application needs. As a rule of thumb, it is recommended to start off with one database and create more if the requirement arises.

<div class="note">
[Important]
Databases are isolated from one another. Even when running on the same TypeDB Server, it is not possible to perform operations from one database on another one.
</div>

### Creating a Database
We can create a new a database via the TypeDB Clients [Java](../04-client-api/01-java.md), [Node.js](../04-client-api/03-nodejs.md) and [Python](../04-client-api/02-python.md) and [TypeDB Console](../03-console/01-console.md).

### Listing All Databases
We can list all databases of the running TypeDB server via the TypeDB Clients [Node.js](../04-client-api/03-nodejs.md#retrieve-all-databases) and [Python](../04-client-api/02-python.md#retrieve-all-databases), as well as [Workbase](../07-workbase/01-connection.md#select-a-database).

### Cleaning a Database
Cleaning the database, not to be confused with deletion, wipes out both the data and the schema contained within the database. We can clean a database via [TypeDB Console](../03-console/01-console.md#console-commands).

### Deleting a Database
We can delete a database via the TypeDB Clients [Java](../04-client-api/01-java.md#delete-a-database), [Node.js](../04-client-api/03-nodejs.md#delete-a-database) and [Python](../04-client-api/02-python.md#delete-a-database).

### Renaming a Database
Once we have created a database, its name can no longer be changed. The only way to achieve a renamed database is to migrate the data from the database with the old name to the newly created database.
