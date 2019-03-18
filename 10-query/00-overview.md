---
pageTitle: Graql Queries
keywords: graql, query, reserved keywords
longTailKeywords: graql queries, graql query structure, graql reserved keywords
Summary: Introduction to Graql queries.
permalink: /docs/query/overview
---

## Graql Query Language

Graql is the query language for the Grakn knowledge graph. Whether it's through the [Grakn Console](/docs/running-grakn/console) or one of the [Grakn Clients](/docs/client-api/overview), 
Grakn accepts instructions and provides answers only in its own language - Graql.

**Graql is declarative**. 
When writing Graql queries, you simply describe __what__ information you would like to retrieve, rather than __how__ should it be obtained. 
Once we specify the target information to retrieve, the Graql query processor will take care of finding an optimal way to retrieve it.

**Graql is intuitive**. 
Graql was designed to provide a high-level query language interface with a clear and human-readable syntax. By defining high-level application specific [schema](/docs/schema/overview), 
we effectively define our own vocabulary to talk about the domain of interest. By introduction of explicit data model tightly reflected in the structure of the query language,
formulating queries comes naturally as it is reminiscent of building ordinary sentences about our domain. The more tightly the schema respresents our domain of interest, the more intuitive writing and reading Graql queries become.

**Graql serves as both the Data Manipulation Language (DML) as well as the Data Definition Language (DDL)**
Graql is a language that provides you with a complete set of tools to perform all data oriented tasks: including definition of the schema and creation of data as well as data manipulation: retrieval and updates. 


## The structure of a Graql query

Let's look at the anatomy of a typical Match-Get query:

![Query structure](/docs/images/query/query-structure.png)

The important parts were marked with numbers, as a result we have:

  1. A __query keyword__ specifying the query type and subsequently the nature of the operation we want the query to carry out. In that way we can differentiate between data manipulation and update operations(`match`, `compute`), 
  as well as data definition operations (`define`, `insert`).
  
  1. A __query pattern__ part. The pattern describes the part of the knowledge graph we are interested in.
  Notice that differently from what normally happens with query languages, **the order of patterns in a Graql query does not matter**: the system will take care of putting it in the correct order and execute 
  the query in the most efficient way it can.

  1. A mandatory __action__ that actually specifies what the query does. With some exceptions, this take the form of a keyword followed by variables. The action defines the type of the query as well (`get`, `insert`, `delete`...)
  
  1. One or more optional __modifiers__. This specify any modification operation to be carried out on our results. Here we can control the order in which they should be displayed, the number of results you want or a specific offset.

In the following sections, we learn how to create Graql queries of different types in order to:
- retrieve data
    * [Match](/docs/query/match-clause) specific patterns in the data and schema   
    * [Get](/docs/query/get-query) back desired data/knowledge

- define and undefine schema
    * [Define/Undefine](/docs/query/schema/concepts) new instances of concept types into the knowledge graph

- insert and remove data
    * [Insert](/docs/query/insert-query) new instances of concept types into the knowledge graph
    * [Delete](/docs/query/delete-query) instances of concept types from the knowledge graph

- manipulate data
    * [Aggregate](/docs/query/aggregate-query) values over a set of data
    * [Compute](/docs/query/compute-query) distributed analytics over a large set of data
    * [Update](/docs/query/update-query) instances of concept types

## Graql Answers
Some Graql queries such as `get`, `aggregate` and `compute` are expected to return an answer. Depending on the type of query, the structure of the answer may be different (more on Answer types in the [Client API](/docs/client-api/overview#investigating-answers) section). As a part of the [Concept API](/docs/concept-api/overview), we can call various methods on the concepts contained in an answer to retrieve more explicit and implicit knowledge about them and their surroundings.

## Reserved Keywords
The following keywords are reserved and meant to only be used by Graql in the queries.
<!-- test-ignore -->
```graql
asc
by
compute, contains, count
delete, desc
from
get, group
id, in, insert
label, limit
match, max, mean, median, min
offset, order
regex
std, sum
to
val
```