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


### Connecting to Grakn Core

Go to the directory whe you have your `grakn-core-all` or `grakn-core-console` distribution unarchived, and run `./grakn console`
```
cd <your_grakn_console_dir>/
./grakn console
```


### Connecting to Grakn Cluster

<div class="note">
[Warning]
Connecting to Grakn Cluster **requires** a special option, specifying the server address and port number:

```
./grakn console --cluster=127.0.0.1:1729
```

Failing to do so results in incorrect behaviour.
This is a known issue which is going to be fixed soon.
</div>

## Command line arguments

You can provide several command-line arguments when running Console in the terminal.


| Option                | Alias | Description                                                           |
|-----------------------|-------|-----------------------------------------------------------------------|
| `--cluster=<cluster>` |       | Grakn Cluster address to which Console will connect to.               |
| `--help`              | `-h`  | Show help message.                                                    |
| `--script=<script>`   |       | Script with commands to run in the Console, without interactive mode. |
| `--server=<server>`   |       | Grakn Core address to which Console will connect to.                  |
| `--version`           | `-V`  | Print version information and exit.                                   |

## Console commands

Grakn Console provides two levels of interaction: database-level commands and transaction-level commands. The database-level command is the first level of interaction, i.e. first-level REPL. From one of the database-level commands, you can open a transaction to the database. This will open a transaction-level interface, i.e. second-level REPL.

### Database management commands

Give any of these commands inside a console at the `>` prompt.

| Command                                   | Description                                                                                                            |
|-------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `database create <db>`                    | Create a database with name `<db>` on the server.                                                                      |
| `database list`                           | List the databases on the server                                                                                       |
| `database delete <db>`                    | Delete a database with name `<db>` on the server                                                                       |
| `database schema <db>`                    | Print schema of a database with name `<db>` on the server                                                              |
| `transaction <db> schema|data read|write` | Start a transaction to database `<db>` with session type `schema` or `data`, and transaction type `write` or `read`.   |
| `help`                                    | Print help menu                                                                                                        |
| `clear`                                   | Clear console screen                                                                                                   |
| `exit`                                    | Exit console                                                                                                           |

### Transaction querying commands

Give any of these commands inside a console at the `>` prompt.

| Command         | Description                                                                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `<query>`       | Once you're in the transaction REPL, the terminal immediately accepts a multi-line Graql query, and will execute it when you hit enter twice.   |
| `source <file>` | Run Graql queries in a file, which you can refer to using relative or absolute path. On Windows escape `\` by writing `\\`.                                                            |
| `commit`        | Commit the transaction changes and close transaction.                                                                                           |
| `rollback`      | Will remove any uncommitted changes you've made in the transaction, while leaving transaction open.                                             |
| `close`         | Close the transaction without committing changes, and takes you back to the database-level interface, i.e. first-level REPL.                    |
| `help`          | Print this help menu                                                                                                                            |
| `clear`         | Clear console screen                                                                                                                            |
| `exit`          | Exit console                                                                                                                                    |

### Transaction options

The following flags can be passed to the `transaction <db> schema|data read|write` command, for example:

```
transaction grakn data read --infer true
```

| Option                          | Allowed values | Description                                   |
|---------------------------------|----------------|-----------------------------------------------|
| `--infer`                       | `true|false`   | Enable or disable inference                   |
| `--trace-inference`             | `true|false`   | Enable or disable inference tracing           |
| `--explain`                     | `true|false`   | Enable or disable inference explanations      |
| `--parallel`                    | `true|false`   | Enable or disable parallel query execution    |
| `--batch-size`                  | `1..[max int]` | Set RPC answer batch size                     |
| `--prefetch`                    | `true|false`   | Enable or disable RPC answer prefetch         |
| `--session-idle-timeout`        | `1..[max int]` | Kill idle session timeout (ms)                |
| `--schema-lock-acquire-timeout` | `1..[max int]` | Acquire exclusive schema session timeout (ms) |

When connecting to Grakn Cluster, the following flags are additionally available:

| Option               | Allowed values | Description                              |
|----------------------|----------------|------------------------------------------|
| `--read-any-replica` | true|false     | Allow or disallow reads from any replica |


### Non-interactive mode

To invoke console in a non-interactive manner, we can define a script file that contains the list of commands to run, then invoke console with `./grakn console --script=<script>`. We can also specify the commands to run directly from the command line using `./grakn console --command=<command1> --command=<command2> ...`.

For example given the following command script file:

```
database create test
transaction test schema write
    define person sub entity;
    commit
transaction test data write
    insert $x isa person;
    commit
transaction test data read
    match $x isa person;
    close
database delete test
```

You will see the following output:

```
> ./grakn console --script=script                                                                                                                                                                                                                    73.830s
+ database create test
Database 'test' created
+ transaction test schema write
++ define person sub entity;
Concepts have been defined
++ commit
Transaction changes committed
+ transaction test data write
++ insert $x isa person;
{ $x iid 0x966e80017fffffffffffffff isa person; }
answers: 1, duration: 87 ms
++ commit
Transaction changes committed
+ transaction test data read
++ match $x isa person;
{ $x iid 0x966e80018000000000000000 isa person; }
answers: 1, duration: 25 ms
++ close
Transaction closed without committing changes
+ database delete test
Database 'test' deleted
```

The indentation in the script file are only for visual guide and will be ignored by the console. Each line in the script is interpreted as one command, so multiline query is not available in this mode.


## Examples

The following example illustrates how to create a database, define a schema, and insert some data into Grakn.

<!-- test-ignore -->
```graql
$ ./grakn console

Welcome to Grakn Console. You are now in Grakn Wonderland!
Copyright (C) 2020 Grakn Labs

> database create grakn
Database 'grakn' created

> database list
grakn

> transaction grakn schema write
grakn::schema::write> define person sub entity;
                      
Concepts have been defined
grakn::schema::write> commit
Transaction changes committed

> transaction grakn data write
grakn::data::write> insert $p isa person;
                    
{ p iid 0x966e80017fffffffffffffff isa person; }
grakn::data::write> commit
Transaction changes committed

> exit
```
