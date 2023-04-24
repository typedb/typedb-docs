---
pageTitle: Managing Databases
keywords: typedb, database
longTailKeywords: typedb database
Summary: Creating, listing and deleting TypeDB Databases.
toc: false
---

## What is a Database?
A database is the outermost container for data in a TypeDB knowledge graph. As per a relational database, it is commonly known to be good practice to create a single database per application, but it is absolutely fine to create as many databases as your application needs. As a rule of thumb, it is recommended to start off with one database and create more if the requirement arises.

<div class="note">
[Important]
Databases are isolated from one another. Even when running on the same TypeDB Server, it is not possible to perform operations from one database on another one.
</div>

### Creating a Database
We can create a new a database via the TypeDB Clients ([Java](../02-clients/java/01-java-overview.md), [Node.js](../02-clients/node-js/01-node-js-overview.md) and [Python](../02-clients/python/01-python-overview.md)) as well as [TypeDB Console](../02-console/01-console.md) and [Studio](../07-studio/01-quickstart.md).

### Listing All Databases
We can list all databases of the running TypeDB server via the TypeDB Clients [Node.js](../02-clients/node-js/01-node-js-overview.md#retrieve-all-databases) and [Python](../02-clients/python/01-python-overview.md#retrieve-all-databases), as well as [TypeDB Console](../02-console/01-console.md) and [Studio](../07-studio/01-quickstart.md).

### Deleting a Database
We can delete a database via the TypeDB Clients [Java](../02-clients/java/01-java-overview.md#delete-a-database), [Node.js](../02-clients/node-js/01-node-js-overview.md#delete-a-database) and [Python](../02-clients/python/01-python-overview.md#delete-a-database), as well as [TypeDB Console](../02-console/01-console.md) and [Studio](../07-studio/01-quickstart.md).

### Renaming a Database
Once we have created a database, its name can no longer be changed. The only way to achieve a renamed database is to [migrate](../06-management/04-migration-and-backup.md) the data from the database with the old name to the newly created database.
