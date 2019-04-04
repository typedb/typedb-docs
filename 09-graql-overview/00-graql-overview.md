---
pageTitle: Graql Overview
keywords: graql, query, reserved keywords
longTailKeywords: graql queries, graql query structure, graql reserved keywords
Summary: Query Language Overview.
---

## Graql Query Language

Graql is the query language for the Grakn knowledge graph. The majority of the interaction with Grakn happens via the query language - whether it is through the [Grakn Console](../02-running-grakn/02-console.md) or one of the [Grakn Clients](../03-client-api/00-overview.md).
Therefore, in this section we aim to give an overview of the query language.


## Graql design motivations

**Simplicity**

Graql was designed to be intuitive and simple such that it can offer extensive capabilities within a short learning time. By learning a handful of simple keywords the user can already write complex and expressive queries whereas advanced features can be learnt on the fly and depending on needs.

**Close to natural language**

We wanted the user to be able to talk about domains of interest in a language he is familiar with. Making the language schema-first allows that as for each specific application, the user defines his own domain vocabulary - the schema, which is explicitly reflected in the query language.

**Human-readable and concise**

We wanted the language to be clean and readable for a majority of users. As a results, we used keywords that occur in everyday conversations to create basic constructs of the language. In that way, writing queries feels more natural and aligned with creating normal sentences.

**High-level semantics**

One of the main design goals was to abstract the graph structure details from the user so that we don't have to think about the underlying representation in terms of nodes and edges. Instead we can focus on the high-level representation which is aligned with a specific domain.

## Why to use Graql

**Graql is declarative**.

When writing Graql queries, we simply describe **what** information we would like to retrieve, rather than **how** should it be obtained.
Once we specify the target information to retrieve, the Graql query processor will take care of finding an optimal way to retrieve it.

**Graql is schema-first**

All Graql queries operate based on a user-defined, application-specific [schema](../10-schema/00-overview.md) that defines and controls the high-level vocabulary of our domain. Thanks to schema we can provide data integrity and consistency guarantees as well as explicit semantics for the queries.

**Graql is intuitive**.

Graql was designed to provide a high-level query language interface with clear and human-readable syntax. By defining the high-level application-specific, we define our own vocabulary to talk about the domain of interest. As a result, formulating queries comes naturally as it is reminiscent of building ordinary sentences about our domain. The more tightly the schema represents our domain of interest, the more intuitive writing and reading Graql queries become.

**Graql serves as both the Data Manipulation Language (DML) as well as the Data Definition Language (DDL)**

Graql is a language that provides you with a complete set of tools to perform all data-oriented tasks. This includes defining the schema, retrieving information as well as creating and manipulating data.

**Rooted in logics**
Graql takes great inspiration from logics and logic languages such as Datalog or Prolog. People familiarised with those topics should feel at home when using Graql.


## Language features
**Expressive querying in near natural language**
Being schema-first with the Extended Entity-Relationship model as a data model, Graql is a simple yet expressive query language where writing queries closely mimicks writing sentences in natural languages.

**Strong abstraction over low-level details**
Graql provides a high-level abstraction over the graph and query structure, allowing for simpler expressions of complex constructs, while the system determines the most optimal query execution.

**Rule-based reasoning as an integral part of the language**
Graql is equipped with rule-based reasoning facilities by design. This allows to perform deductive inference tasks seamlessly by writing standard queries.

**Distributed analytics as a n integral part of the language**
Graql provides out-of-the-box distributed analytics (Pregel and MapReduce) algorithms, accessible through the language through simple queries.

**Support for recursion**
Graql queries allow for recursive constructs which are expressed via suitably defined rules. General forms of recursion are allowed - first order, mutual, transitive and beyond.

**Support for negation**
Graql is equipped with a negation operator allowing for formulating queries involving exclusions.

**Lazy execution**
All queries are evaluated in a call-by-need strategy - the answer retrieval is delayed until needed. This allows to stream query answers, define answer pipelines and control flows and avoid needless answer evaluations.
