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

The image below illustrates the structure of various Graql queries.

![Query structure](/docs/images/query/query-structure.png)

As shown in the image above, Graql queries are categorized into two main types:
- **Data Definition**:
  - **[Define](/docs/query/schema/concepts#define)**: adds definition of a concept type to the schema.
  - **[Undefine](/docs/query/schema/concepts#undefine)**: removes definition of a concept type from the schema.

- **Data Manipulation**:
  - **[Get](/docs/query/get-query)**: returns the data instances or concept types that match the preceding pattern(s), optionally limited by, sorted by or offset by the given modifiers.
  - **[Delete](/docs/query/delete-query)**: removes the data instances assigned to the given variable that match the preceding pattern(s), optionally limited by, sorted by or offset by the given modifiers.
  - **[Insert](/docs/query/insert-query)**: inserts a data instance according to the given statement(s), optionally, preceded by a `match` clause.
  - **[Group](/docs/query/aggregate-query#grouping-answers)**: always as a part of a `get` query, returns the results grouped by the given variable, optionally mapped to the count of each group.
  - **[Aggregate Values](/docs/query/aggregate-query#aggregate-values-over-a-dataset)**: always as a part of a `get` query, returns the statistical value of numeric attributes based on the given aggregate function.
  - **[Compute Statistics](/docs/query/compute-query)**: computes paths between two instances, clusters and centrality.

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