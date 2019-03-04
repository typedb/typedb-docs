---
sidebarTitle: Schema
pageTitle: Defining a Sample Schema
permalink: /docs/examples/phone-calls-schema
---

## The Goal
In this tutorial, our aim is to write a schema and load it into our `phone_calls` knowledge graph - one that describes the reality of our dataset.

## The Dataset
First off, let’s look at the dataset we are going to be working within this series. Simply put, we’re going to have:

**people** who **call** each other. Those who make calls have a **contract** with **company** “Telecom”.

People, calls, contracts and companies. That’s what we are dealing with. But what do we want to get out of this data?

## The Insights
At the end of this series of examples, we aim to obtain the following insights from the dataset contained within this knowledge graph.

- Since September 10th, which customers called the person X?
- Who are the people who have received a call from a London customer aged over 50 who has previously called someone aged under 20?
- Who are the common contacts of customers X and Y?
- Who are the customers who 1) have all called each other and 2) have all called person X at least once?
- How does the average call duration among customers aged under 20 compare with those aged over 40?

This is all we need for determining how our schema should be defined. Let's break it down.

A **company** has a **name**, and can be the **provider** of a **contract** to a **person**, who then becomes a **customer**.

A **person** has a **first and last name**, an **age**, a **city** they live in, and a **phone number**. A person who doesn’t have a registered contract (not a customer) has only a **phone number**.

A **call**, made from a **person (caller)** to another **person (callee)**, has a **duration** as well as the **date and time** it’s been made.

## The Schema
Now that we have a good understanding of our dataset, we can go ahead and write the schema for it.

But first, let’s visualise the reality of our dataset.

![The Visualised Schema](/docs/images/examples/phone_calls_schema.png)

By looking at this visualised schema, we can identify the [Concepts](/docs/schema/concepts).

**call** is of type **relation** that has two role players:
- **person** who plays the role of a **caller**, and
- (another) **person** who plays the role of a **callee**.

**contract** is also of type **relation** that has two role players:
- **company** who plays the role of a **provider**, and
- **person** who plays the role of a **customer**.

**company** and **person** are of type **entity**.

**first-name**, **last-name**, **phone-number**, **city**, **age**, **started-at** and **duration** are of type **attribute**.

That’s all well and good, but how do we get our knowledge graph to reflect this model?

## Time to Talk Graql
Open a new file in your favourite text editor, preferably one with syntax highlighting for Graql (`.gql`) files. Here are the ones for [atom](https://atom.io/packages/language-graql), [visual studio code](https://marketplace.visualstudio.com/items?itemName=idealley.gql) and [sublime 3](https://github.com/graknlabs/graql_syntax_sublime).

You can define the elements of a Grakn schema in any order you wish. I personally prefer to start from the relations, as I see them to be the source of interactions — where knowledge is derived from.

Any **relation** relates to at least one **role** that is played by at least 2 **concepts**.

In our case, a **call** relates to **caller** played by a **person** and to **callee** played by another **person**.

Likewise for a **contract**. It relates to **provider** played by a **company** and to **customer** played by a **person**.
<!-- test-ignore -->
```graql
define

  contract sub relation,
    relates provider,
    relates customer;

  call sub relation,
    relates caller,
    relates callee;

  company sub entity,
    plays provider;

  person sub entity,
    plays customer,
    plays caller,
    plays callee;
```

To define the attributes, we use the has keyword.
<!-- test-ignore -->
```graql
define

  contract sub relation,
    relates provider,
    relates customer;

  call sub relation,
    relates provider,
    relates customer,
    has started-at,
    has duration;

  company sub entity,
    plays provider,
    has name;

  person sub entity,
    plays customer,
    plays caller,
    plays callee,
    has first-name,
    has last-name,
    has phone-number,
    has city,
    has age,
    has is-customer;
```

Lastly, we need to define the type of each attribute.
<!-- test-ignore -->
```graql
define

  contract sub relation,
    relates provider,
    relates customer;

  call sub relation,
    relates caller,
    relates callee,
    has started-at,
    has duration;

  company sub entity,
    plays provider,
    has name;

person sub entity,
    plays customer,
    plays caller,
    plays callee,
    has first-name,
    has last-name,
    has phone-number,
    has city,
    has age,
    has is-customer;

  name sub attribute,
	  datatype string;
  started-at sub attribute,
	  datatype date;
  duration sub attribute,
	  datatype long;
  first-name sub attribute,
	  datatype string;
  last-name sub attribute,
	  datatype string;
  phone-number sub attribute,
	  datatype string;
  city sub attribute,
	  datatype string;
  age sub attribute,
	  datatype long;
  is-customer sub attribute,
	  datatype boolean;
```

Note that we don't need to define an id attribute. Grakn takes care of that for us.
Save the schema.gql file. In a few minutes, we'll have it loaded into a brand new Grakn keyspace.

## Load and test the schema
In order to load this schema in a keyspace, we first need to run the Grakn server.

**1 -** [Download Grakn](/docs/running-grakn/install-and-run#download-and-install-grakn)
For the rest of these instructions, I assume that you have downloaded the Grakn zip file and navigated into the unzipped folder via terminal.

**2 -** Run the Grakn server:

```
./grakn server start
```

**3 -** Load the schema into a Grakn keyspace. Run:

```
./grakn console --keyspace phone_calls --file path/to/the/schema.gql
```

**4 -** Open the Graql console in interactive mode. Run:

```
./grakn console --keyspace phone_calls
```

**5 -** Make sure the schema is properly defined in our newly created knowledge graph. While in the Graql console, run:

```graql
match $x sub thing; get;
```

The result should be as follows:
<!-- test-ignore -->
```graql
{$x label thing;}
{$x label entity;}
{$x label relation;}
{$x label attribute;}
{$x label company sub entity;}
{$x label person sub entity;}
{$x label call sub relation;}
{$x label "@has-attribute" sub relation;}
{$x label contract sub relation;}
{$x label name sub attribute;}
{$x label started-at sub attribute;}
{$x label age sub attribute;}
{$x label city sub attribute;}
{$x label last-name sub attribute;}
{$x label first-name sub attribute;}
{$x label duration sub attribute;}
{$x label phone-number sub attribute;}
{$x label is-customer sub attribute;}
{$x label "@has-started-at" sub "@has-attribute";}
{$x label "@has-first-name" sub "@has-attribute";}
{$x label "@has-city" sub "@has-attribute";}
{$x label "@has-name" sub "@has-attribute";}
{$x label "@has-duration" sub "@has-attribute";}
{$x label "@has-age" sub "@has-attribute";}
{$x label "@has-last-name" sub "@has-attribute";}
{$x label "@has-phone-number" sub "@has-attribute";}
{$x label "@has-is-customer" sub "@has-attribute";}
```

## To Recap
We started off by describing our dataset in the most natural way possible.

Next, we went on to visualise that dataset by how we perceive it in the real world.

Then, by identifying the Grakn concepts in the visualised schema, we went ahead and wrote our schema in Graql.

Lastly, we loaded the schema into a Grakn keyspace and ran a generic match query to ensure it was indeed loaded correctly.

## Next
Now that we have a model for our knowledge graph, aka. the schema, we can go ahead and migrate some actual data into it so that we can proceed to query for those insights. Pick the client of your choice to continue with migration.

- [Java](/docs/examples/phone-calls-migration-java)
- [Node.js](/docs/examples/phone-calls-migration-nodejs)
- [Python](/docs/examples/phone-calls-migration-python)
