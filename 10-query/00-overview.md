---
pageTitle: Graql Queries
keywords: graql, query, reserved keywords
longTailKeywords: graql queries, graql query structure, graql reserved keywords
Summary: Introduction to Graql queries.
permalink: /docs/query/overview
---

## Graql Query Language

Graql is the query language for the Grakn knowledge graph. Whether it's through the [Grakn Console](/docs/running-grakn/console) or one of the [Grakn Clients](/docs/client-api/overview), Grakn accepts instructions and provides answers only in its own language - Graql.

**Graql is declarative**.
When writing Graql queries, we simply describe **what** information we would like to retrieve, rather than **how** should it be obtained.
Once we specify the target information to retrieve, the Graql query processor will take care of finding an optimal way to retrieve it.

**Graql is intuitive**.
Graql was designed to provide a high-level query language interface with clear and human-readable syntax. By defining high-level application-specific [schema](/docs/schema/overview), we effectively define our own vocabulary to talk about the domain of interest. By introduction of an explicit data model tightly reflected in the structure of the query language, formulating queries comes naturally as it is reminiscent of building ordinary sentences about our domain. The more tightly the schema represents our domain of interest, the more intuitive writing and reading Graql queries become.

**Graql serves as both the Data Manipulation Language (DML) as well as the Data Definition Language (DDL)**
Graql is a language that provides you with a complete set of tools to perform all data-oriented tasks. This includes defining the schema, retrieving information as well as creating and manipulating data.

## The structure of a Graql query

Let's look at the anatomy of a typical Get query:

![Query structure](/docs/images/query/query-structure.png)

The important parts were marked with numbers. As a result, we have:

1. The **`match` keyword** that indicates what follows is a pattern expected to be looked for within the knowledge graph. The `match` keyword and the preceding pattern, commonly known as the _match clause_, is always accompanied by a _query keyword_. In the example above, that query keyword happens to be `get`. `match` may also be accompanied with, `insert` and `delete`.

2. The **query pattern** that describes the part of the knowledge graph we are interested in. Notice that unlike most other query languages, **the order of patterns in a Graql query does not matter**. The system will take care of putting it in the correct order and execute the query in the most efficient way it can.

3. The **query keyword** that specifies what the query actually does. In the case of `get` and `delete` queries, the keyword is followed by variables previously defined in the match clause. In the case of `insert` queries, what follows is one or more statements that describe the instances to be inserted.

4. One or more optional **modifiers** specify any modification operation to be carried out on the results. Here we can control the order in which they should be displayed, the number of results you want or a specific offset.

In the following sections, we learn how to create Graql queries of different types in order to:
- retrieve data
    * [Get](/docs/query/get-query) back desired data/knowledge
    * [Aggregate](/docs/query/aggregate-query) values over a set of data
    * [Compute](/docs/query/compute-query) distributed analytics over a large set of data

- define and undefine schema
    * [Define/Undefine](/docs/query/schema/concepts) new instances of concept types into the knowledge graph

- insert and remove data
    * [Insert](/docs/query/insert-query) new instances of concept types into the knowledge graph
    * [Delete](/docs/query/delete-query) instances of concept types from the knowledge graph

- manipulate data
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
```