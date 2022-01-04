---
pageTitle: Migration and Backup
keywords: typedb, migration, backup
longTailKeywords: typedb migration
Summary: Backing up and migrating data between versions of TypeDB.
toc: false
---

# Migration and Backup

TypeDB will warn you when moving data across incompatible binary-data layer versions.

Here is the compatibility chart of loaded data of TypeDB:

| Data Encoding Version | Compatible TypeDB Versions |
| --------------------- | -------------------------- |
| 1                     | 2.0.0 - 2.5.0              |
| 2                     | 2.6.0 -                    |
  

<div class="note">
[Important]
If you are migrating from 1.6.x or below to 2.0.x, you must first copy your `server/db` directory from your existing Grakn installation into an Grakn 1.7.3 installation. This will be fast and can be done to move from a version of TypeDB without migration tools to one which has them. From 1.7.3 you are able to migrate to TypeDB 2.0. 
</div>

The migration features describe beyond this point are designed for use with databases that can reasonably fit on a local disk at least twice, as they make use of files to contain your data. If you have use cases for migrating data that will not fit onto disk, please reach out to us on our [Discord](https://discord.com/invite/vaticle) community or [Forums](https://discuss.vaticle.com) where we can advise you further.

## Data Backup

You can back up your data (NOT schema!) in a version-independent file using:

```
typedb server export --database=[database] --file=[filename].typedb
```

You can import a backup into a new database with a compatible schema using:

```
typedb server import --database=[database] --file=[filename].typedb
```

These paths are relative or absolute. 

Importing a backup will not delete existing data in the database, so you should clean the database using console and reload the schema prior to the operation.

## Migration

### Schema Migration

The first step of migration is to migrate your schema. The `database schema my-database-name` command in Console allows you to get the current schema of a database as a single `define` query. This schema query can then be loaded via the Console to the new server.

Export the old schema using console:
```
old/typedb console
> database schema [database]
```

Copy the schema into a file named `schema.tql`.

You can skip the step of exporting schema if you already have a copy of your schema to import.

If migrating from TypeDB version <2.0 to version >=2.0 you need to update your schema to conform to 2.0 syntax. 

Once conforming to the new syntax, import the new schema:
```
new/typedb console
> database create <database> 
> transaction <database> schema write
[database]::schema::write> source schema.tql
[database]::schema::write> commit
```

### Data Migration

Data migration is performed using an export followed by an import.

```
old/typedb server export --database=<database> --file=data.typedb
new/typedb server import --database=<database> --file=data.typedb
```

This requires your database in the new typedb to have a valid schema that is compatible with your data. If a failure occurs during import, please check your database has the schema you expect.

Once the data has been successfully imported, you can safely delete the data file with `rm data.typedb`.

<div class="note">
In versions previous to 2.6.0, the `--database=` and `--file=` named arguments are not used, and you should simply use positional arugments like this:
`old/typedb server export <database> data.typedb` or `old/typedb server import --database=<database> --file=data.typedb`
</div>

## Dealing With Migration Issues

### Migration Errors

If you encounter migration errors, follow this checklist:

* Ensure that you are running the correct `typedb` command (the binary in the TypeDB directory of the server you are exporting from or importing to.)
* Ensure that the schema has been imported correctly to the new database.
* Ensure that the correct data import path was specified.
* Ensure that the data was correctly exported by checking the filesize.
* Ensure that any changed labels are remapped in the import options.

If you have any further errors, please join one of our communities and ask for assistance.
