---
title: Concepts
keywords: schema
tags: [graql]
summary: "How a Grakn Schema is defined."
permalink: /docs/schema/concepts
---

{% include warning.html content="The content from here onwards belongs to the old and is planned to be removed in the favor of the new." %}

## Introduction

In this section we are going to run through the construction of a basic schema. We recommend that you refer to the [Knowledge Model](../knowledge-model/model) documentation before reading this page. The process we will follow is a general guideline as to how you may start designing a schema.

The schema we will be building will be used for a genealogy knowledge graph used for mapping out a family tree. You can find the complete schema, the dataset and rules that accompany it, on Github in our [sample-datasets repository](https://github.com/graknlabs/sample-datasets/tree/master/genealogy-knowledge-base).


## Identifying Entity Types

The first step is about identifying the categories of things that will be in your knowledge graph.
For example if you are modelling a retail store, valid categories may be `product`, `electronics`, `books`, etc.  It is up to you to decide the granularity of your categories.

For our genealogy knowledge graph we know that it will mostly be filled with people. So we can create an entity type:

```graql
define
  person sub entity;
```

Naturally, we could break this up into `man` and `woman` but for this example we are going to keep things simple.

## Describing Entity Types

Grakn provides you with the ability to attach resources to entity types. For example a `car` could have an `engine`, a `licence number`, and a `transmission type` as resources that help to describe it.

So what helps describe a `person`?
Philosophical debates aside let us go with something simple. A `person` typically has a `firstname`, a `lastname`, and a `gender`. We can model this and other resources that identify a person with:

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
  has gender;

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

## Supported Resource Types
The following attribute types are supported: `string`, `boolean`, `long`, `double`, `date`.

## Identifying Relationships and Roles

The next step is to ask how your data is connected, that is, what are the relationships between your data?

This can be between different entity types, for example, a `person` **drives** a `car`, or even between the same entity types, for example, a `person` **marries** another `person`.

In a Grakn, N-ary relationships are also possible. For example, a `person` has a `child` with another `person`.

In our example, we will add `marriage` and `parentship` relationships. A `marriage` has two roles: `spouse1` and `spouse2`, while `parentship` has a `parent` role and a `child` role.

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

## Allowing Roles to be Played

The next step is to give our entity types permission to play specific roles.  We do this explicitly so that we don't accidentally relate data which should not be related. For example, this will prevent us from accidentally saying that a `dog` and a `person` can have a child.

For this current example we only have one entity type, which can play all our current roles, so we explicitly state that with:

```graql
define

person sub entity
  plays parent
  plays child
  plays spouse1
  plays spouse2;
```

We have now completed our basic genealogy schema.

## The Complete Schema

The final schema will now look something like this:

```graql
define

 # Entities

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

 # Attributes

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

 # Roles and Relations

  marriage sub relationship
    relates spouse1
    relates spouse2
    has picture;

  parentship sub relationship
    relates parent
    relates child;
```

![Schema](/images/basic-schema1.png)

## Summary

In this tutorial we described our entity type `person` across separate steps. This was done to demonstrate the typical thought process when creating a schema. It is typically good practice to group entity type definitions together as above.

{% include note.html content="It is worth noting that the schema does not need to be completely finalised before loading data. The schema of a Grakn knowledge graph can be expanded even after loading data." %}

## Where Next?

We will continue to explore the development of a schema in the next section on defining a [hierarchical schema](./hierarchical-schema).



- - - -
MUST BE MERGED
- - - -

---
title: Defining Schema
keywords: graql, query, define
tags: [graql]
summary: "Defining Grakn Schema using Graql"
sidebar: documentation_sidebar
permalink: /docs/building-schema/defining-schema
folder: docs
KB: genealogy-plus
---

The page documents use of the Graql `define` and `undefine` queries, which will define a specified
[variable pattern](../querying-data/match-clause#variable-patterns) describing a schema. To follow along, or experiment
further, with the examples given below, please load the *basic-genealogy.gql* file, which can be found in the *examples*
directory of the Grakn installation zip, or on
[Github](https://github.com/graknlabs/grakn/blob/master/grakn-dist/src/examples/basic-genealogy.gql).

{% include note.html content="If you are working in the Graql shell, don't forget to `commit`." %}

## Define

[Define queries](../api-references/ddl#define-query) are used to define your schema. Any
[variable patterns](../api-references/dml#patterns) within them are added to the schema:

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell-define" data-toggle="tab">Graql</a></li>
    <li><a href="#java-define" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell-define">
<pre class="language-graql"> <code>
define
person sub entity, has name;
name sub attribute, datatype string;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java-define">
<pre class="language-java"> <code>
qb.define(
    label("person").sub("entity").has("name"),
    label("name").sub("attribute").datatype(STRING)
).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->

This example defines an entity `person` and an attribute `name`. `name` is given the datatype `string` and a `person`
can have a name.

## Undefine

[Undefine queries](../api-references/ddl#undefine-query) are used to undefine your schema. Any
[variable patterns](../api-references/dml#patterns) within them are removed from your schema:

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell-undefine-has" data-toggle="tab">Graql</a></li>
    <li><a href="#java-undefine-has" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell-undefine-has">
<pre class="language-graql"> <code>
undefine person has name;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java-undefine-has">
<pre class="language-java"> <code>
qb.undefine(label("person").has("name")).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->

This example will stop instances of a `person` from having a `name`. `person` and `name` will both still be in the
schema.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell-undefine-sub" data-toggle="tab">Graql</a></li>
    <li><a href="#java-undefine-sub" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell-undefine-sub">
<pre class="language-graql"> <code>
<!--test-ignore-->
undefine person sub entity;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java-undefine-sub">
<pre class="language-java"> <code>
<!--test-ignore-->
qb.undefine(label("person").sub("entity")).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->

This example will remove `person` from the schema entirely.

## Properties

### id

It is not possible to define a concept with the given id, as this is the job of the system. However, if you attempt to
define by id, you will retrieve a concept if one with that id already exists. The created or retrieved concept can then
be modified with further properties.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell3" data-toggle="tab">Graql</a></li>
    <li><a href="#java3" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell3">
<pre class="language-graql"> <code>
<!--test-ignore-->
define id "1376496" plays parent;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java3">
<pre class="language-java"> <code>
<!--test-ignore-->
qb.define(var().id(ConceptId.of("1376496")).plays("parent")).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->

### sub

Set up a hierarchy.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell8" data-toggle="tab">Graql</a></li>
    <li><a href="#java8" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell8">
<pre class="language-graql"> <code>
define
man sub person;
woman sub person;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java8">
<pre class="language-java"> <code>
qb.define(label("man").sub("person")).execute();
qb.define(label("woman").sub("person")).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->


### relates
Add a role to a relationship.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell9" data-toggle="tab">Graql</a></li>
    <li><a href="#java9" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell9">
<pre class="language-graql"> <code>
define siblings sub relationship, relates sibling, relates sibling;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java9">
<pre class="language-java"> <code>
qb.define(
  label("siblings").sub("relationship")
    .relates("sibling").relates("sibling")
).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->


### as
Equivalent to `sub`, but only used in `relates` for defining the hierarchy of roles.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell9" data-toggle="tab">Graql</a></li>
    <li><a href="#java9" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell9">
<pre class="language-graql"> <code>
define fatherhood sub parentship, relates father as parent, relates son as child;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java9">
<pre class="language-java"> <code>
qb.define(
  label("fatherhood").sub("parentship")
    .relates(label("father"), label("parent"))
    .relates(label("son"), label("child"))
).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->


### plays
Allow the concept type to play the given role.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell10" data-toggle="tab">Graql</a></li>
    <li><a href="#java10" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell10">
<pre class="language-graql"> <code>
define person plays sibling;
</code>
</pre>
</div>
<div role="tabpanel" class="tab-pane" id="java10">
<pre class="language-java"> <code>
qb.define(label("person").plays("sibling")).execute();
qb.define(label("person").plays("sibling")).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->


### has

Allow the concept type to have the given attribute.

This is done by creating a specific relationship relating the concept and attribute.

<ul id="profileTabs" class="nav nav-tabs">
    <li class="active"><a href="#shell11" data-toggle="tab">Graql</a></li>
    <li><a href="#java11" data-toggle="tab">Java</a></li>
</ul>

<div class="tab-content">
<div role="tabpanel" class="tab-pane active" id="shell11">
<pre class="language-graql"> <code>
define person has nickname;
</code>
</pre>
</div>

<div role="tabpanel" class="tab-pane" id="java11">
<pre class="language-java"> <code>
qb.define(label("person").has("nickname")).execute();
</code>
</pre>
</div> <!-- tab-pane -->
</div> <!-- tab-content -->
