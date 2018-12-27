---
sidebarTitle: Console
pageTitle: Graql Console
summary:
permalink: /docs/running-grakn/console
---

## What is the Graql Console?
The Graql Console, along with the [Grakn Clients](/docs/client-api/overview) and [Workbase](...), is an interface which we can use to read from and write to a Grakn knowledge graph. Console interacts directly with a given keyspace that contains the Grakn knolwedge graph.

<!-- keyspace -> kbase -->

## Console Options {#console-options}

The options accepted by the `graql console` command are as follows.

| Option               | Alias | Mode            | Used with   | Description                                                                             |
|----------------------|-------|-----------------|-------------|---------------------------------------------------------------------------------------- |
| `--keyspace <name>`  | `-k`  | interactive     | -           | Enters console with the given keyspace. If none found with the given name, creates one. |
| `--file <path>`      | `-f`  | non-interactive | - -keyspace | Loads the given schema into the given keyspace.                                         |
| `--uri <address>`    | `-r`  | interactive     | - -keyspace | Enters the console connected to the given keyspace hosted remotely.                     |
| `--no-infer`         | `-n`  | interactive     | - -keyspace | Enters the console connected to the given keyspace with inference disabled.             |
| `--version`          | `-v`  | non-interactive | -           | Prints version of the running Grakn.                                                    |

<!-- ### Selecting/creating a keyspace
To enter an existing or new keyspace, we use the `--keyspace` (or `-k`) option followed by the name of the keyspace. The name may only contain alphanumeric values and underscores.

```
./graql console --keyspace keyspace_name
```

### Loading a schema into a keyspace
To load a [schema](/docs/schema/overview) into a keyspace, we use the `--file` (or `-f`) option followed by the path to the schema (`.gql`) file. In addition, we need to [select the keyspace](#selecting/creating-a-keyspace) into which the schema should be loaded. Note that if the keyspace has not yet been created, this command also creates a new keyspace with the given name.

```
./graql console -k keyspace_name --file path/to/schema.gql
```

### Entering a remote keyspace
If the keyspace of interest is hosted remotely, we use the `--uri` (or `r`) option followed by the target URI. In addition, we need to [select the keyspace](#selecting/creating-a-keyspace) that we would like to enter.

```
./graql console -k keyspace_name --uri the-uri-hosting-the-keyspace
```

### Disabling inference
If we intend to ignore [inferred instances of data](...) when querying the knowledge graph, we use the `-no-infer` (or `-n`).

```
./graql console -k keyspace_name --no-infer
```

### Viewing the Grakn's version
To find out which version of Grakn is installed, we use the `--version` (or `-v`) option. -->

## Console Commands {#console-commands}

Once inside the console, besides [Graql queries](/docs/query/overview), we can run the following commands.

| Option     | Description                                                                                                                                                                           |
|------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `commit`   | Any write operations, executed via the console, affects only a local copy of the keyspace. This command commits all changes to the original keyspace running on the Grakn Server.     |
| `rollback` | Undoes any changes made in the knowledge graph since the last `commit`.                                                                                                               |
| `edit`     | Opens the text-editor specified by the `$EDITOR` environment variable (vim by default). We can then write queries in multiple lines that get exectued as soon as we exit the editor.  |
| `clear`    | Clears the console from any previous queries, answers and commands.                                                                                                                   |
| `clean`    | Meant to be used with caution, removes not only the data but also the schema of the knowledge graph contained within the keyspace.                                                    |
| `exit`     | Exists the console.                                                                                                                                                                   |

<!-- ### Committing changes
Any write operations executed via the console, affects only a _local_ copy of the keyspace that contains the altered knowledge graph. In order for these changes to be reflected on the original keyspace running on the Grakn Server, we use the `commit` command.

### Rolling back changes
As the name suggests, we use the `rollback` command to undo any uncommitted changes. This rolls the state of the knowledge graph back to how it was right after the last `commit` was made.

### Running multiline queries
The Graql Console, at the moment, does not support multiline entries. However, we can use the `edit` command to open the text editor specified by the $EDITOR environment variable (vim by default). This will then allows us to write one or more queries in multiple lines and have them run as soon as we exit the text editor.

### Clearing the console
In order to clear the console from any previous queries, answers and commands, we use the `clear` command.

### Deleting the entire knowledge graph
Meant to be used with caution, the `clean` command removes not only the data but also the schema of the knowledge graph contained within the entered keyspace. This is an irreversible act that results in an empty keyspace.

### Exiting the console
To exit the console, we use the `exit` command. -->