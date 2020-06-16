---
pageTitle: Quickstart
keywords: getting started, grakn, graql, tutorial, quickstart, overview
longTailKeywords: get started with grakn, grakn tutorial, grakn quickstart, learn grakn
summary: Learn about the constructs of the Grakn Schema, visualise a knowledge graph, perform read and write queries and explore the power of automated reasoning and analytics with Grakn.
toc: false
---

### An Overview
In this tutorial, we go through creating and interacting with a Grakn knowledge graph representing a social network. In the process, we learn about the constructs of the Grakn Schema, visualise the knowledge graph, perform read and write queries and explore the power of automated reasoning and analytics with Grakn.

Let's get started!

### Run Grakn
[Install Grakn](../02-running-grakn/01-install-and-run.md#system-requirements) and start the [Grakn Server](../02-running-grakn/01-install-and-run.md#start-the-grakn-server).


### The Schema
A [Grakn schema](../09-schema/00-overview.md) is the blueprint of a Grakn knowledge graph. The code presented below is only a part of the schema for the social network knowledge graph that represents the concepts of `friendship`.

```graql
define

title sub attribute,
  value string;

event-date sub attribute,
  abstract,
  value datetime;
approved-date sub event-date;

## an abstract relation, only to be subtyped by other relations
request sub relation,
  abstract,
  has approved-date,
  relates approved-subject,
  relates requester,
  relates respondent;

friendship sub relation,
    relates friend,
    plays approved-friendship,
    plays listed-friendship;

## an example of subtyping in Grakn
friend-request sub request,
    relates approved-friendship as approved-subject,
    relates friendship-requester as requester,
    relates friendship-respondent as respondent;

friends-list sub relation,
    has title,
    relates list-owner,
    relates listed-friendship;

person sub entity,
    plays friend,
    plays friendship-requester,
    plays friendship-respondent,
    plays list-owner;
```

The code you see above is Graql. Graql is the language for the Grakn knowledge graph. Whether it's through the [Grakn Console](../02-running-grakn/02-console.md), [Workbase](../07-workbase/00-overview.md) or one of the [Grakn Clients](../03-client-api/00-overview.md), Grakn accepts instructions and provides answers only in its own language - Graql.

### Download and Load the Complete Schema
First, download the [`social-network/schema.gql`](../files/social-network/schema.gql){:target="_blank"} which contains the complete schema for the social network knowledge graph. Now, we need to load this schema into a [keyspace](../06-management/01-keyspace.md). To do this, we use the non-interactive mode of the [Grakn Console](../02-running-grakn/02-console.md).

<div class="note">
[Note]
Feel free to study the content of `social-network-schema.gql`. The definitions have been divided into multiple sections for better understandability, with each section containing the (commented-out) query for visualisation of the corresponding section in [Grakn Workbase](../07-workbase/00-overview.md).
</div>

While in the unzipped directory of the Grakn distribution, via terminal, run:

```
./grakn console --keyspace social_network --file path-to-the-social-network/schema.gql
```

### Load the Dataset
Download the [`social-network/data.gql`](../files/social-network/data.gql){:target="_blank"} and load it into the same keyspace. Run:

```
./grakn console --keyspace social_network --file path-to-the-social-network/data.gql
```

As you may have guessed it, `social-network-data.gql` contains a series of [Graql insert queries](../11-query/03-insert-query.md) that creates data instances in the social network knowledge graph. In a real-world application, it's more likely that we have the data in some data formats such as CSV, JSON or XML. In such a case, we need to use one of the [Grakn Clients](../03-client-api/00-overview.md) to [migrate](../08-examples/00-phone-calls-overview.md#whats-covered) the dataset into the target keyspace.

### Query the Knowledge Graph
Now that we have some data in our social network knowledge graph, we can go ahead and retrieve some information from it. To do this, we can use the [Grakn Console](../02-running-grakn/02-console.md), [Grakn Workbase](../07-workbase/00-overview.md) or one of the [Grakn Clients](../03-client-api/00-overview.md).

Let's see an example of running [Graql get queries](../11-query/02-get-query.md) via each of these interfaces.

#### Retrieve the full name of everyone who has travelled to a location using [Grakn Console](../02-running-grakn/02-console.md)

Enter the `social_network` keyspace using the Console.
```
$ ./grakn console -k social_network
```

Write the query to retrieve the desired result.
```graql
match $tra (traveler: $per) isa travel; (located-travel: $tra, travel-location: $loc) isa location-of-travel; $loc has name "French Lick"; $per has full-name $fn; get $fn;
```

The result contains the following answers.
<!-- test-ignore -->
```graql
{$fn "Solomon Tran" isa full-name;}
{$fn "Julie Hutchinson" isa full-name;}
{$fn "Miriam Morton" isa full-name;}
```

#### Visualise all friendships using [Workbase](../07-workbase/00-overview.md)

![Visualise all married people](../images/quickstart/workbase_sample_query.png)

#### Retrieve all employments using [Client Java](../03-client-api/01-java.md)

<!-- test-example SocialNetworkQuickstartQuery.java -->
```java
package grakn.examples;

import grakn.client.GraknClient;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlGet;
import grakn.client.answer.ConceptMap;

import java.util.List;

public class SocialNetworkQuickstartQuery extends Throwable {
    public static void main(String[] args) {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");
        GraknClient.Transaction transaction = session.transaction().write();

        GraqlGet query = match(
                var().rel("employer", var("org")).rel("employee", var("per")).isa("employment"),
                var("per").has("full-name", var("per-fn")),
                var("org").has("name", var("org-n"))
        ).get();

        List<ConceptMap> answers = transaction.execute(query).get();

        for (ConceptMap answer : answers) {
            System.out.println(answer.get("per-fn").asAttribute().value());
            System.out.println(answer.get("org-n").asAttribute().value());
            System.out.println(" - - - - - - - - ");
        }

        transaction.close();
        session.close();
    }
}
```

#### Lazily retrieve all photos and videos that have been found funny by women using [Client Python](../03-client-api/02-python.md)

<!-- test-example social_network_quickstart_query.py -->
```python
from grakn.client import GraknClient

with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace = "social_network") as session:
      with session.transaction().read() as transaction:
        query = '''
          match
            $pos isa media;
            $fun isa emotion;
            $fun "funny";
            $per has gender "female";
            (reacted-emotion: $fun, reacted-to: $pos, reacted-by: $per) isa reaction;
          get $pos;
        '''
        answer_iterator = transaction.query(query).get()
        for answer in answer_iterator:
          print(answer.map().get("pos").id)
```

#### Retrieve the average salary of all employees at Pharos using [Client Node.js](../03-client-api/03-nodejs.md)

<!-- test-example socialNetworkQuickstartQuery.js -->
```javascript
const GraknClient = require("grakn-client");

async function getAverageSalaryAt (orgName) {
    const client = new GraknClient("localhost:48555");
	const session = await client.session("social_network");
	const transaction = await session.transaction().read()
	const query = `
		match
			$org isa organisation, has name "${orgName}";
			($org, $per) isa employment, has salary $sal;
		get $sal; mean $sal;
	`
	const answerIterator = await transaction.query(query);
	const answer = await answerIterator.next();
	if (answer) {
		console.log(await answer.number());
	} else {
	  console.log(`No one works at ${orgName}`);
	}
	await transaction.close();
	await session.close();
	client.close();
}

getAverageSalaryAt("Pharos"); // asynchronous call
```

### Insert and Delete Data
We can create and delete instances of data in a Grakn knowledge graph by running [insert](../11-query/03-insert-query.md) and [delete](../11-query/04-delete-query.md) queries. Let's give them a try using the Console.

#### Insert an instance of type person
<!-- ignore-test -->
```graql
insert $per isa person, has full-name "Johny Jimbly Joe", has gender "male", has email "johnyjj@gmail.com";
```

<!-- test-ignore -->
```graql
commit
```

<div class="note">
[Important]
Any manipulation made in the schema or the data instances, is not persisted to the original keyspace until we run the `commit` command.
</div>

#### Associate the newly added person with a nickname

```graql
match $per isa person, has email "johnyjj@gmail.com"; insert $per has nickname "JJJ";
```
<!-- test-ignore -->
```graql
commit
```

#### Delete the newly added person
<!-- ignore-test -->
```graql
match $per isa person, has full-name "Johny Jimbly Joe"; delete $per;
```

<!-- test-ignore -->
```graql
commit
```

### Store Knowledge
Grakn is capable of reasoning over data to infer new knowledge, commonly known as automated reasoning or inference. Inference in a Grakn knowledge graph is made via pre-defined [Rules](../09-schema/03-rules.md).

Let's look at some simple examples of how Grakn uses rules for reasoning over explicit data.

```graql
define

course-enrollment-mutuality sub relation,
  relates coursemate,
  relates mutual-course-enrollment;

people-taken-the-same-course sub rule,
  when {
    $sce1 (student: $p1, enrolled-course: $sc) isa school-course-enrollment;
    $sce2 (student: $p2, enrolled-course: $sc) isa school-course-enrollment;
    $p1 != $p2;
  }, then {
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
define

school-mutuality sub relation,
  relates schoolmate,
  relates mutual-school;

people-gone-to-the-same-school sub rule,
  when {
    (student: $p1, enrolled-course: $c1) isa school-course-enrollment;
    (student: $p2, enrolled-course: $c2) isa school-course-enrollment;
    (offered-course: $c1, offering-school: $s) isa school-course-offering;
    (offered-course: $c2, offering-school: $s) isa school-course-offering;
    $p1 != $p2;
  }, then {
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

The [Graql compute queries](../11-query/07-compute-query.md) are designed to traverse the knowledge graph in parallel over a large dataset, distributed across multiple machines. We can use the compute queries to retrieve statistical information, find the shortest path between any two nodes, identify significant nodes based on their centrality and identify clusters within the knowledge graph.

Let's look at a few examples of running `compute` on the `genealogy` knowledge graph.

#### Retrieve the mean of an attribute owned by a given type

```graql
compute mean of salary, in employment;
```

#### Retrieve the total number of instances of a given type

```graql
compute count in travel;
```

#### Find the [shortest path](../11-query/07-compute-query.md#compute-the-shortest-path) between two instances

```graql
match $x has full-name "Dominic Lyons"; $y has full-name "Haider Johnson"; get;
```

<!-- test-ignore -->
```graql
{$x id V446496 isa person; $y id V229424 isa person;}
```

<!-- test-ignore -->
```graql
compute path from V446496, to V229424;
```

<!-- test-ignore -->
```graql
{V184392, V442424, V90344}
```

#### [Identify clusters](../11-query/07-compute-query.md#identify-clusters) in a subgraph
```graql
compute cluster in [person, employment, organisation], using connected-component;
```

<!-- test-ignore -->
```graql
{V192656}
{V663728, V266336, V262392, V680112, V479408}
{V180272, V446496, V278672, V463024, V671920}
{V172176}
{V360448, V250104, V176176, V667824, V180368, V303200, V639152}
{V647200, V295008, V237808, V225328, V364544, V372832, V356352, V167984, V266488, V299104, V663584}
{V401584, V229424, V639008, V213040, V655392}
```

### Where Next?

- [Grakn Schema](../09-schema/00-overview.md)
- [Graql Queries](../11-query/00-overview.md)
- [Workbase](../07-workbase/00-overview.md)
- [Examples](../08-examples/00-phone-calls-overview.md)
