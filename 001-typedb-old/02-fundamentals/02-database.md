---
pageTitle: Database
keywords: database
longTailKeywords: typedb database
summary: TypeDB database concept.
toc: false
---

<!--- 
Logically separate data, cannot touch each other (eg. stored in separately directories) & therefore copyable independently etc.,, not optimised for many (1-10s), database contains schema + data
-->

# Database

A database is the outermost container for data in a TypeDB knowledge graph. Like a relational database, it is commonly 
known to be a good practice to create a single database per application, but it is absolutely fine to create as many 
databases as your application needs. As a rule of thumb, it is recommended to start off with one database and create 
more if the requirement arises.

<div class="note">
[Note]
TypeDB optimised for lesser number of databases. So the best practise would be to keep no more than 10 databases on 
TypeDB server.
</div>

Databases are isolated from one another. Even when running on the same TypeDB Server, it is not possible to connect to
one database but perform operations on another one. But you can connect to multiple databases simultaneously.

A database is made of [schema](../../09-schema/00-overview.md), and [data](../../11-query/00-overview.md).
