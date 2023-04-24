---
pageTitle: Response interpretation
keywords: typeql, query, response, result, answer, concept
longTailKeywords: typeql response, concept map, typeql variables
Summary: TypeDB query response interpretation.
---

# Response interpretation

TypeDB can return a response in different formats, depending on a type of query. The response will be interpreted by a 
TypeDB Client being used. TypeDB Client provides classes and methods for different response types respectively. Please 
see the table below for mapping of response format to a type of query that has been sent.

|  **#**  |             **Query type**              |          **Response format**           |
|:-------:|:---------------------------------------:|:--------------------------------------:|
|    1    |                Get query                |   Stream/Iterator of **ConceptMap**    |
|    2    |       Get query with aggregation        |       **Future** of **Numeric**        |
|    3    |         Get query with grouping         | Stream/Iterator of **ConceptMapGroup** |
|    4    | Get query with grouping and aggregation |  Stream/Iterator of **NumericGroup**   |
|    5    |              Insert query               |   Stream/Iterator of **ConceptMap**    |
|    6    |              Delete query               |     **Future** (of empty response)     |
|    7    |   Update (match-delete-insert) query    |   Stream/Iterator of **ConceptMap**    |
|    8    |                 Define                  |     **Future** (of empty response)     |
|    9    |                Undefine                 |     **Future** (of empty response)     |
|   10    |                 Explain                 | Stream/Iterator of **Explanation**     |

## Expected results

See the table above for an overview of response formats. For more details see the [Response formats](#response-formats) 
section below.

### Get query

The ordinary [get query](05-read.md#get-query) (without [aggregation](05-read.md#aggregation) or 
[grouping](05-read.md#group)) returns a stream/iterator of a ConceptMap objects. 

Every iteration returns result as a [ConceptMap](#conceptmap) object. 

### Get query with aggregation

The get query with **aggregation** can only return a singular value (aggregated result). Hence it returns a Future 
object of Numeric.

Use [Future](#future) object’s `get()` method to wait and retrieve the [Numeric](#numeric) object when it’s ready.

### Get query with grouping

The get query with **grouping** returns a stream/iterator of ConceptMapGroup objects.

Every iteration should return result as a [ConceptMapGroup](#conceptmapgroup) object. 

Use ConceptMapGroup object to retrieve [ConceptMap](#conceptmap).

### Get query with grouping and aggregation

The get query with **grouping** and **aggregation** returns a stream/iterator of a NumericGroup objects.

Every iteration should return result as a [NumericGroup](#numericgroup) object.

Use NumericGroup object to retrieve [Numeric](#numeric).

### Insert query

An insert query returns a stream/iterator of a ConceptMap objects. 

Every iteration should return result as a [ConceptMap](#conceptmap) object. 

### Delete query

A delete query can only return a Future object of a void (empty response).

We can’t retrieve any useful data from the Future object for a delete query.

### Update (match-delete-insert) query

Similar to an [insert](#insert-query) query.

### Define query

Similar to a [delete](#delete-query) query.

### Undefine query

Similar to a [delete](#delete-query) query.

### Explain

The explain query returns a stream/iterator of an Explanation objects.

For more information on inference explanation please see the [Inferring data](06-infer.md) page. 

## Response formats

[TypeDB Studio](../../02-clients/01-studio.md) and [TypeDB Console](../../02-clients/02-console.md) process the 
responses automatically to present the results (in GUI and CLI respectively) to the user. 

For [TypeDB Drivers](../../02-clients/00-clients.md#typedb-drivers): the specific methods/calls used to interpret the 
response depend on the TypeDB Driver used. 

The following is a very basic description of objects used to interpret the results from the TypeDB query response. 
For more information please see the [API & Drivers](08-api.md) page and documentation for the 
[Java](../../02-clients/java/01-java-overview.md), 
[Python](../../02-clients/python/01-python-overview.md), and 
[Node.js](../../02-clients/node-js/01-node-js-overview.md) TypeDB Drivers respectively.

### ConceptMap

ConceptMap is a special object, made for mapping of variables from a query to concepts in a database. Its methods 
provide a way to interact with the concepts. 

Usually represents a single solution/answer from a stream of answers for a TypeDB query.

### ConceptMapGroup

It’s a container for a [ConceptMap](#conceptmap) object with an owner. 

### Concept

Object to represent a type or an instance of a type (data) from a database. 

There are separate methods for every of the base types (entity type, attribute type and relation type) or for 
instances of every base type (entity, attribute or relation).

### Numeric

Numeric object represents a numeric value.

### NumericGroup

NumericGroup object has not only a Numeric object but also an owner.

### Future

Future object represents an asynchronous query result to be able to get the value later, when query execution completes. 

### Explanation

Explanation is a special object returned as a response to an explain query. 
These are used to explain [data inference](06-infer.md). To perform an [explain query](06-infer.md#explain-query) 
use `explainables` and `explainable` objects.

## Number of answers

If the query type can return **multiple** results (e.g. a get query) then the result of such query type is a 
**stream/iterator** to iterate through all the results. Even if the actual query of such type returns one result or no 
results at all — it returns a stream/iterator with one or zero iterations respectively.

Query types that can return only a single answer or a void (an empty response) are executed fully asynchronous on the 
server. To wait for a query to finish execution, and return its result if there is one, use the `get()` method of the 
**Future** object returned by the query.

## Best practice

### Asynchronous queries

Invoking a TypeQL query sends it to a TypeDB server, where it will be completed in the background. Local processing 
can take place while waiting for responses to be received. Take advantage of these asynchronous queries to mask network 
round-trip costs and increases throughput. 

For example, if we are performing 10 get queries in a transaction, it’s best to send them all to the server before 
iterating over any of their answers.
