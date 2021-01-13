---
pageTitle: Grakn Console
keywords: grakn, console
longTailKeywords: load schema into grakn, create grakn database, grakn console
summary: List of options and commands for the Grakn Console.
toc: false
---

## What is the Grakn Console?
The Grakn Console, along with the [Grakn Clients](../03-client-api/00-overview.md) and [Workbase](../07-workbase/00-overview.md), is an interface which we can use to read from and write to a Grakn knowledge graph. Console interacts directly with a given database that contains the Grakn knowledge graph.

## Running Grakn Console in the terminal

Go to the directory whe you have your `grakn-core-all` or `grakn-core-console` distribution unarchived, and run `./grakn console`
```
cd <your_grakn_console_dir>/
./grakn console
```

## Command line arguments

You can provide several command arguments when running console in the terminal.


| Option               | Alias | Description                                             |
|----------------------|-------|-------------------------------------------------------- |
| `--server=<address>` |       | Server address to which the console will connect to.    |
| `--version`          | `-V`  | Print version information and exit.                     |
| `--help`             | `-h`  | Show help message.                                      |

## Console commands

Grakn Console provides two levels of interaction: database-level commands and transaction-level commands. The database-level command is the first level of interaction, i.e. first-level REPL. From one of the database-level commands, you can open a transaction to the database. This will open a transaction-level interface, i.e. second-level REPL.

### Database management commands

Give any of these commands inside a console at the `>` prompt.

| Command                                   | Description                                                                                           |
|-------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `database create <db>`                    | Create a database with name `<db>` on the server. For example:                                        |
                                            |  ```                                                                                                  |
                                            |  > database create my-grakn-database                                                                  |
                                            |  Database 'my-grakn-database' created                                                                 |
                                            |  ```                                                                                                  |
| `database list`                           | List the databases on the server                                                                      |
| `database delete <db>`                    | Delete a database with name `<db>` on the server                                                      |
| `transaction <db> schema|data read|write` | Start a transaction to database `<db>` with schema or data session, with read or write transaction    |
| `help`                                    | Print help menu                                                                                       |
| `clear`                                   | Clear console screen                                                                                  |
| `exit`                                    | Exit console                                                                                          |

### Transaction querying commands

Give any of these commands inside a console at the `>` prompt.

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

.
