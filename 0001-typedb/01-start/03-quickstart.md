---
pageTitle: Quickstart guide
keywords: getting started, typedb, typeql, tutorial, quickstart, overview
longTailKeywords: get started with typedb, typedb tutorial, typedb quickstart, learn typedb
summary: Learn how to create a TypeDB database, load schema and data, perform queries.
toc: false
---

# Quickstart guide

## Overview

This Quickstart guide goes through the step-by-step process of creating and interacting with a TypeDB database designed 
for an [Identity and Access Management](https://en.wikipedia.org/wiki/Identity_management) solution that will be 
described [later](04-iam-schema.md).

<div class="note">
[Important]
We highly recommend completing this guide. Its goal is to prepare an environment for TypeDB exploration and development.
The resulting database (schema and data) will be needed for example queries throughout the documentation.
</div>

## Prerequisites

This Quickstart guide takes advantage of TypeDB Studio, an IDE (integrated development environment) for TypeDB. To proceed, 
please install both TypeDB and TypeDB Studio:

- [Install TypeDB](02-installation.md)
- [Install TypeDB Studio](../../02-clients/01-studio.md#installation)

<div class="note">
[Important]
It’s recommended to use TypeDB and TypeDB Studio of the same version number in order to ensure compatibility. If 
TypeDB Studio doesn't have a version similar to the TypeDB release — use the closest lower version instead.
</div>

## Initialize database

### Start TypeDB

Run the following command in a terminal:

<!-- test-ignore -->
```bash
typedb server
```

After showing the TypeDB ASCII logo and the bootup completion time, TypeDB is ready for connections.

![TypeDB server bootup message](../../images/quickstart/quickstart-launched-typedb.png)

### Connect to TypeDB

Launch TypeDB Studio, then:

1. Click the [**Connect to TypeDB**] button (right side of the toolbar).
2. Enter `localhost:1729` in the [**Address**] field.
3. Click the [**Connect**] button (the dialog will close after a successful connection).

![Connection Manager Connected](../../images/studio/connection-interface-connected.png)

### Create a project

TypeDB Studio projects allow us to organize and save related queries for future reuse.

![Project Interface empty](../../images/quickstart/studio-projects-empty.png)

To create a new project:

1. Click the [**Open Project**] button in the [**Project**] panel (upper left).
2. Choose a directory for the project files.
3. Click the [**Open**] button.

The [**Project**] panel will now display the root directory and a nested hidden directory for unsaved files.

![Project Interface With Open Folder](../../images/studio/project-interface-created-folder.png)

### Create a database

1. Click the database icon to open the [**Manage Databases**] dialog (left side of the toolbar).

   ![Database Manager Empty](../../images/studio/studio-database.png)

2. Enter `iam` in the text field, and click the [**Create**] button next to it.
3. Click the [**Close**] button in the bottom right.

   ![Database Manager With Phone Calls Database](../../images/studio/databases-interface-iam-database.png)

4. Select `iam` from the database dropdown (next to the database icon).

### Prepare a TQL file

<!-- #todo Change the link to TypeQL --->

A [TypeDB schema](../02-dev/02-schema.md) contains entity, relation, and attribute type definitions that make up the 
data model, as well as rules which may be applied to it – all of which are expressed in [TypeQL](../../11-query), 
TypeDB’s query language.

To prepare the schema definition file:

1. Click the `+` icon in the top left corner of the [**Text-editor**] panel (directly right from the [**Project**] 
   panel).
2. Copy the TypeQL statements below into the [**Text-editor**] panel.
3. Click the save icon on the left side of the toolbar.
4. Enter `iam-schema.tql` in the [**Save As**] field.
5. Click the [**Save**] button.

<!-- test-ignore -->
```typeql
define

company sub entity,
    owns name,
    plays company-membership:company;

company-membership sub relation,
    relates company,
    relates member;

parent-company-name sub attribute,
    value string;

#rule attribute-parent-company:
#    when {
#        (company: $c, member: $t) isa company-membership;
#        $c has name $c-name;
#        ?name-value = $c-name
#    } then {
#        $t has parent-company-name ?name-value;
#    };

rule attribute-parent-company:
    when {
        (company: $c, member: $t) isa company-membership;
        $c has name $c-name;
        $pc isa parent-company-name;
        $c-name = $pc;
    } then {
        $t has $pc;
    };

root-collection sub attribute,
    value boolean;

rule automatic-member-collection:
    when {
        $c isa resource-collection;
        (member: $c) isa collection-membership;
    } then {
        $c has root-collection false;
    };

rule automatic-root-collection:
    when {
        $c isa resource-collection;
        not {
            $c has root-collection false;
        };
    } then {
        $c has root-collection true;
    };

subject sub entity,
    abstract,
    owns parent-company-name,
    owns credential,
    plays company-membership:member,
    plays group-membership:member,
    plays group-ownership:owner,
    plays object-ownership:owner,
    plays permission:subject,
    plays change-request:requester,
    plays change-request:requestee,
    plays segregation-violation:subject;

user sub subject,
    abstract;

user-group sub subject,
    abstract,
    plays group-membership:group,
    plays group-ownership:group,
    plays group-maximisation-violation:group;

object sub entity,
    abstract,
    owns parent-company-name,
    owns object-type,
    plays company-membership:member,
    plays collection-membership:member,
    plays object-ownership:object,
    plays access:object,
    plays segregation-violation:object;

resource sub object,
    abstract;

resource-collection sub object,
    abstract,
    owns root-collection,
    plays collection-membership:collection;

action sub entity,
    abstract,
    owns parent-company-name,
    owns name,
    owns object-type,
    plays company-membership:member,
    plays set-membership:member,
    plays access:action,
    plays segregation-policy:action;

operation sub action;

operation-set sub action,
    plays set-membership:set;

membership sub relation,
    # abstract,
    relates parent,
    relates member;

group-membership sub membership,
    relates group as parent;

collection-membership sub membership,
    relates collection as parent;

set-membership sub membership,
    relates set as parent;

ownership sub relation,
    # abstract,
    relates owned,
    relates owner;

group-ownership sub ownership,
    relates group as owned,
    owns ownership-type;

object-ownership sub ownership,
    relates object as owned,
    owns ownership-type;

access sub relation,
    relates object,
    relates action,
    plays permission:access,
    plays change-request:change;

permission sub relation,
    relates subject,
    relates access,
    owns review-date,
    owns validity,
    plays permission-maximisation-violation:permission;

direct-permission sub permission;
inherited-permission sub permission;

change-request sub relation,
    relates requester,
    relates requestee,
    relates change;

segregation-policy sub relation,
    relates action,
    owns name,
    plays segregation-violation:policy;

violation sub relation,
    abstract;

segregation-violation sub violation,
    relates subject,
    relates object,
    relates policy;

maximization-violation sub violation,
    abstract;

permission-maximisation-violation sub maximization-violation,
    relates permission;

group-maximisation-violation sub maximization-violation,
    relates group;

credential sub attribute,
    value string;

object-type sub attribute,
    value string;

ownership-type sub attribute,
    value string;

review-date sub attribute,
    value datetime;

validity sub attribute,
    value boolean;

person sub user,
    owns full-name,
    owns email;

business-unit sub user-group,
    owns name;

user-role sub user-group,
    owns name;

user-account sub user-group,
    owns email;

file sub resource,
    owns path,
    owns size-kb;

interface sub resource,
    owns name;

record sub resource,
    owns number;

directory sub resource-collection,
    owns path,
    owns size-kb;

application sub resource-collection,
    owns name;

database sub resource-collection,
    owns name;

table sub resource-collection,
    owns name;

id sub attribute,
    abstract,
    value string;

email sub id,
    value string;

name sub id,
    value string;

path sub id,
    value string;

number sub id,
    value string;

full-name sub attribute,
    value string;

size-kb sub attribute,
    value long;

rule transitive-membership:
    when {
        ($parent: $e1, $member: $e2) isa! $membership;
        ($parent: $e2, $member: $e3) isa! $membership;
        $membership sub membership;
        $membership relates $parent, relates $member;
    } then {
        ($parent: $e1, $member: $e3) isa $membership;
    };

#rule transitive-object-access:
#    when {
#        (collection: $c1, member: $c2) isa collection-membership;
#        $c1 isa! $c1-type;
#        $c2 isa! $c2-type;
#        $c1-type is $c2-type;
#        (object: $c1, action: $a) isa access;
#    } then {
#        (object: $c2, action: $a) isa access;
#    };
#
#rule transitive-action-access:
#    when {
#        (set: $s, member: $a) isa set-membership;
#        (object: $o, action: $s) isa access;
#    } then {
#        (object: $o, action: $a) isa access;
#    };

rule subject-permission-inheritance:
    when {
        $s isa subject;
        (group: $g, member: $s) isa group-membership;
        (subject: $g, access: $ac) isa permission;
    } then {
        (subject: $s, access: $ac) isa inherited-permission;
    };

rule object-permission-inheritance:
    when {
        $o isa object;
        (collection: $c, member: $o) isa collection-membership;
        $ac-c(object: $c, action: $a) isa access;
        $ac-o(object: $o, action: $a) isa access;
        (subject: $s, access: $ac-c) isa permission;
    } then {
        (subject: $s, access: $ac-o) isa inherited-permission;
    };

rule action-permission-inheritance:
    when {
        $a isa action;
        (set: $se, member: $a) isa set-membership;
        $ac-s(object: $o, action: $se) isa access;
        $ac-a(object: $o, action: $a) isa access;
        (subject: $s, access: $ac-s) isa permission;
    } then {
        (subject: $s, access: $ac-a) isa inherited-permission;
    };

rule segregation-violation-detection:
    when {
        $po(action: $a1, action: $a2) isa segregation-policy;
        $ac1(object: $o, action: $a1) isa access;
        $ac2(object: $o, action: $a2) isa access;
        $p1(subject: $s, access: $ac1) isa permission;
        $p2(subject: $s, access: $ac2) isa permission;
    } then {
        (subject: $s, object: $o, policy: $po) isa segregation-violation;
    };

rule permission-maximisation-violation-detection:
    when {
        $p-d(subject: $s, access: $ac) isa direct-permission;
        $p-i(subject: $s, access: $ac) isa inherited-permission;
    } then {
        (permission: $p-d, permission: $p-i) isa permission-maximisation-violation;
    };

#rule group-maximisation-violation-detection:
#    when {
#        $g1 isa user-group;
#        $g2 isa user-group;
#        not {
#            (subject: $g1, access: $ac) isa permission;
#            not { (subject: $g2, access: $ac) isa permission; };
#            not { (group: $g1, member: $s) isa group-membership; };
#            (group: $g2, member: $s) isa group-membership;
#        };
#    } then {
#        (group: $g1, group: $g2) isa group-maximisation-violation;
#    };

#rule group-maximisation-violation-detection:
#    when {
#        $g1 isa user-group;
#        $g2 isa user-group;
#        {
#            not { (subject: $g1, access: $ac) isa permission; };
#        } or {
#            (subject: $g2, access: $ac) isa permission;
#        } or {
#            (group: $g1, member: $s) isa group-membership;
#        } or {
#            not { (group: $g2, member: $s) isa group-membership; };
#        };
#    } then {
#        (group: $g1, group: $g2) isa group-maximisation-violation;
#    };

rule automatic-permission-invalidity:
    when {
        $po(action: $a1, action: $a2) isa segregation-policy;
        $ac1(object: $o, action: $a1) isa access;
        $ac2(object: $o, action: $a2) isa access;
        $p1(subject: $s, access: $ac1) isa permission;
        $p2(subject: $s, access: $ac2) isa permission;
    } then {
        $p1 has validity false;
    };

rule automatic-permission-validity:
    when {
        $p isa permission;
        not {
            $p has validity false;
        };
    } then {
        $p has validity true;
    };

rule add-view-permission:
    when {
        $modify isa action, has name "modify_file";
        $view isa action, has name "view_file";
        $ac_modify (object: $obj, action: $modify) isa access;
        $ac_view (object: $obj, action: $view) isa access;
        (subject: $subj, access: $ac_modify) isa permission;
    } then {
        (subject: $subj, access: $ac_view) isa permission;
    };
```

### Upload the schema

To execute the TypeQL statements in the opened file and send them as queries:

1. Ensure the [**Session type**] (schema / data) switch (next to the database dropdown) is set to `schema`.
2. Ensure the [**Transaction type**] (write / read) switch is set to `write`.

   ![Select transaction type](../../images/quickstart/studio-select-transaction-type.png)

3. Click the 'Run Query' button (with a 'play' symbol, in the middle of the toolbar) to start the transaction.
4. Click the 'Commit Transaction' button (with a checkmark symbol, left of the 'Run Query' button) to commit the changes.

The transaction has been committed, and `iam` database now has a schema.

The Types panel will now display the entity, relation, and attribute types within a type hierarchy of the schema.

![Types browser with IAM schema](../../images/quickstart/studio-types-browser-iam.png)

Data can now be inserted.

## First important queries

### Read the schema

TypeQL can be used to query the schema.

To execute a simple schema query:

1. Ensure the [**Session type**] (schema / data) switch is set to `schema` (next to the database dropdown).
2. Ensure the [**Transaction type**] (write / read) switch is set to `read`.
3. Click the `+` icon right from the [**Project**] panel next to the `iam-schema.tql` tab in the [**Text-editor**] panel.
4. Copy the TypeQL statement below.
5. Click the green “play” button.

<!-- test-ignore -->
```typeql
match $t sub thing;
```
The above query returns all types in the schema and displays the results as a graph.

<div class="note">
[Warning]
The `thing` base type will be deprecated in TypeDB version `3.0`. Consider using `entity`, `attribute`, or `relation` 
base type instead. To produce the same result as the above example, use the following query:

<!-- test-ignore -->
```typeql
match $s sub $t; { $t type entity; } or { $t type relation; } or { $t type attribute; };
```

</div>

![IAM schema graph](../../images/quickstart/studio-iam-schema.png)

### Insert data

We will insert data the same way we created the schema, by creating a `.tql` file in our project and executing it.

To create the file:

1. Click the `+` icon right from the [**Project**] panel next to the `iam-schema.tql` tab in the [**Text-editor**] panel.
2. Copy the TypeQL statements below.
3. Click the save icon (left side of toolbar).
4. Enter `iam-data.tql` in the [**Save As**] field.
5. Click the [**Save**] button.

<!-- test-ignore -->
```typeql
# Subjects
insert $p isa person, has full-name "Masako Holley", has email "masako.holley@vaticle.com";  # No access
insert $p isa person, has full-name "Pearle Goodman", has email "pearle.goodman@vaticle.com";  # Sales manager
insert $p isa person, has full-name "Kevin Morrison", has email "kevin.morrison@vaticle.com";  # Full access

# Objects
insert $f isa file, has path "iopvu.java", has size-kb 55;
insert $f isa file, has path "zlckt.ts", has size-kb 143;
insert $f isa file, has path "psukg.java", has size-kb 171;
insert $f isa file, has path "axidw.java", has size-kb 212;
insert $f isa file, has path "lzfkn.java", has size-kb 70;
insert $f isa file, has path "budget_2022-05-01.xlsx", has size-kb 758;
insert $f isa file, has path "zewhb.java";
insert $f isa file, has path "budget_2021-08-01.xlsx", has size-kb 1705;
insert $f isa file, has path "LICENSE";
insert $f isa file, has path "README.md";

# Operations
insert $o isa operation, has name "modify_file";
insert $o isa operation, has name "view_file";

# Potential access types
match $ob isa file, has path "iopvu.java"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "zlckt.ts"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "psukg.java"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "axidw.java"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "lzfkn.java"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "budget_2022-05-01.xlsx"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "zewhb.java"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "budget_2021-08-01.xlsx"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "LICENSE"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "README.md"; $op isa operation, has name "modify_file"; insert $a (object: $ob, action: $op) isa access;

match $ob isa file, has path "iopvu.java"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "zlckt.ts"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "psukg.java"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "axidw.java"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "lzfkn.java"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "budget_2022-05-01.xlsx"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "zewhb.java"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "budget_2021-08-01.xlsx"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "LICENSE"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;
match $ob isa file, has path "README.md"; $op isa operation, has name "view_file"; insert $a (object: $ob, action: $op) isa access;

# Permissions
match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "iopvu.java";
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access;
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "zlckt.ts"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "psukg.java"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "axidw.java"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "lzfkn.java"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "budget_2022-05-01.xlsx"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "zewhb.java"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "budget_2021-08-01.xlsx"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "LICENSE"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Kevin Morrison"; $o isa object, has path "README.md"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Pearle Goodman"; $o isa object, has path "budget_2022-05-01.xlsx"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Pearle Goodman"; $o isa object, has path "zewhb.java"; 
      $a isa action, has name "view_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Pearle Goodman"; $o isa object, has path "budget_2021-08-01.xlsx"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Pearle Goodman"; $o isa object, has path "LICENSE"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;

match $s isa subject, has full-name "Pearle Goodman"; $o isa object, has path "README.md"; 
      $a isa action, has name "modify_file"; $ac (object: $o, action: $a) isa access; 
insert $p (subject: $s, access: $ac) isa permission;
```

To execute the TypeQL statements copied from code block above:

1. Ensure the [Session type] (schema / data) switch (next to the database dropdown) is set to `data`.
2. Ensure the [Transaction type] (write / read) switch is set to `write`.
3. Click the green “play” button.
4. Click the “checkmark” button.

The transaction has been committed, and data can now be queried.

### Read data

To retrieve data from a database:

1. Click the `+` icon right from the [**Project**] panel next to the `iam-data.tql` tab in the [**Text-editor**] panel.
2. Ensure the [Session type] (schema / data) switch (next to the database dropdown) is set to `data`.
3. Ensure the [Transaction type] (write / read) switch is set to `read`.
4. Replace the TypeQL statement in the [**Text-editor**] panel with the one below.
5. Click the green “play” button.

<!-- test-ignore -->
```typeql
match $f isa file, has path $fp;
```

The above query returns all `file` entities with their `path` attributes. TypeDB Studio displays the results as in 
the image below.

![IAM data graph](../../images/quickstart/studio-iam-data.png)

## Schema and data

The Quickstart guide above provides a fast and easy way to set up the minimum IAM database environment:
a TypeDB database with IAM schema and a small dataset. It can be used for examples in this documentation
or for independent exploration of TypeDB features.

The files that have been used in the guide above:

- [iam-schema.tql](../../files/iam/iam-schema.tql) — TypeQL script for the IAM schema definition.
- [iam-data.tql](../../files/iam/iam-data.tql) — TypeQL script to load a sample dataset into the IAM schema.

We can do the same process of creating a database, loading schema and data through any other TypeDB Client. Here is 
an example with TypeDB Console:

```bash
# create database
typedb console --command="database create test-iam-db"

# load schema into the new database from a file
typedb console --command="transaction test-iam-db schema write" --command="source iam-schema.tql" --command="commit"

# load data into the new database from a file
typedb console --command="transaction test-iam-db data write" --command="source iam-data.tql" --command="commit"

# check the data loaded (single quotes for bash syntax compatibility with the variable $t)
typedb console --command="transaction test-iam-db data read" --command='match $t isa thing; get $t;'
```
