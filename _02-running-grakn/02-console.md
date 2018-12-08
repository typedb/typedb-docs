---
title: Console
keywords:
tags: []
summary:
permalink: /docs/running-grakn/console
---

## What is the Graql Console?
The Graql Console, along with [Grakn Clients](/docs/client-api/overview) and [Workbase](...), is an interface through which we can read from and write to a Grakn knowledge graph. In addition, as an admin user of [KGMS](...), we can manage users and authentication in the Graql Console.

## Console Options

### Selecting/creating a keyspace
To enter an existing or new keyspace, we use the `--keyspace` (or `-k`) option followed by the name of the keyspace. The name of keyspace can only contain alphanumeric values and `_`. Running the following command creates.

```
./graql console --keyspace keyspace_name
```

### Loading a schema into a keyspace
To load a [schema](/docs/schema/overview) into a keyspace, we use the `--file` (or `-f`) option followed by the path to the schema (`.gql`) file. In addition, we need to [select the keyspace](#selecting/creating-a-keyspace) into which the schema is to be loaded. Note that if the keyspace has not yet been created, this command also creates a new keyspace with the given name.

```
./graql console -k keyspace_name --file path/to/schema.gql
```

### Entering a remote keyspace
If the keyspace of interest is hosted remotely, we use the `--uri` (or `r`) option followed by the URI. In addition, we need to select the keyspace to enter needs to be specified. To do so, we use the `--keyspace` or (`-k`) option followed by the name of the keyspace.

```
./graql console -k keyspace_name --uri the-uri-hosting-the-keyspace
```

### Disabling inference
If we intend to ignore [inferred instances of data](...), when querying the knowledge graph, we use the `-no-infer` (or `-n`) option to disable inference.

```
./graql console -k keyspace_name --no-infer
```

### Viewing the Grakn's version
To find out which version of Grakn is installed, we use the `--version` (or `-v`) option.

## Console Commands

### Managing Users [KGMS-ONLY]
Once inside the Graql Console, we can use the following commands to authenticate users of the entered keyspace.

#### Creating a new user
```
CREATE USER username WITH PASSWORD user-password WITH ROLE admin
```

#### Updating a user
```
UPDATE USER username WITH PASSWORD new-password
```

#### Retrieving all users
```
LIST USERS
```

#### Retrieving one user
```
GET USER username
```

#### Deleing a user
```
DELETE USER username
```

### Committing changes
Any write operations executed via the console, alters the knowledge graph contained in a local copy of the keyspace. In order for these changes to be reflected on the original keyspace running on the Grakn Server, we use the `commit` command.

### Rolling back changes
As the name suggests, we use the `rollback` command to undo any uncommitted changes. This rolls back the state of the knowledge graph to how it was right after the last `commit` was made.

### Running multiline queries
The Graql Console, at the moment, does not support multiline entries. However, we can use the `edit` command which opens the text editor, specified by the $EDITOR environment variable (vim by default). This will then allows us to write one or more queries in multiple lines and have them run as soon as we exit the text editor.

### Clearing the console
In order to clear the console from any previous queries, answers and commands, we use the `clear` command.

### Deleting the entire knowledge graph
Meant to be used with caution, the `clean` command cleans not only the data but also the schema from the knowledge graph contained within the entered keyspace. This is an irreversible act that results in an empty keyspace.

### Exiting the console
To exit the console, we use the `exit` command.