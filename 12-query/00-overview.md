---
pageTitle: Graql Queries
keywords: graql, query, reserved keywords
longTailKeywords: graql queries, graql query structure, graql reserved keywords
Summary: Introduction to Graql queries.
---

## The structure of a Graql query

The image below illustrates the structure of various Graql queries.

![Query structure](../images/query/query-structure.png)

As shown in the image above, Graql queries are categorized into two main types:
- **Data Definition**:
  - **[Define](../10-schema/01-concepts.md#define)**: adds definition of a concept type to the schema.
  - **[Undefine](../10-schema/01-concepts.md#undefine)**: removes definition of a concept type from the schema.

- **Data Manipulation**:
  - **[Get](../12-query/02-get-query.md)**: returns the data instances or concept types that match the preceding pattern(s), optionally limited by, sorted by or offset by the given modifiers.
  - **[Delete](../12-query/04-delete-query.md)**: removes the data instances assigned to the given variable that match the preceding pattern(s), optionally limited by, sorted by or offset by the given modifiers.
  - **[Insert](../12-query/03-insert-query.md)**: inserts a data instance according to the given statement(s), optionally, preceded by a `match` clause.
  - **[Group](../12-query/06-aggregate-query.md#grouping-answers)**: always as a part of a `get` query, returns the results grouped by the given variable, optionally mapped to the count of each group.
  - **[Aggregate Values](../12-query/06-aggregate-query.md#aggregate-values-over-a-dataset)**: always as a part of a `get` query, returns the statistical value of numeric attributes based on the given aggregate function.
  - **[Compute Statistics](../12-query/07-compute-query.md)**: computes paths between two instances, clusters and centrality.

## Graql Answers

Some Graql queries such as `get`, `aggregate` and `compute` are expected to return an answer. Depending on the type of query, the structure of the answer may be different (more on Answer types in the [Client API](../03-client-api/00-overview.md#investigating-answers) section). As a part of the [Concept API](../04-concept-api/00-overview.md), we can call various methods on the concepts contained in an answer to retrieve more explicit and implicit knowledge about them and their surroundings.

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