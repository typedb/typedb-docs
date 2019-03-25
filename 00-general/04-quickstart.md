---
sidebarTitle: Quickstart
pageTitle: Quickstart
permalink: /docs/general/quickstart
---

### An Overview
In this tutorial, we go through creating and interacting with a Grakn knowledge graph representing a social network. In the process, we learn about the constructs of the Grakn Schema, visualise the knowledge graph, perform read and write queries and explore the power of automated reasoning and analytics with Grakn.

Let's get started!

### Run Grakn
[Install Grakn](/docs/running-grakn/install-and-run#system-requirements) and start the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server).


### The Schema
A [Grakn schema](/docs/schema/overview) is the blueprint of a Grakn knowledge graph. The code presented below is only a part of the schema for the social network knowledge graph that represents the concepts of `friendship`.

```graql
define

title sub attribute,
  datatype string;

event-date sub attribute,
  is-abstract,
  datatype date;
approved-date sub event-date;

## an abstract relationship, only to be subtyped by other relationships
request sub relationship,
  is-abstract,
  has approved-date,
  relates approved-subject,
  relates requester,
  relates respondent;

friendship sub relationship,
    relates friend,
    plays approved-friendship,
    plays listed-friendship;

## an example of subtyping in Grakn
friend-request sub request,
    relates approved-friendship as approved-subject,
    relates friendship-requester as requester,
    relates friendship-respondent as respondent;

friends-list sub relationship,
    has title,
    relates list-owner,
    relates listed-friendship;

person sub entity,
    plays friend,
    plays friendship-requester,
    plays friendship-respondent,
    plays list-owner;
```

The code you see above is Graql. Graql is the language for the Grakn knowledge graph. Whether it's through the [Graql Console](/docs/running-grakn/console) or one of the [Grakn Clients](/docs/client-api/overview), Grakn accepts instructions and provides answers only in its own language - Graql.

### Download and Load the Complete Schema
First, download the [`social-network-schema.gql`](/docs/files/social-network-schema.gql){:target="_blank"} which contains the complete schema for the social network knowledge graph. Now, we are going to load this schema into a [keyspace](/docs/management/keyspace). To do this, we need to use the non-interactive mode of the [Graql Console](/docs/running-grakn/console).

<div class="note">
[Note]
Feel free to study the content of `social-network-schema.gql`. The definitions have been divided into multiple sections for better understandability, with each section containing the (commented-out) query for visualisation of the corresponding section in [Grakn Workbase](/docs/workbase/overview).
</div>

While in the unzipped directory of the Grakn distribution, via terminal, run:

```
./graql console --keyspace social_network --file path-to-the/social-network-schema.gql
```

### Load the Dataset
Download the [`social-network-data.gql`](/docs/files/social-network-data.gql){:target="_blank"} and load it into the same keyspace. Run:

```
./graql console --keyspace social_network --file path-to-the-data.gql
```

As you may have guessed it, `social-network-data.gql` contains a series of [Graql insert queries](/docs/query/insert-query) that creates data instances in the social network knowledge graph. In a real-world application, it's more likely that we have the data in some formats such as CSV, JSON or XML. In such a case, we need to use one of the [Grakn Clients](/docs/client-api/overview) to [migrate](/docs/examples/phone-calls-overview#whats-covered) the dataset into the target Grakn knowledge graph.

### Query the Knowledge Graph
Now that we have some data in our social network knowledge graph, we can go ahead and retrieve some information from it. To do this, we can use the [Graql Console](/docs/running-grakn/console), [Grakn Workbase](/docs/workbase/overview) or one of the [Grakn Clients](/docs/client-api/overview).

Let's see an example of running [Graql get queries](/docs/query/get-query) via each of these interfaces.

#### Retrieve the full name of everyone who has travelled to a location using [Graql Console](/docs/running-grakn/console)
<!-- ignore-test -->
```graql
$ ./graql console -k social_network
>>> match $tra (traveler: $per) isa travel; (located-travel: $tra, travel-location: $loc) isa location-of-travel; $loc has name "French Lick"; $per has full-name $fn; get $fn;

{$fn "Solomon Tran" isa full-name;}
{$fn "Julie Hutchinson" isa full-name;}
{$fn "Miriam Morton" isa full-name;}
```

#### Visualise all friendships using [Workbase](/docs/workbase/overview)

![Visualise all married people](/docs/images/quickstart/workbase_sample_query.png)

#### Retrieve all employments using [Client Java](/docs/client-api/java)

<!-- ignore-test -->
```java
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
    Keyspace keyspace = Keyspace.of("social_network");
    Grakn grakn = new Grakn(localGrakn);
    Grakn.Session session = grakn.session(keyspace);
    Grakn.Transaction transaction = session.transaction(GraknTxType.READ);

    GetQuery query = Graql.match(
      var().rel("employer", var("org")).rel("employee", var("per")).isa("employment"),
      var("per").has("full-name", var("per-fn")),
      var("org").has("name", var("org-n"))
    ).get();

    List <ConceptMap> answers = query.withTx(transaction).execute();

    for (ConceptMap answer: answers) {
      System.out.println(answer.get("per-fn").asAttribute().value());
      System.out.println(answer.get("org-n").asAttribute().value());
      System.out.println(" - - - - - - - - ");
    }

    transaction.close();
    session.close();
  }
}
```

#### Lazily retrieve all photos and videos that have been found funny by women using [Client Python](/docs/client-api/python)

<!-- ignore-test -->
```python
import grakn

client = grakn.Grakn(uri = "localhost:48555")
with client.session(keyspace = "social_network") as session:
  with session.transaction(grakn.TxType.READ) as transaction:
    query = '''
      match
        $pos isa media;
        $fun isa emotion;
        $fun == "funny";
        $per has gender "female";
        (reacted-emotion: $fun, reacted-to: $pos, reacted-by: $per) isa reaction;
      get $pos;
    '''
    answer_iterator = transaction.query(query)
    for answer in answer_iterator:
      print(answer.map().get("pos").id)
```

#### Retrieve the average salary of all employees at Pharos using [Client Node.js](/docs/client-api/nodejs)

<!-- ignore-test -->
```javascript
const Grakn = require("grakn");
const grakn = new Grakn("localhost:48555");

async function getAverageSalaryAt(orgName) {
  const session = await grakn.session((keyspace = "social_network"));
  const transaction = await session.transaction(Grakn.txType.READ);
  const query = `
    match
      $org isa organisation, has name "${orgName}";
      ($org, $per) isa employment, has salary $sal;
      get $sal; mean $sal;
  `
  const answerIterator = await transaction.query(query);
  const answer = await answerIterator.next();
  console.log(await answer.number());
  transaction.close();
  session.close();
}

getAverageSalaryAt("Pharos");
```

### Insert and Delete Data
We can create and delete instances of data in a Grakn knowledge graph by running [insert](/docs/query/insert-query) and [delete](/docs/query/delete-query) queries. Let's give them a try using the console.

#### Insert an instance of type person
<!-- ignore-test -->
```graql
>>> insert $per isa person, has full-name "Johny Jimbly Joe", has gender "male", has email "johnyjj@gmail.com";
{$per id V139280 isa person;}
>>> commit
```

<div class="note">
[Important]
Any manipulation made in the schema or the data instances, is not persisted to the original keyspace until we run the `commit` command.
</div>

#### Associate the newly added person with a nickname
<!-- ignore-test -->
```graql
>>> match $per id V139280; insert $per has nickname "JJJ";
{$per id V139280 isa person;}
>>> commit
```

#### Delete the newly added person
<!-- ignore-test -->
```graql
>>> match $per isa person, has full-name "Johny Jimbly Joe"; delete $per;
{V139280}
>>> commit
```

### Store Knowledge
Grakn is capable of reasoning over data to infer new knowledge, commonly known as automated reasoning or inference. Inference in a Grakn knowledge graph is made via pre-defined [Rules](/docs/schema/rules).

Let's look at some simple examples of how Grakn uses rules for reasoning over explicit data.

```graql
course-enrollment-mutuality sub relationship,
  relates coursemate,
  relates mutual-course-enrollment;

people-taken-the-same-course sub rule,
  when {
    $sce1 (student: $p1, enrolled-course: $sc) isa school-course-enrollment;
    $sce2 (student: $p2, enrolled-course: $sc) isa school-course-enrollment;
    $p1 != $p2;
  } then {
    (coursemate: $p1, coursemate: $p2, mutual-course-enrollment: $sce1, mutual-course-enrollment: $sce2) isa course-enrollment-mutuality;
  };
```

As you can see in the `social_network_data.gql` file, no instance of `course-enrollment-mutuality` was ever inserted. It's only the rule above that allows Grakn to infer this knowledge and know the answer to the following question at query time.

```graql
match
  $per isa person, has full-name "Miriam Morton";
  ($per, coursemate: $mate) isa course-enrollment-mutuality;
  $mate has full-name $mate-fn;
get $mate-fn;
```

Given the second rule:

```graql
school-mutuality sub relationship,
  relates schoolmate,
  relates mutual-school;

people-gone-to-the-same-school sub rule,
  when {
    (student: $p1, enrolled-course: $c1) isa school-course-enrollment;
    (student: $p2, enrolled-course: $c2) isa school-course-enrollment;
    (offered-course: $c1, offerring-school: $s) isa school-course-offerring;
    (offered-course: $c2, offerring-school: $s) isa school-course-offerring;
    $p1 != $p2;
  } then {
    (schoolmate: $p1, schoolmate: $p2, mutual-school: $s) isa school-mutuality;
  };
```

We can query for people who have attended the same school and taken the same course, like so:

```graql
match
  (coursemate: $mate-1, coursemate: $mate-2) isa course-enrollment-mutuality;
  (schoolmate: $mate-1, schoolmate: $mate-2) isa school-mutuality;
  $mate-1 has full-name $mate-1-fn;
  $mate-2 has full-name $mate-2-fn;
get $mate-1-fn, $mate-2-fn;
```

Similar to the first rule, the answer we're asking for here, was never injected into the knowledge graph and is being inferred at query time by Grakn.

### Distributed Analytics With Grakn

The [Graql compute queries](/docs/query/compute-query) are designed to traverse the knowledge graph in parallel over a large dataset, distributed across multiple machines. We can use the compute queries to retrieve statistical information, find the shortest path between any two nodes, identify significant nodes based on their centrality and identify clusters within the knowledge graph.

Let's look at a few examples of running `compute` on the `genealogy` knowledge graph.

#### Retrieve the mean of an attribute owned by a given type
<!-- ignore-test -->
```graql
>>> compute mean of salary, in employment;
4460.714285714285
```

#### Retrieve the total number of instances of a given type
<!-- ignore-test -->
```graql
>>> compute count in travel;
9
```

#### Find the [shortest path](/docs/query/compute-query#compute-the-shortest-path) between two instances
<!-- ignore-test -->
```graql
>>> match $x has full-name "Dominic Lyons"; $y has full-name "Haider Johnson"; get;
{$x id V446496 isa person; $y id V229424 isa person;}
>>> compute path from V446496, to V229424;
{V184392, V442424, V90344}
```

#### [Identify clusters](/docs/query/compute-query#identify-clusters) in a subgraph
<!-- ignore-test -->
```graql
>>> compute cluster in [person, employment, organisation], using connected-component;
{V192656}
{V663728, V266336, V262392, V680112, V479408}
{V180272, V446496, V278672, V463024, V671920}
{V172176}
{V360448, V250104, V176176, V667824, V180368, V303200, V639152}
{V647200, V295008, V237808, V225328, V364544, V372832, V356352, V167984, V266488, V299104, V663584}
{V401584, V229424, V639008, V213040, V655392}
```

### Where Next?

- [Grakn Schema](/docs/schema/overview)
- [Graql Queries](/docs/query/overview)
- [Workbase](/docs/workbase/overview)
- [Examples](/docs/examples/phone-calls-overview)