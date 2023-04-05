---
pageTitle: TypeDB Console
keywords: typedb, console
longTailKeywords: load schema into typedb, create typedb database, typedb console
summary: List of options and commands for the TypeDB Console.
toc: false
---

## What is the TypeDB Console?
The TypeDB Console, along with the [TypeDB Clients](../03-client-api/00-overview.md) and [Studio](../07-studio/00-overview.md), is an interface which we can use to read from and write to a TypeDB knowledge graph. Console interacts directly with a given database that contains the TypeDB knowledge graph.

## Run TypeDB Console in the terminal


### Connect to TypeDB 

Go to the directory where you have your `typedb-all` or `typedb-console` distribution unarchived, and run `./typedb console`
```
cd <your_typedb_console_dir>/
./typedb console
>
```


### Connect to TypeDB Cluster

Go to the directory where you have your `typedb-cluster-all` or `typedb-console` distribution unarchived, and run `./typedb console`
```
cd <your_typedb_console_dir>/
./typedb console --cluster=127.0.0.1:1729 --username=<username> --password --tls-enabled=<true|false>
Enter password:
>
```

### Locale settings

TypeDB can store string attributes that have characters outside the [ASCII](https://ascii.cl/) range (for example:
non-English letters, symbols, and emojis). To manipulate them using Console, the console terminal must use a locale
with a compatible code set, such as Unicode.

If it doesn't, these characters will most likely be rendered as "?" symbols in Console. If this issue occurs:

- **Windows**: use [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701?hl=en-gb&gl=GB) or run [chcp](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/chcp) in your terminal (e.g: `chcp 936` for Chinese text)
- **MacOS, Linux**: use `locale -a` to list all installed locales, and use (for example, to use `en_US.UTF-8`) `export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8`

Most systems also allow you to set the system-wide locale, however this impacts the appearance of other applications.

## Command line arguments

You can provide several command-line arguments when running Console in the terminal.


| Option                  | Alias | Description                                                          |
|-------------------------|-------|----------------------------------------------------------------------|
| `--server=<address>`    |       | Address to which Console will connect to. (TypeDB only)              |
| `--cluster=<address>`   |       | Address to which Console will connect to. (TypeDB Cluster only)      |
| `--username=<username>` |       | Username (TypeDB Cluster only)                                       |
| `--password`            |       | Password (TypeDB Cluster only)                                       |
| `--tls-enabled`         |       | Whether to connect with TLS encryption (TypeDB Cluster only)         |
| `--tls-root-ca=<path>`  |       | Path to the TLS root CA file (TypeDB Cluster only)                   |
| `--help`                | `-h`  | Show help message.                                                   |
| `--command=<commands>`  |       | Commands to run in the Console, without interactive mode             |
| `--script=<script>`     |       | Script with commands to run in the Console, without interactive mode. |
| `--version`             | `-V`  | Print version information and exit.                                  |

## Console commands

TypeDB Console provides two levels of interaction: database-level commands and transaction-level commands. The database-level command is the first level of interaction, i.e. first-level REPL. From one of the database-level commands, you can open a transaction to the database. This will open a transaction-level interface, i.e. second-level REPL.

### Database management commands

Give any of these commands inside a console at the `>` prompt.

| Command                                   | Description                                                                                                            |
|-------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `database create <db>`                    | Create a database with name `<db>` on the server.                                                                      |
| `database list`                           | List the databases on the server                                                                                       |
| `database delete <db>`                    | Delete a database with name `<db>` on the server                                                                       |
| `database schema <db>`                    | Print schema of a database with name `<db>` on the server                                                              |
| `user create <username>`                  | Create a user with name `<username>` on the server (TypeDB Cluster only)                                               |
| `user list`                               | List the users on the server (TypeDB Cluster only)                                                                     |
| `user delete <username>`                  | Delete a user with name `<username>` on the server (TypeDB Cluster only)                                               |
| `transaction <db> schema⎮data read⎮write` | Start a transaction to database `<db>` with session type `schema` or `data`, and transaction type `write` or `read`.   |
| `help`                                    | Print help menu                                                                                                        |
| `clear`                                   | Clear console screen                                                                                                   |
| `exit`                                    | Exit console                                                                                                           |

### Transaction querying commands

Give any of these commands inside a console at the `>` prompt.

| Command         | Description                                                                                                                                     |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `<query>`       | Once you're in the transaction REPL, the terminal immediately accepts a multi-line TypeQL query, and will execute it when you hit enter twice.  |
| `source <file>` | Run TypeQL queries in a file, which you can refer to using relative or absolute path. On Windows escape `\` by writing `\\`.                    |
| `commit`        | Commit the transaction changes and close transaction.                                                                                           |
| `rollback`      | Will remove any uncommitted changes you've made in the transaction, while leaving transaction open.                                             |
| `close`         | Close the transaction without committing changes, and takes you back to the database-level interface, i.e. first-level REPL.                    |
| `help`          | Print this help menu                                                                                                                            |
| `clear`         | Clear console screen                                                                                                                            |
| `exit`          | Exit console                                                                                                                                    |

### Transaction options

The following flags can be passed to the `transaction <db> schema⎮data read⎮write` command, for example:

```
transaction typedb data read --infer true
```

| Option                          | Allowed values | Description                                                    |
|---------------------------------|----------------|----------------------------------------------------------------|
| `--infer`                       | `true⎮false`   | Enable or disable inference                                    |
| `--trace-inference`             | `true⎮false`   | Enable or disable inference tracing                            |
| `--explain`                     | `true⎮false`   | Enable or disable inference explanations                       |
| `--parallel`                    | `true⎮false`   | Enable or disable parallel query execution                     |
| `--batch-size`                  | `1..[max int]` | Set RPC answer batch size                                      |
| `--prefetch`                    | `true|false`   | Enable or disable RPC answer prefetch                          |
| `--session-idle-timeout`        | `1..[max int]` | Kill idle session timeout (ms)                                 |
| `--schema-lock-acquire-timeout` | `1..[max int]` | Acquire exclusive schema session timeout (ms)                  |
| `--read-any-replica`            | `true|false`   | Allow or disallow reads from any replica (TypeDB Cluster only) |


### Non-interactive mode

To invoke console in a non-interactive manner, we can define a script file that contains the list of commands to run, then invoke console with `./typedb console --script=<script>`. We can also specify the commands to run directly from the command line using `./typedb console --command=<command1> --command=<command2> ...`.

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
> ./typedb console --script=script                                                                                                                                                                                                                    73.830s
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

The following example illustrates how to create a database, define a schema, and insert some data into TypeDB.

<!-- test-ignore -->
```typeql
$ ./typedb console

Welcome to TypeDB Console. You are now in TypeDB Wonderland!
Copyright (C) 2020 TypeDB Labs

> database create typedb
Database 'typedb' created

> database list
typedb

> transaction typedb schema write
typedb::schema::write> define person sub entity;
                      
Concepts have been defined
typedb::schema::write> commit
Transaction changes committed

> transaction typedb data write
typedb::data::write> insert $p isa person;
                    
{ p iid 0x966e80017fffffffffffffff isa person; }
typedb::data::write> commit
Transaction changes committed

> exit
```
