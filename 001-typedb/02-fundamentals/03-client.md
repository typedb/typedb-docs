---
pageTitle: Session
keywords: typedb, session
longTailKeywords: typedb session
summary: TypeDB session concept.
toc: false
---

<!--- 
A grouping of transactions, access either schema or data - schema is “admin” type and prevents data write transactions opening, can be opened with session-wide options.
-->

# What is a TypeDB Client?

A TypeDB client is an interface which we can use to read from and write to a TypeDB knowledge graph.

List of TypeDB clients:

- [TypeDB Console](../02-console/01-console.md)
- [TypeDB Studio](../07-studio/00-overview.md)
- [TypeDB libraries / drivers](../03-client-api/00-overview.md)
    - Supported libraries
        - [**Java**](../03-client-api/01-java.md)
        - [**Node.js**](../03-client-api/03-nodejs.md)
        - [**Python**](../03-client-api/02-python.md)
    - [Other drivers](../03-client-api/04-other-languages.md)

If we are building an application that uses a TypeDB knowledge graph as its database, we would need a TypeDB client at 
our application layer to handle the [database](../06-management/01-database.md) operations. Such a client could be one 
of the TypeDB libraries or TypeDB Console.

![Structure of a TypeDB Client Application](../../images/client-api/client-server-comms.png)

## Architecture
All TypeDB Clients share a common architecture. Simply put, the main components of a TypeDB client are the `interfaces`,
`client` itself, [session](04-session.md) and [transaction](05-transaction.md).

### Interfaces

Any interface used to interact with the client. It can be:

- GUI (Graphic users interface), like TypeDB Studio.
- API (Application programming interface), like TypeDB drivers.
- CLI (Command line interface), like TypeDB Console.

### Client

Client handles remote connection to the [TypeDB Server](/docs/typedb/install-and-run#start-the-typedb-server). 
We then use this connection to manage [databases](../06-management/01-database.md) and open [sessions](04-session.md).

<div class="note">
[Note]
Best practice is to use one client per application process.
</div>
