---
pageTitle: Migration and Backup
keywords: grakn, migration, backup
longTailKeywords: grakn migration
Summary: Backing up and migrating data between versions of Grakn.
toc: false
---

# Migration and Backup

Grakn version 1.7.3 and later include tools to backup and migrate data between versions of grakn that are not data-level compatible. Please note the chart below for which versions are data-level compatible:

| Data-level Versions | Versions at Data-level | Earliest Version With Migration Available |
| ------------------- | ---------------------- | ----------------------------------------- |
| 1.7                 | 1.5.x, 1.6.x, 1.7.x    | 1.7.3                                     |
| 1.8                 | 1.8.x                  | 1.8.1                                     |
| 2.0                 | 2.0.x                  | 2.0                                       |

<div class="note">
[Important]
If you are migrating from 1.6.x or below to 2.0.x, you must first copy your `server/db` directory from your existing Grakn installation into an Grakn 1.7.3 installation. This will be fast and can be done to move from a version of Grakn without migration tools to one which has them. From 1.7.3 you are able to migrate to Grakn 2.0. 
</div>

The migration features describe beyond this point are designed for use with databases that can reasonably fit on a local disk multiple times (in the order of Gigabytes), as they make use of files to contain your data. If you have use cases for migrating data that will not fit onto disk, please reach out to us on our [Discord](https://discord.com/invite/graknlabs) community or [Forums](https://discuss.grakn.ai/) where we can advise you further.

## Backup

You can backup your data in a version-independent file using:

```
typedb server export [database] [filename].typedb
```

You can import a backup using:

```
typedb server import [database] [filename].typedb
```

These paths are relative to the current working directory of the CLI. The CLI expands the relative path to an absolute path for the server, which does the file writing directly, so you must ensure that the path is writable by the server process and should avoid symblic links where possible.

Importing a backup will not delete existing data in the database, so you should clean the database using console and reload the schema prior to the operation.

## Migration

### Schema Migration

The first step of migration is to migrate your schema. The `database schema my-database-name` command in Console allows you to get the current schema of a database as a single `define` query. This schema query can then be loaded via the Console to the new server.

Export the old schema:
```
old/typedb console
database schema [database]
```

Copy the schema into a file named `schema.tql`.

You can skip the step of exporting schema if you already have a copy of your schema to import.

If migrating from Grakn version <2.0 to version >=2.0 you need to update your schema to conform to 2.0 syntax. 

Once conforming to the new syntax, import the new schema:
```
new/typedb console
> create database [database] 
> transaction [database] schema write
[database]::schema::write> source schema.tql
```

### Data Migration

Data migration is performed using an export followed by an import.

```
old/typedb server export [database] data.typedb
new/typedb server import [database] data.typedb
```

This requires your database in the new grakn to have a valid schema that is compatible with your data. If a failure occurs during import, please check your database has the schema you expect.

Once the data has been successfully imported, you can safely delete the temporary data file with `rm data.typedb`.

## Dealing With Migration Issues

### Migration Errors

If you encounter migration errors, follow this checklist:

* Ensure that you are running the correct `typedb` command (the binary in the TypeDB directory of the server you are exporting from or importing to.)
* Ensure that the schema has been imported correctly to the new database.
* Ensure that the correct data import path was specified.
* Ensure that the data was correctly exported by checking the filesize.
* Ensure that any changed labels are remapped in the import options.

If you have any further errors, please join one of our communities and ask for assistance.

### Incompatible Schema

Between versions, some schemas will become incompatible due to syntax change. Whilst most issues can be corrected in the schema before importing it, it is possible for a label to become invalid (if the label becomes a keyword in a new version). In order to handle this scenario, we have added an option to import from 1.8 onwards that allows you to remap labels during the import.

```
typedb server import <database> <file>.grakn <old_label>=<new_label>...
```

### Implicit Relations

Schemas that use implicit relations in 1.7 and earlier (e.g. `@has-attribute`) are not supported by migration tools since they were removed in 1.8. It is therefore recommended that you convert any usage of implicit relations to real relations before migrating to 1.8.
