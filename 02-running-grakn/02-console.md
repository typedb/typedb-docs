---
pageTitle: Grakn Console
keywords: grakn, console
longTailKeywords: load schema into grakn, create grakn database, grakn console
summary: List of options and commands for the Grakn Console.
toc: false
---

## What is the Grakn Console?
The Grakn Console, along with the [Grakn Clients](../03-client-api/00-overview.md) and [Workbase](../07-workbase/00-overview.md), is an interface which we can use to read from and write to a Grakn knowledge graph. Console interacts directly with a given database that contains the Grakn knowledge graph.

## Command line arguments

| Option               | Alias | Description                                             |
|----------------------|-------|-------------------------------------------------------- |
| `--server=<address>` |       | Server address to which the console will connect to.    |
| `--version`          | `-V`  | Print version information and exit.                     |
| `--help`             | `-h`  | Enters the console connected to server hosted remotely. |

## Console commands

Console implements database management commands and transaction querying commands. These commands are separated into two levels. Initially database management commands are available, and after opening a transaction, you can start using transaction querying commands.

### Database management commands

| Command                                   | Description                                                                                           |
|-------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `database list`                           | List the databases on the server                                                                      |
| `database create <db>`                    | Create a database with name `<db>` on the server                                                      |
| `database delete <db>`                    | Delete a database with name `<db>` on the server                                                      |
| `transaction <db> schema|data read|write` | Start a transaction to database `<db>` with schema or data session, with read or write transaction    |
| `help`                                    | Print help menu                                                                                       |
| `clear`                                   | Clear console screen                                                                                  |
| `exit`                                    | Exit console                                                                                          |

### Transaction querying commands
| Command         | Description                                             |
|-----------------|---------------------------------------------------------|
| `<query>`       | Run Graql query                                         |
| `source <file>` | Run Graql queries in file                               |
| `commit`        | Commit the transaction changes and close transaction    |
| `rollback`      | Rollback the transaction to the beginning state         |
| `close`         | Close the transaction without committing changes        |
| `help`          | Print this help menu                                    |
| `clear`         | Clear console screen                                    |
| `exit`          | Exit console                                            |
