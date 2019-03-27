---
pageTitle: Managing Keyspaces
keywords: grakn, keyspace
longTailKeywords: grakn keyspace
Summary: Creating, listing, cleaning and deleting Grakn Keyspaces.
toc: false
---

## What is a Keyspace?
A keyspace is the outermost container for data in a Grakn knowledge graph, corresponding closely to a relational _database_. As per a relational database, it is commonly known to be good practice to create a single keyspace per application, but it is absolutely fine to create as many keyspaces as your application needs. As a rule of thumb, it is recommended to start off with one keyspace and create more if the requirement arises.

<div class="note">
[Important]
Keyspaces are isolated from one another. Even when running on the same Grakn Server, it is not possible to perform operations from one keyspace on another one.
</div>

### Creating a Keyspace
We can create a new a keyspace via the Grakn Clients [Java](../03-client-api/01-java.md#client-api-method-create-a-session-keyspace), [Node.js](../03-client-api/03-nodejs.md#client-api-method-create-a-session-keyspace) and [Python](../03-client-api/02-python.md#client-api-method-create-a-session-keyspace) and [Grakn Console](../02-running-grakn/02-console.md#console-options).

### Listing All Keyspaces
We can list all keyspaces of the running Grakn server via the Grakn Clients [Node.js](../03-client-api/03-nodejs.md#client-api-method-retrieve-all-keyspaces) and [Python](../03-client-api/02-python.md#client-api-method-retrieve-all-keyspaces), as well as [Workbase](../07-workbase/01-connection.md#select-a-keyspace).

### Cleaning a Keyspce
Cleaning the keyspace, not to be confused with deletion, wipes out both the data and the schema contained within the keyspace. We can clean a keyspace via [Grakn Console](../02-running-grakn/02-console.md#console-commands).

### Deleting a Keyspace
We can delete a keyspace via the Grakn Clients [Java](../03-client-api/01-java.md#client-api-method-delete-a-keyspace), [Node.js](../03-client-api/03-nodejs.md#client-api-method-delete-a-keyspace) and [Python](../03-client-api/02-python.md#client-api-method-delete-a-keyspace).

### Renaming a Keyspace
Once we have created a keyspace, its name can no longer be changed. The only way to achieve a renamed keyspace is to migrate the data from the keyspace with the old name to the newly created keyspace.