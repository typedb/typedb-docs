---
pageTitle: Best practices
keywords: api, typedb, typeql, optimization, query, design, tips
longTailKeywords: TypeDB best practice, query design, schema design
Summary: Best practices for schema and query design.
---

# Best practices

## Schema modelling

### Tips for beginners

There are only three base types (excluding roles):

* An **attribute** is a single concept with a fixed value in a given domain. That attribute is a property of the domain rather than of its 
  owners, and so is not uniquely defined by any concepts that might own it, nor does it require any owners to exist: a name of value "Bob" can be owned by either no one, one particular person, or multiple people.
* An **entity** is a single concept with an independent existence. It might practically require other entities to 
  exist, such as a car that cannot exist without its parts, but can be conceptualized without reference to those 
  other entities: a car can be imagined without considering its parts.
* A **relation** is a single concept with an existence that depends on at least one other concept. It cannot be 
  conceptualized without those concepts: it is impossible to imagine a marriage without considering its spouses.

Please see the following tips for modelling your schema:

* The best way to start modelling your database schema is to model entity types first and then proceed with connecting 
  them with relation types and assign ownership of attribute types to them later.
* Try to create your schema as close to the data model as possible, including naming the types, building subtype 
  hierarchy and connecting relations. That will make queries sound natural.
* Creating a schema is an iterative process. Don't forget that schema of a database can be updated. Consider testing your schema on a 
  small dataset first. The sooner the schema will be adapted to all use cases and tested for edge cases — the 
  smaller amount of work will be required to adapt all other code for changes in the schema.
* Implementing drastic changes to your database schema is possible by undefining old types/rules (after undefining 
  all subtypes and deleting all instances of data of these types) and defining new ones. You can even use the Client API 
  or TypeDB Studio to rename types without deleting them. However, it might be easier to create a new database and 
  upload your new schema and data from scratch.
* It’s easier to debug queries using TypeDB Studio, than with any TypeDB Driver, because Studio manages sessions 
  and transactions for you, and can visualise query results.

### Advanced tips

The following principles are considered being useful to take into account when you develop a more sophisticated 
database schema:

* When inserting instances of a relation, it is not necessary to define all of its **role players**. But this 
  represents an incomplete information state, such as a marriage in which only one of the spouses is known. While a 
  relation can be instantiated with only one role player, and sometimes a relation can logically exist without some of its 
  role players, it's not always the case. So an instance of a relation can imply the existence of its missing role players.
* In an n-ary relation, every combination of (**n-1**)-ary relation between its role players should be valid.
  For example, a ternary relation between an actor, a film, and a role is valid because the following binary 
  relations are valid:
  * actor and film, 
  * actor and role, 
  * film and role.
* TypeQL extends the relational functionality of SQL and strongly types it, by separating entities and relations 
  into distinct **concepts** with distinct attributes. 

    Relational tables (SQL) are homogeneous in that they can be used both to represent a list of relation's role players 
    (a join table) or a list of entity's attributes (a regular table). These two types of table are indistinguishable 
    from the perspective of an SQL database engine without additional context or constraints.

* Each schema construct incurs a computational cost when traversed as part of a data query. Sorted in the order of 
  **increasing** cost, the constructs are:

1. Attributes
2. Entities
3. Subtypes
4. Binary relations
5. N-ary relations
6. Rules

   Thus, it is important to consider the value of employing a rule, as the gain in query simplicity can be offset by
   the computational cost.

* Composition (using role names to describe the functions that entities/relations perform) is generally preferred over 
  **inheritance** (using subtyping to describe those functions). This is because a type `a` should be a subtype of 
  `b` if every instance of `a` is necessarily also an instance of `b` (within the domain). For example, making `car`
  a subtype of `product` should be avoided as not every car is necessarily a product. The most general approach 
  would be to make `car` a subtype of `vehicle` and then have `car` play the role of `product` in, for instance, a 
  `purchase` relation.

  In domains where cars are always products, for instance in a car dealership database (that might also sell 
  other products: parts, add-ons, and extended warranties, etc.), it might be safe to make it a subtype of 
  `product`, however this then means that the database cannot scale to consider cars in contexts other than being 
  products. This could be a worthwhile tradeoff in very well specified models.

## Developing a query

TypeDB query engine will try to retrieve/process all required concepts in the most optimal and efficient way.

If you have a problem with your query, we recommend trying to execute it with TypeDB Studio just to see whether 
the problem lies within the query itself, or other parts of applications logic, like connection control.

To optimise execution time of your query try to do the following:

* Limit the number of concepts being processed by adding additional [constraints](03-match.md#patterns-overview) to 
  variables in your `match` clauses.
* Limit the number of results returned by using pagination (limit + offset) or [aggregation](05-read.md#aggregation) 
  when possible.
* Disable inference if you don’t need it in your transaction. 
* Consider sending all queries that you can before starting to iterate through responses. TypeDB process most queries asynchronously.

### Async Queries

All TypeQL queries sent to a TypeDB server, will be processed by it asynchronously. Local 
processing can take place while waiting for responses to be received. Take advantage of these asynchronous queries 
to mask network round-trip costs and increases throughput. For example, to perform 10 get queries in a transaction, 
it's best to send them all to the server before iterating over any of their answers.

Queries that return answers, such as get, insert return them as Streams/Iterators or Futures. These can then be 
awaited, or iterated, to retrieve the answers as they are computed.

<div class="note">
[Important]
When a transaction is committed or closed, all of its asynchronous queries are completed first.
</div>

### API

Data retrieved from a TypeDB database consists of concepts and delivered in the form of 
[ConceptMaps](07-response.md#conceptmap). Use the methods introduced by the TypeDB Client API to obtain more 
information about the retrieved concept. To explore the concept's surroundings, the API has methods to traverse the 
neighbours of a specific concept instance to obtain more insights.

<div class="note">
[Important]
When retrieving a large number of concepts it is more efficient to do that with a TypeQL query.
</div>

### Troubleshooting

The following are some of the most common mistakes and misunderstandings that could cause errors.

#### Get clause alters results

Using an optional [get](05-read.md#get-query) clause can alter the set of returned results. For example:

<!-- test-ignore -->
```typeql 
match $p isa person, has full-name $n; get $n;
```

The above query returns full-names (`$n`) owned by `$p` of the `person` type. 

Are we to expect to have a full name for every person instance in the results? No.

1. A person can have more than one attribute of type `full-name`. Every instance of attribute will get to the results.
2. A person can have no attributes of type `full-name`. In that case the person will not be represented by variable 
   `$p`. That will person will not be accounted for.
3. Finally, different people can have the same full names. In TypeDB that means different instances of `person` type 
   can own the same instance of `full-name` type. By filtering results to get only full-names you will receive a
   deduplicated list of full-names. Because it's just a list of all attributes owned by `$p` type. 

To get complete information about all full names of every person, we need to modify the query as follows:

<!-- test-ignore -->
```typeql 
match $p isa person, has full-name $n; get $p, $n;
```

With this slight alteration (we added variable `$p` to the `get` clause) the response will consist of pairs of 
`person` type object and its owned `full-name` attribute. Because of the `person` object in the response any 
repeated full names (represented in a database by the very same single attribute) will now be returned in pair with 
their owner. If a person has two `full-name` attributes, then the resulting response will contain two pairs with the 
same `person` object but different `attributes`.

We can further improve the output by [grouping](05-read.md#group) the results by `person` and/or applying 
[aggregation](05-read.md#aggregation) to count the number of results.
