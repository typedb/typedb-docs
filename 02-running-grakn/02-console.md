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

<!-- FIXME(vmax): console doesn't support `--database-use` and `--source` options yet; document once they are available -->
| Option               | Alias | Mode            | Used with     | Description                                                                             |
|----------------------|-------|-----------------|---------------|---------------------------------------------------------------------------------------- |
| `--help`             | `-h`  | non-interactive | -             | Display all options
| `--server=<address>` |       | non-interactive | -             | Enters the console connected to server hosted remotely.                     |
| `--version`          | `-V`  | non-interactive | -             | Prints version of the running Console.                                                    |


## Console Commands

<!-- FIXME(vmax): currently we can only execute queries via transaction command, not directly -->
Once inside the console, besides [Graql queries](../11-query/00-overview.md), we can run the following commands.

| Option     | Description                                                                                                                                                                           |
|------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `database list`   |  List the databases on the server |
| `database create <db>` | Create a database with name <db> on the server |
| `database delete <db>`   | Delete a database with name <db> on the server |
| `transaction <db> schema|data read|write`    | Start a transaction to database <db> with schema or data session, with read or write transaction |
| `help`    | Print this help menu |
| `clear`               | Clear console screen |
| `exit`     | Exists the console.                                                                                                                                                                   |
