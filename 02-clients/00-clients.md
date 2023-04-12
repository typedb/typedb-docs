---
pageTitle: TypeDB Clients
keywords: typedb, console, studio, client, api, drivers
longTailKeywords: typedb client api, typedb api, client api, typedb studio, typedb console
Summary: All you need to know about the architecture of a TypeDB Client.
toc: false
---

# Clients

## Overview

A TypeDB Client is meant to be used for the purpose of managing databases and performing operations (querying) with a
database schema and data on the TypeDB server. A client uses `gRPC` to interact with a TypeDB server and provides 
more user-friendly interface: API, GUI or CLI.

Here is a list of existing TypeDB Clients:

- Software tools:
  - [TypeDB Studio](01-studio.md)
  - [TypeDB Console](02-console.md)
- [TypeDB drivers](#typedb-drivers) — libraries to connect to a TypeDB server with an application. There are:
  - Native drivers:
    - [Java](03-java.md)
    - [Python](04-python.md)
    - [Node.js](05-nodejs.md)
  - [Community drivers](06-other-languages.md)

If you can't find a suitable client, consider [creating a new client](07-new-client.md).

## Architecture

All TypeDB Clients share a common architecture. Simply put, the main components of any TypeDB Client are the classes 
and methods to establish a connection to a TypeDB database, execute queries and parse responses.

Specific information on the classes and methods provided in the API reference, but the syntax may vary for different 
programming languages.

## Software tools

To work with TypeDB databases we can use one of the standalone software tools:

1. [TypeDB Studio](01-studio.md) (GUI).
2. [TypeDB Console](02-console.md) (CLI).

Both tools are complete software products that can be used to connect to TypeDB and interact with it.

TypeDB Studio is mostly remarkable for its friendly graphical user interface, types explorer and graph visualization.
TypeDB Console is a powerful CLI tool often used to manage TypeDB server and its databases.

## TypeDB drivers

If we are developing our own application (software) we can use one of the libraries (or drivers) that are available for 
some popular programming languages.

The following TypeDB drivers are officially supported and actively maintained by the Vaticle. They 
usually support latest TypeDB features and receive continuous bug fixes and improvements.

- [Java](03-java.md)
- [Node.js](05-nodejs.md)
- [Python](04-python.md)

We also have some community projects for [other Languages](06-other-languages.md)

### What is a TypeDB driver?

A TypeDB driver, is a library which we can use to read from and write to a TypeDB database. If we are building an 
application that uses a TypeDB database, we would need a TypeDB driver at our application layer to handle the
database operations.

![Structure of a TypeDB Client Application](../images/client-api/client-server-comms.png)

### Async Queries

Invoking a TypeQL query sends the query to the TypeDB server, where it will be completed in the background. Local 
processing can take place while waiting for responses to be received. Take advantage of these asynchronous queries to 
mask network round-trip costs and increases your throughput. For example, if you are performing 10 match queries in a 
transaction, it's best to send them all to the server _before_ iterating over any of their answers.

Queries that return answers, such as [match](../0001-typedb/02-dev/03-match.md), return them as Futures, Streams or 
Iterators depending on the language. These can then be awaited, or iterated, to retrieve the answers as they are 
computed.

<div class="note">
[Important]
When a transaction is committed or closed, all of its asynchronous queries are completed first.
</div>

### Investigating Answers

Depending on the type of the query carried out by a transaction, we retrieve different forms of answers. These answers, 
regardless of their type, all contain concepts. We can then use the methods introduced by the 
[Concept API](../0001-typedb/02-dev/08-api.md) to obtain more information about the retrieved concept and its 
surroundings. Furthermore, the Concept API allows us to traverse the neighbours of a specific concept instance to obtain 
more insights.

## Summary

A TypeDB Client is meant to be used for the purpose of managing and performing operations over databases that live on 
the TypeDB server.
