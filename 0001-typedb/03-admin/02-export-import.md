---
pageTitle: Export and import
keywords: typedb, import, export, backup, save
longTailKeywords: TypeDB import data, TypeDB export data, TypeDB import database, TypeDB export database
summary: TypeDB import and export functions.
toc: false
---

# Export and import

TypeDB can export and import both schema and data of a database, but separately. 

TypeDB Console provides a way to export the database schema in TypeQL format. The resulting `.tql` file can be used to 
import a schema by executing a define query on any database on a TypeDB server (of compatible version).

TypeDB offers a way to export database data into a binary format. The resulting file can be used to import the data on 
any database with compatible schema on a TypeDB server. 

<div class="note">
[Note]
Using the export feature is the best way to migrate to a version of TypeDB that is not backward compatible.
</div>

The exported binary file might be up to two times larger than the original database. Please ensure your disk has enough 
free capacity to store a file of this size.

## Migration process

A TypeDB database consists of a schema and data. They are exported and imported separately. 

Migration using the export/import features is a two-step process: schema migration, followed by data migration.

Both import and export of schema and data require an instance of TypeDB server to be working. If you are migrating 
your data from one instance to another on the same server (for example — from old version to a newer one) be extra 
careful with what instance being addressed by the commands.

## Export

For the export to work make sure your TypeDB server with **the database to export** is working.

You can use any TypeDB Client to import schema, but only TypeDB Console can export schema. The following instructions 
are for the TypeDB Console.

The data of a database can be exported and imported only by a TypeDB server itself.

### Schema

Use [TypeDB Console](../../02-clients/02-console.md) with the following command to export a schema:

<!-- test-ignore -->
```bash
typedb console --command="database schema [database]" > [filename].tql
```

, where: 

* `[database]` — the name of the database to export data from;
* `[filename]` — the name for the file to export to.

<div class="note">
[Important]
Check the exported schema file in any text editor — delete anything before the `define` keyword.
</div>

### Data

Use the following TypeDB command to export a database data into a file:

<!-- test-ignore -->
```bash
typedb server export --database=[database] --port=[server rpc port] --file=[filename].typedb
```

, where: 

* `[database]` — the name of the database to export data from;
* `[server rpc port]` — the port number of the active TypeDB server to export from;
* `[filename]` — the name for the file to export to.

<div class="note">
[Note]
In versions previous to **2.6.0**, the `--database=` and `--file=` named arguments are not used. 
Use positional arguments instead. For example, `typedb server export [database] [filename].typedb`.
</div>

## Import

For the import to work make sure your target TypeDB server (where your database will be **migrated to**) is working.

### Schema

Create a new database (replace the [new-db] placeholder with the name of the new database):

<!-- test-ignore -->
```bash
typedb console --command="database create [new-db]"
```

Import the schema from a `tql` file to the database:

<!-- test-ignore -->
```bash
typedb console --command="transaction [new-db] schema write" --command="source [filename].tql" --command="commit"
```
, where: 

* `[new-db]` — the name of the new database to import schema to;
* `[filename]` — the name for the schema file to import from.

### Data

Use the following TypeDB command to import data from a binary file into a database:

<!-- test-ignore -->
```bash
typedb server import --database=[database] --port=[server rpc port] --file=[filename].typedb
```

, where: 

* `[database]` — the name of the database to import data to;
* `[server rpc port]` — the gRPC port number of the active TypeDB server to import to (default is 1729);
* `[filename]` — the name for the file to import from.

<div class="note">
[Note]
In versions previous to **2.6.0**, the `--database=` and `--file=` named arguments are not used. 
Use positional arguments instead. For example, `typedb server import [new-db] [filename].typedb`.
</div>

## Troubleshooting

If you encounter migration errors, follow this checklist:

* Ensure that you are running the correct `typedb` command with the **correct TypeDB server** (use `./typedb` instead 
  of `typedb` to use the TypeDB binary in the current directory instead of the default TypeDB server installation).
* Ensure that the schema has been imported correctly to the new database. 
  Use [TypeDB Studio](../../02-clients/01-studio.md) or [TypeDB Console](../../02-clients/02-console.md) to check the 
  schema.
* Ensure that the correct path was specified for the datafile import.

If you have any further errors, please join one of our communities and ask for assistance.
