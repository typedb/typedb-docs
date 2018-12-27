---
sidebarTitle: Quickstart
pageTitle: Quickstart

permalink: /docs/general/quickstart
---

### An Overview
In this tutorial, we go through creating and interacting with a Grakn knowledge graph containing a simple genealogy dataset. In the process, we learn about the constructs of Grakn Schema, extend and visualise the knowledge graph, perform read and write queries and explore the power of automated reasoning and analytics with Grakn.

Let's get started!

### Run Grakn
[Install Grakn](/docs/running-grakn/install-n-run#system-requirements) and start the [Grakn Server](/docs/running-grakn/install-n-run#start-the-grakn-server).


### The Schema
A [Grakn schema](/docs/schema/overview) is the blueprint of a Grakn knowledge graph. Let's take a look at what the initial schema for our genealogy example looks like.

```lang-graql
define

marriage sub relationship
  has picture,
  relates spouse;

parentship sub relationship
  relates parent
  relates child;

person sub entity,
  has first-name,
  has middle-name,
  has surname,
  has picture,
  has age,
  has birth-date,
  has death-date,
  has gender,
  plays parent,
  plays child,
  plays spouse;

name sub attribute datatype string;
first-name sub name datatype string;
middle-name sub name datatype string;
surname sub name datatype string;
picture sub attribute datatype string;
age sub attribute datatype long;
event-date sub attribute datatype date;
birth-date sub event-date datatype date;
death-date sub event-date datatype date;
gender sub attribute datatype string;
```

The code you see above is Graql. Graql is the language for the Grakn knowledge graph. Whether it's through the [Graql Console](/docs/running-grakn/console) or one of the [Grakn Clients](/docs/client-api/overview), Grakn accepts instructions and provides answers only in its own language - Graql.

Save the code above in a file named `schema.gql`.

### Load the Schema
To create the genealogy knowledge graph, we need to load this schema into a [keyspace](/docs/management/keyspace). To do this, we need to use the non-interactive mode of the [Graql Console](/docs/running-grakn/console).

While in the unzipped directory of the Grakn distribution, via terminal, run:

```
./graql console --keyspace genealogy --file path-to-the-schema.gql
```

### Load the Dataset
Download the [`genealogy-data.gql`](/docs/files/genealogy-data.gql){:target="_blank"} and load into the same keyspace. Run:

```
./graql console --keyspace genealogy --file path-to-the-data.gql
```

As you may have guessed it, `data.gql` contains a series of [Graql insert queries](/docs/query/insert-query) that creates data instances in the genealogy knowledge graph. In a real-world application, it's more likely that we have the data in some formats such as CSV, JSON or XML. In such a case, we need to use one of the [Grakn Clients](/docs/client-api/overview) to [migrate](/docs/examples/phone-calls-overview#whats-covered) the dataset into the target Grakn knowledge graph.

### Query the Knowledge Graph
Now that we have some data in our genealogy knowledge graph, we can go ahead and retrieve some information from it. To do this we can use the [Graql Console](/docs/management/console), [Grakn Workbase](/docs/workbase/overview) or one of the [Grakn Clients](/docs/client-api/overview).

Let's see an example of running [Graql get queries](/docs/query/get-query) via each of these interfaces.

#### Retrieve the full name of each person using [Graql Console](/docs/running-grakn/console)

```lang-graql
$ ./graql console -k genealogy
>>> match $p isa person has first-name $fn, has surname $sn; get;

{$sn val "Herchelroth" isa surname; $fn val "Barbara" isa first-name; $p id V37080 isa person;}
{$fn val "Isabelle" isa first-name; $p id V53320 isa person; $sn val "McGaughey" isa surname;}
{$sn val "Newman" isa surname; $p id V32984 isa person; $fn val "Hermione" isa first-name;}
## 54 more answers
```

#### Visualise all married people in the "Niesz" family using [Workbase](/docs/workbase/overview)

![Visualise all married people](/docs/images/quickstart/workbase_sample_query.png)

#### Retrieve all parents and children using [Client Java](/docs/client-api/java)

```lang-java
package ai.grakn.examples;
import ai.grakn.GraknTxType;
import ai.grakn.Keyspace;
import ai.grakn.client.Grakn;
import ai.grakn.graql.GetQuery;
import ai.grakn.graql.Graql;
import ai.grakn.graql.answer.ConceptMap;
import ai.grakn.util.SimpleURI;
import java.util.List;
import static ai.grakn.graql.Graql.var;

public class Queries {
  public static void main(String[] args) {
    SimpleURI localGrakn = new SimpleURI("localhost", 48555);
    Keyspace keyspace = Keyspace.of("genealogy");
    Grakn grakn = new Grakn(localGrakn);
    Grakn.Session session = grakn.session(keyspace);
    Grakn.Transaction transaction = session.transaction(GraknTxType.READ);

    GetQuery query = Graql.match(
      var().rel("parent", var("p")).rel("child", var("c")).isa("parentship"),
      var("p").has("first-name", var("p-fn")),
      var("c").has("first-name", var("c-fn"))
    ).get();

    List < ConceptMap > answers = query.withTx(transaction).execute();

    for (ConceptMap answer: answers) {
      System.out.println(answer.get("p-fn").asAttribute().value());
      System.out.println(answer.get("c-fn").asAttribute().value());
      System.out.println(" - - - - - - - - ");
    }

    transaction.close();
    session.close();
  }
```

#### Lazily retrieve all people named _Elizabeth_ using [Client Python](/docs/client-api/python)

```lang-python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "genealogy") as session:
  with session.transaction(grakn.TxType.READ) as transaction:
    answers_iterator = transaction.query('match $p isa person has first-name "Elizabeth"; get;')
    for answer in answers_iterator:
      print(answer.map().get("p").id)
```

#### Eagerly retrieve the age of all fathers using [Client Node.js](/docs/client-api/nodejs)

```lang-javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");

async function getFathers() {
  const session = await grakn.session((keyspace = "genealogy"));
  const transaction = await session.transaction(Grakn.txType.READ);
  const answersIterator = await transaction.query('match (parent: $f) isa parentship; $f isa person has gender "male" has age $a; get $a;')
  const answers = await answersIterator.collectConcepts();
  for (answer of answers) {
    console.log(await answer.value());
  }
  transaction.close();
  session.close();
}

getFathers();
```

### Insert and Delete Data
We can add and remove instances of data in a Grakn knowledge graph by running [insert](/docs/query/insert-query) and [delete](/docs/query/delete-query) queries. Let's try one of each in our genealogy example.

#### Insert an instance of type person

```lang-graql
>>> insert $p isa person has first-name "Johny", has middle-name "Jimbly", has surname "Joe", has gender "male";
{$p id V139280 isa person;}
>>> commit
```

<div class="note">
[Important]
Any manipulation made in the schema or the data instances, is not persisted to the original keyspace until we run the `commit` command.
</div>

### Insert an age attribute to the newly added person

```lang-graql
>>> match $p id V139280; insert $p has age 77;
{$p id V139280 isa person;}
>>> commit
```

#### Retrieve the newly added person

```lang-graql
>>> match $p isa person has first-name "Johny", has surname "Joe"; get;
{$p id V139280 isa person;}
```

#### Delete thew newly added person

```lang-graql
>>> match $p isa person has first-name "Johny", has surname "Joe"; delete;
{V139280}
>>> commit
```

### Store Knowledge
Grakn is capable of reasoning over explicit data to infer new implicit relationships. This is commonly known as automated reasoning. Inference in a Grakn knowledge graph is made via [Graql Rules](/docs/schema/rules) and [Type Hierarchies](/docs/schema/overview#type-hierarchy).

Let's extend the schema for our genealogy knowledge graph to take advantage of type hierarchies and rules.

In the schema we defined and loaded into a keyspaces previously, there is no notion of `father`, `mother`, `son` and `daughter`. However, every single one of these new concept types can be inferred based on the existing explicitly stored dataset. All we need to do to make such inferences, is to look at the `gender` of each person in conjunction with the `role` they play in a `parentship` relationship.

```lang-graql
person
  plays son
  plays daughter
  plays mother
  plays father;

parentship sub relationship
  relates mother
  relates father
  relates son
  relates daughter;

mother sub parent;
father sub parent;
son sub child;
daughter sub child;

male-parent-and-male-child-implies-father-son-parentship sub rule,
  when {
    (parent: $p, child: $c) isa parentship;
    $p has gender "male";
    $c has gender "male";
  } then {
    (father: $p, son: $c) isa parentship;
  };

male-parent-and-female-child-implies-father-daughter-parentship sub rule,
  when {
    (parent: $p, child: $c) isa parentship;
    $p has gender "male";
    $c has gender "female";
  } then {
    (father: $p, daughter: $c) isa parentship;
  };

female-parent-and-male-child-implies-mother-son-parentship sub rule,
  when {
    (parent: $p, child: $c) isa parentship;
    $p has gender "female";
    $c has gender "male";
  } then {
    (mother: $p, son: $c) isa parentship;
  };

female-parent-and-female-child-implies-mother-daughter-parentship sub rule,
  when {
    (parent: $p, child: $c) isa parentship;
    $p has gender "female";
    $c has gender "female";
  } then {
    (mother: $p, daughter: $c) isa parentship;
  };
```

The code above is a _part of_ the extension we are about to make to the genealogy schema.
Download the [`genealogy-extension.gql`](/docs/files/genealogy-extension.gql){:target="_blank"} and to load it into the `genealogy` keyspace, via terminal, run:

```
$ ./graql console --keyspace genealogy --file path-to-the-genealogy-extension.gql
```

<div class="note">
[Note]
Feel free to study the content of `genealogy-extension.gql`. It includes definitions of more concept types and rules that build a complete family tree based on the existing dataset.
</div>

With the extended complete schema, we can now, for instance, ask for the fatherhood relationships, although such information was not included in the dataset we initially loaded into our knowledge graph.

```lang-graql
>>> match (father: $f, son: $s) isa parentship; $f isa person has first-name $f-fn, has surname $f-sn; $s isa person has first-name $s-fn, has surname $s-sn; limit 5; get;
```

### Distributed Analytics With Grakn

The [Graql compute queries](/docs/query/compute-query) are designed to traverse the knowledge graph in parallel over a large dataset, distributed across multiple machines. We can use the compute queries to retrieve statistical information, find the shortest path between any two nodes, identify significant nodes based on their centrality and identify clusters within the knowledge graph.

Let's look at a few examples of running `compute` on the `genealogy` knowledge graph.

#### Retrieve the mean of an attribute owned by a given type
```lang-graql
>>> compute mean of age, in person;
78.22727272727273
```

#### Retrieve the total number of instances of a given type
```lang-graql
>>> compute count in marriage;
22
```

#### Find the shortest path between two instances
```lang-graql
>>> match $x has first-name "Barbara", has surname "Shafner"; $y has first-name "Jacob", has surname "Niesz"; get;
{$y id V184392 isa person; $x id V90344 isa person;}
>>> compute path from V184392, to V90344;
{V184392, V442424, V90344}
```

#### Identify clusters in a subgraph
```lang-graql
>>> compute cluster in [person, marriage], using connected-component;
{V159816, V98432, V184320, V82152, V336040}
{V196664, V151608, V430136}
## more clusters
```

### Where Next?

- [Grakn Schema](/docs/schema/overview)
- [Graql Queries](/docs/query/overview)
- [Workbase](/docs/workbase/overview)
- [Examples](/docs/examples/phone-calls-overview)