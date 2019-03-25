---
sidebarTitle: Overview
pageTitle: Graql Queries
permalink: /docs/query/overview
---

## Graql Instructions
Graql is the language for the Grakn knowledge graph. Whether it's through the [Graql Console](/docs/running-grakn/console) or one of the [Grakn Clients](/docs/client-api/overview), Grakn accepts instructions and provides answers only in its own language - Graql.

**Graql is declarative**. In simple terms, when writing Graql code, you simply describe _what_ you would like to achieve, rather than _how_ it's going to get there. The implementation of a Graql query is hidden under the hood and never affects you as the developer.

**Graql is intuitive**. Graql queries can look a lot like questions the same way they are formed in mind, as opposed to a complicated series of statements that are difficult to follow and, at scale, become confusing. It's important to note that the intuitiveness of a Graql query originates from the [schema](/docs/schema/overview). The better the knowledge graph represents the reality of its dataset via its schema, the more intuitive writing and reading Graql queries become.

In this section, we learn how a Graql query can be written to:
- [Match](/docs/query/match-clause) specific patterns in the data and schema
- [Insert](/docs/query/insert-query) new instances of conept types into the knowledge graph
- [Get](/docs/query/get-query) back desired data/knowledge
- [Aggregate](/docs/query/aggregate-query) values over a set of data
- [Delete](/docs/query/delete-query) instances of concept types from the knowledge graph
- [Compute](/docs/query/compute-query) distributed analytics over a large set of data
- [Update](/docs/query/update-query) instances of concept types

## Graql Answers
Some Graql queries such as `get`, `aggregate` and `compute` are expected to return an answer. Depending on the type of query, the structure of the answer may be different (more on Answer types in the [Client API](/docs/client-api/overview#investigating-answers) section). As a part of the [Concept API](/docs/concept-api/overview), we can call various methods on the concepts contained in an answer to retrieve more explicit and implicit knowledge about them and their surroundings.

## Reserved Keywords
The following keywords are reserved and meant to only be used by Graql in the queries.

```graql
aggregate, asc
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

## Summary
Graql is a powerful language that is easy to learn, write and read.

In the sections that follow, we learn about how we can use Graql to query and modify the data instances as well as the underlying schema.