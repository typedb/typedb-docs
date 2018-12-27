---
title: Java
keywords: setup, getting started, download, driver
tags: [getting-started]

permalink: /docs/client-api/java
---

## Declaring The Dependency In Maven
All applications will require the `client-java` dependency to be declared on the `pom.xml` of your application.

```xml
<repositories>
  <repository>
    <id>releases</id>
    <url>https://oss.sonatype.org/content/repositories/releases</url>
  </repository>
</repositories>

<properties>
    <grakn.version>1.3.0</grakn.version>
</properties>

<dependencies>
  <dependency>
    <groupId>ai.grakn</groupId>
    <artifactId>client-java</artifactId>
    <version>${grakn.version}</version>
  </dependency>
</dependencies>
```

## Opening A Session And Transaction

{% include note.html content="Before proceeding, make sure that the Grakn knowledge graph has already been started. Otherwise, refer to the [Setup guide](../get-started/setup-guide#install-graknai) on how to install and start Grakn properly." %}

A **session** object is responsible for maintaining a connection to a specific keyspace in the knowledge graph. Opening a session is performed by invoking the `session()` method on the grakn client.
Once the session is open, you can proceed by creating a **transaction** in order to manipulate the data in the keyspace.

The following snippet shows how to open a Grakn session and transaction:

```lang-java-test-ignore
import ai.grakn.GraknTxType;
import ai.grakn.Keyspace;
import ai.grakn.client.Grakn;
import ai.grakn.util.SimpleURI;

public class App {
  public static void main(String[] args) {
    SimpleURI localGrakn = new SimpleURI("localhost", 48555);
    Keyspace keyspace = Keyspace.of("grakn");
    Grakn grakn = new Grakn(localGrakn);
    try (Grakn.Session session = grakn.session(keyspace)) {
      try (Grakn.Transaction transaction = session.transaction(GraknTxType.WRITE)) {
        // ...
        transaction.commit();
      }
    }
  }
}
```

## Keyspace Uniqueness
A "Keyspace" uniquely identifies the knowledge graph and allows you to create different knowledge graphs.

Please note that keyspaces are **not** case sensitive. This means that these `grakn`, `Grakn`, and `GrAkn` names refer to the same keyspace.

## Transaction Types
We currently support three transaction types:

* `GraknTxType.WRITE` - A transaction that allows mutations to be performed on the knowledge graph
* `GraknTxType.READ` - Prohibits any mutations to be performed to the knowledge graph
* `GraknTxType.BATCH` - Allows faster mutations to be performed to the knowledge graph at the cost of switching off some internal consistency checks. This option should only be used if you are certain that you are loading a clean dataset.

## Where Next?

The pages in this section of the documentation cover some of the public APIs available to Java developers:

* [Java API](./core-api)
* [Java Graql](./graql-api)
* [Migration API](./migration-api)
* [Loader API](./loader-api)

There is also a page (in progress) that discusses advanced topics in Java development, such as transactions and multi-threading.

There is an example described in our [blog](https://blog.grakn.ai/working-with-grakn-ai-using-java-5f13f24f1269#.8df3991rw) that discusses how to get set up to develop using Java, and how to work with the Java API.


The Core API is the low level API that encapsulates the [Grakn knowledge model](../knowledge-model/model). The API provides Java object constructs for ontological elements (entity types, relationship types, etc.) and data instances (entities, relationships, etc.), allowing you to build a knowledge graph programmatically.

To get set up to use this API, please read through our [Setup Guide](../get-started/setup-guide) and guide to [starting Java development with GRAKN.AI](./setup).

## Core API

On this page we will focus primarily on the methods provided by the `Grakn.Transaction` interface which is used by all knowledge graph mutation operations executed by Graql statements. If you are primarily interested in mutating the knowledge graph, as well as doing simple concept lookups the `Grakn.Transaction` interface will be sufficient.

It is also possible to interact with the knowledge graph using a Core API to form Graql queries via `Grakn.Transaction::graql()`, which is discussed separately [here](./graql-api), and is best suited for advanced querying.

## Building a Schema with the Core API

In the [Basic Schema documentation](../building-schema/basic-schema) we introduced a simple schema built using Graql.
Let's see how we can build the same schema exclusively via the Core API.
First we need a knowledge graph. For this example we will just use an
[in-memory knowledge graph](./setup#initialising-a-transaction-on-the-knowledge-base):

```lang-java-test-ignore
Grakn grakn = new Grakn(new SimpleURI("localhost:48555"));
Grakn.Session session = grakn.session(Keyspace.of("grakn"));
Grakn.Transaction tx = session.transaction(GraknTxType.WRITE);
```

We need to define our constructs before we can use them. We will begin by defining our attribute types since they are used everywhere. In Graql, they were defined as follows:

```graql
define

identifier sub attribute datatype string;
name sub attribute datatype string;
firstname sub name datatype string;
surname sub name datatype string;
middlename sub name datatype string;
picture sub attribute datatype string;
age sub attribute datatype long;
event-date sub attribute datatype date;
birth-date sub event-date datatype date;
death-date sub event-date datatype date;
gender sub attribute datatype string;
```

These same attribute types can be built with the Core API as follows:

```lang-java-test-ignore
AttributeType identifier = tx.putAttributeType("identifier", AttributeType.DataType.STRING);
AttributeType firstname = tx.putAttributeType("firstname", AttributeType.DataType.STRING);
AttributeType surname = tx.putAttributeType("surname", AttributeType.DataType.STRING);
AttributeType middlename = tx.putAttributeType("middlename", AttributeType.DataType.STRING);
AttributeType picture = tx.putAttributeType("picture", AttributeType.DataType.STRING);
AttributeType age = tx.putAttributeType("age", AttributeType.DataType.LONG);
AttributeType birthDate = tx.putAttributeType("birth-date", AttributeType.DataType.DATE);
AttributeType deathDate = tx.putAttributeType("death-date", AttributeType.DataType.DATE);
AttributeType gender = tx.putAttributeType("gender", AttributeType.DataType.STRING);
```

Now the role and relationship types. In Graql:

```graql
define

marriage sub relationship
  relates spouse1
  relates spouse2
  has picture;

parentship sub relationship
  relates parent
  relates child;
```

Using the Core API:

```lang-java-test-ignore
Role spouse1 = tx.putRole("spouse1");
Role spouse2 = tx.putRole("spouse2");
RelationshipType marriage = tx.putRelationshipType("marriage")
                            .relates(spouse1)
                            .relates(spouse2);
marriage.has(picture);

Role parent = tx.putRole("parent");
Role child = tx.putRole("child");
RelationshipType parentship = tx.putRelationshipType("parentship")
                            .relates(parent)
                            .relates(child);
```

Now the entity types. First, in Graql:

```graql
define

person sub entity
  has identifier
  has firstname
  has surname
  has middlename
  has picture
  has age
  has birth-date
  has death-date
  has gender
  plays parent
  plays child
  plays spouse1
  plays spouse2;
```

Using the Core API:

```lang-java-test-ignore
EntityType person = tx.putEntityType("person")
                        .plays(parent)
                        .plays(child)
                        .plays(spouse1)
                        .plays(spouse2);

person.has(identifier);
person.has(firstname);
person.has(surname);
person.has(middlename);
person.has(picture);
person.has(age);
person.has(birthDate);
person.has(deathDate);
person.has(gender);
```

Now to commit the schema using the Core API:

```lang-java-test-ignore
tx.commit();
```

If you do not wish to commit the schema you can revert your changes with:

```lang-java-test-ignore
tx.abort();
```

{% include note.html content="When using the in-memory knowledge graph, mutations to the knowledge graph are performed directly." %}


## Loading Data

Now that we have created the schema, we can load in some data using the Core API. We can compare how a Graql statement maps to the Core API. First, the Graql:

```graql
insert $x isa person has firstname "John";
```

Now the equivalent Core API:    

```lang-java-test-ignore
Grakn grakn = new Grakn(new SimpleURI("localhost:48555"));
Grakn.Session session = grakn.session(Keyspace.of("grakn"));
Grakn.Transaction tx = session.transaction(GraknTxType.WRITE);

Attribute johnName = firstname.create("John"); //Create the attribute
person.create().has(johnName); //Link it to an entity
```   

What if we want to create a relationship between some entities?

In Graql we know we can do the following:

```graql
insert
    $x isa person has firstname "John";
    $y isa person has firstname "Mary";
    $z (spouse1: $x, spouse2: $y) isa marriage;
```

With the Core API this would be:

```lang-java-test-ignore
//Create the attributes
johnName = firstname.create("John");
Attribute maryName = firstname.create("Mary");

//Create the entities
Entity john = person.create();
Entity mary = person.create();

//Create the actual relationships
Relationship theMarriage = marriage.create().assign(spouse1, john).assign(spouse2, mary);
```

Add a picture, first using Graql:

```graql
match
    $x isa person has firstname "John";
    $y isa person has firstname "Mary";
    $z (spouse1: $x, spouse2: $y) isa marriage;
insert
    $z has picture "www.LocationOfMyPicture.com";
```

Now the equivalent using the Core API:

```lang-java-test-ignore
Attribute weddingPicture = picture.create("www.LocationOfMyPicture.com");
theMarriage.has(weddingPicture);
```


## Building A Hierarchical Schema  

In the [Hierarchical Schema documentation](../building-schema/hierarchical-schema), we discussed how it is possible to create more expressive ontologies by creating a type hierarchy.

How can we create a hierarchy using the Core API? Well, this graql statement:

```graql
define
    event sub entity;
    wedding sub event;
```

becomes the following with the Core API:

```lang-java-test-ignore
EntityType event = tx.putEntityType("event");
EntityType wedding = tx.putEntityType("wedding").sup(event);
```

From there, all operations remain the same.

It is worth remembering that adding a type hierarchy allows you to create a more expressive database but you will need to follow more validation rules. Please check out the section on [validation](../knowledge-model/model#data-validation) for more details.

## Rule Core API

Rules can be added to the knowledge graph both through the Core API as well as through Graql. We will consider an example:

```graql
define

R1
when {
    (parent: $p, child: $c) isa Parent;
},
then {
    (ancestor: $p, descendant: $c) isa Ancestor;
};

R2
when {
    (parent: $p, child: $c) isa Parent;
    (ancestor: $c, descendant: $d) isa Ancestor;
},
then {
    (ancestor: $p, descendant: $d) isa Ancestor;
};
```

As there is more than one way to define Graql patterns through the API, there are several ways to construct rules. One options is through the Pattern factory:

```lang-java-test-ignore
Pattern rule1when = var().rel("parent", "p").rel("child", "c").isa("Parent");
Pattern rule1then = var().rel("ancestor", "p").rel("descendant", "c").isa("Ancestor");

Pattern rule2when = and(
        var().rel("parent", "p").rel("child", "c").isa("Parent')"),
        var().rel("ancestor", "c").rel("descendant", "d").isa("Ancestor")
);
Pattern rule2then = var().rel("ancestor", "p").rel("descendant", "d").isa("Ancestor");
```

If we have a specific `Grakn.Transaction tx` already defined, we can use the Graql pattern parser:

```lang-java-test-ignore
rule1when = and(tx.graql().parser().parsePatterns("(parent: $p, child: $c) isa Parent;"));
rule1then = and(tx.graql().parser().parsePatterns("(ancestor: $p, descendant: $c) isa Ancestor;"));

rule2when = and(tx.graql().parser().parsePatterns("(parent: $p, child: $c) isa Parent;(ancestor: $c, descendant: $d) isa Ancestor;"));
rule2then = and(tx.graql().parser().parsePatterns("(ancestor: $p, descendant: $d) isa Ancestor;"));
```

We conclude the rule creation with defining the rules from their constituent patterns:

```lang-java-test-ignore
Rule rule1 = tx.putRule("R1", rule1when, rule1then);
Rule rule2 = tx.putRule("R2", rule2when, rule2then);
```


As well as the Graql shell, users can also construct and execute Graql queries programmatically in Java. The Java Graql API expresses the concepts and functionality of the Graql language in the syntax of Java. It is useful if you want to make queries using Java, without having to construct a string containing the appropriate Graql expression.

To use the API, add the following to your imports:

```lang-java-test-ignore
import ai.grakn.graql.QueryBuilder;
import static ai.grakn.graql.Graql.*;
```

## QueryBuilder

A `QueryBuilder` is constructed from a `Grakn.Transaction`:

```lang-java-test-ignore
Grakn grakn = new Grakn(new SimpleURI("localhost:48555"));
Grakn.Session session = grakn.session(Keyspace.of("grakn"));
Grakn.Transaction tx = session.transaction(GraknTxType.WRITE)

QueryBuilder qb = tx.graql();
```

The user can also choose to not provide a knowledge graph with `Graql.withoutTx()`.
This can be useful if you need to provide the knowledge graph later (using `withTx`),
or you only want to construct queries without executing them.

The `QueryBuilder` class provides methods for building `match`es and `insert`
queries. Additionally, it is possible to build `aggregate`, `match..insert` and `delete` queries from `match`
queries.

## Match

Matches are constructed using the `match` method. This will produce a `Match` instance, which includes additional
methods that apply modifiers such as `limit` and `distinct`:

```lang-java
Match match = qb.match(var("x").isa("person").has("firstname", "Bob")).limit(50);
```

If you're only interested in one variable name, it also includes a `get` method
for requesting a single variable:

```
match.get("x").forEach(x -> System.out.println(x.asResource().getValue()));
```

## Get Queries

Get queries are constructed using the `get` method on a `match`.

```lang-java
GetQuery query = qb.match(var("x").isa("person").has("firstname", "Bob")).limit(50).get();
```

`GetQuery` is `Iterable` and has a `stream` method. Each result is a `Map<Var, Concept>`, where the keys are the
variables in the query.

A `GetQuery` will only execute when it is iterated over.

```lang-java
for (Map<String, Concept> result : query) {
  System.out.println(result.get("x").getId());
}
```

## Aggregate Queries

```lang-java
if (qb.match(var().isa("person").has("firstname", "Bob")).stream().findAny().isPresent()) {
  System.out.println("There is someone called Bob!");
}
```

## Insert Queries

```lang-java
InsertQuery addAlice = qb.insert(var().isa("person").has("firstname", "Alice"));

addAlice.execute();

// Marry Alice to everyone!
qb.match(
  var("someone").isa("person"),
  var("alice").has("firstname", "Alice")
).insert(
  var().isa("marriage")
    .rel("spouse", "someone")
    .rel("spouse", "alice")
).execute();
```

## Delete Queries

```lang-java
qb.match(var("x").has("firstname", "Alice")).delete("x").execute();
```

## Query Parser

The `QueryBuilder` also allows the user to parse Graql query strings into Java Graql
objects:

```lang-java
for (ConceptMap a : qb.<GetQuery>parse("match $x isa person; get;").execute()) {
    System.out.println(a);
}

qb.parse("insert isa person, has firstname 'Alice';").execute();

qb.parse("match $x isa person; delete $x;").execute();
```

{% include warning.html content="Please note that this page is in progress and subject to revision." %}

In this section we focus on using the Java API in a multi-threaded environment, and show how to create multiple transactions, which can affect the knowledge graph concurrently.

## Creating Concurrent Transactions

Transactions in GRAKN.AI are thread bound, which means that for a specific keyspace and thread, only one transaction can be open at any time.
The following would result in an exception because the first transaction `tx1` was never closed:

<!-- Ignored because this is designed to crash! -->
```lang-java-test-ignore
Grakn grakn = new Grakn(new SimpleURI("localhost:48555"));
Grakn.Session session = grakn.session(Keyspace.of("grakn"));
Grakn.Transaction tx1 = session.transaction(GraknTxType.WRITE)
Grakn.Transaction tx2 = session.transaction(GraknTxType.WRITE)
```

If you require multiple transactions open at the same time then you must do this on different threads. This is best illustrated with an example. Let's say that you wish to create 100 entities of a specific type concurrently.  The following will achieve that:

<!-- Ignored because it contains a Java lambda, which Groovy doesn't support -->
```lang-java-test-ignore
Grakn grakn = new Grakn(new SimpleURI("localhost:48555"));
Grakn.Session session = grakn.session(Keyspace.of("grakn"));
Set<Future> futures = new HashSet<>();
ExecutorService pool = Executors.newFixedThreadPool(10);

//Create sample schema
Grakn.Transaction tx = session.transaction(GraknTxType.WRITE);
EntityType entityType = tx.putEntityType("Some Entity Type");
tx.commit();

//Load the data concurrently
for(int i = 0; i < 100; i ++){
    futures.add(pool.submit(() -> {
        Grakn.Transaction innerTx = session.transaction(GraknTxType.WRITE);
        entityType.addEntity();
        innerTx.commit();
    }));
}

for(Future f: futures){
    f.get();
}
```

As you can see each thread opened its own transaction to work with. We were able to safely pass `entityType` into different threads but this was only possible because:

* We committed `entityType` before passing it around
* We opened the transaction in each thread before trying to access `entityType`.

## Issues With Concurrent Mutations

### Locking Exceptions

When mutating the knowledge graph concurrently and attempting to load the same data simultaneously, it is possible to encounter a `GraknLockingException`.  When this exception is thrown on `commit()` it means that two or more transactions are attempting to mutate the same thing. If this occurs it is recommended that you retry the transaction.

### Validation Exceptions

Validation exceptions may also occur when mutating the knowledge graph concurrently. For example, two transactions may be trying to create the exact same relationship and one of them may fail. When this occurs it is recommended retrying the transaction. If the same exception occurs again then it is likely that the transaction contains a validation error that would have still occurred even in a single threaded environment.
