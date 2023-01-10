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

Database is an isolated namespace inside the TypeDB server. All connections are made to one of the databases on the 
TypeDB server.

A database is the outermost container for data in a TypeDB knowledge graph. As per a relational database, it is commonly 
known to be a good practice to create a single database per application, but it is absolutely fine to create as many 
databases as your application needs. As a rule of thumb, it is recommended to start off with one database and create 
more if the requirement arises.

Databases are isolated from one another. Even when running on the same TypeDB Server, it is not possible to perform operations from one database on another one.

