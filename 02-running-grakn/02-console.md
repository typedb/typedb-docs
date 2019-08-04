---
pageTitle: Grakn Console
keywords: grakn, console
longTailKeywords: load schema into grakn, create grakn keyspace, grakn console
summary: List of options and commands for the Grakn Console.
toc: false
---

## What is the Grakn Console?
The Grakn Console, along with the [Grakn Clients](../03-client-api/00-overview.md) and [Workbase](../07-workbase/00-overview.md), is an interface which we can use to read from and write to a Grakn knowledge graph. Console interacts directly with a given keyspace that contains the Grakn knowledge graph.

## Console Options

The options accepted by the `grakn console` command are as follows.

| Option               | Alias | Mode            | Used with     | Description                                                                             |
|----------------------|-------|-----------------|---------------|---------------------------------------------------------------------------------------- |
| `--keyspace <name>`  | `-k`  | interactive     | -             | Enters console with the given keyspace. If none found with the given name, creates one. |
| `--file <path>`      | `-f`  | non-interactive |` --keyspace` | Loads the given schema into the given keyspace.                                         |
| `--address <address>`| `-r`  | interactive     | `--keyspace` | Enters the console connected to the given keyspace hosted remotely.                     |
| `--no_infer`         | `-n`  | interactive     | `--keyspace` | Enters the console connected to the given keyspace with inference disabled.             |
| `version`            | `-v`  | non-interactive | -             | Prints version of the running Grakn.                                                    |


## Console Commands

Once inside the console, besides [Graql queries](../11-query/00-overview.md), we can run the following commands.

| Option     | Description                                                                                                                                                                           |
|------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `commit`   | Any write operations, executed via the console, affects only a local copy of the keyspace. This command commits all changes to the original keyspace running on the Grakn Server.     |
| `rollback` | Undoes any changes made in the knowledge graph since the last `commit`.                                                                                                               |
| `editor`   | Opens the text-editor specified by the `$EDITOR` environment variable (vim by default). We can then write queries in multiple lines that get executed as soon as we exit the editor.  |
| `clear`    | Clears the console from any previous queries, answers and commands.                                                                                                                   |
| `clean`    | Meant to be used with caution, removes not only the data but also the schema of the knowledge graph contained within the keyspace.                                                    |
| `exit`     | Exists the console.                                                                                                                                                                   |
