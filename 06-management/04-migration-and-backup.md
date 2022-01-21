---
pageTitle: Migration and Backup keywords: typedb, migration, backup longTailKeywords: typedb migration Summary: Backing
up and migrating data between versions of TypeDB. toc: false
---

# Migration and Backup

## Migration or Backup by Copying

One method to migrate data across TypeDB distributions is by copying the data directory from the server. To do this,
simply shut down the servers, and copy the database you wish to migrate from the `server/data/` directory into the
`server/data/` directory in the destination distribution.

TypeDB will warn you when moving data across incompatible database encoding versions.

| Database encoding Version  | Compatible TypeDB Versions |
| -------------------------- | -------------------------- |
| 0                          | 2.0.0 - 2.5.0              |
| 1                          | 2.6.0 -                    |

## Migration or Backup using Export/Import

TypeDB offers a way to export all data into a binary format, and then re-import it elsewhere. Using the export feature
is a good way to bridge TypeDB versions that break backward compatibility.

Note that this process will require local disk at least twice that of the database, as they make use of files to contain
your data. If your have to migrate data that will not fit onto disk, please reach out to us on
our [Discord](https://discord.com/invite/vaticle)
community or [Forums](https://discuss.vaticle.com) where we can advise you further.

Migration or backup using the export/import features is a two-step process: schema migration followed by data migration.

### Schema Migration

The first step of migration is to migrate your schema. The `database schema my-database-name` command in Console allows
you to get the current schema of a database as a single `define` query. This schema query can then be loaded via the
Console to the new server.

Export the old schema using console (the older server must be running for this):

```
old/typedb console
> database schema [database]
```

Copy the schema into a file named `schema.tql`.

You can skip the step of exporting schema if you already have a copy of your schema to import.

If migrating from TypeDB version <2.0 to version >=2.0 you need to update your schema to conform to 2.0 syntax.

We then load the schema into the new TypeDB distribution:

```
new/typedb console
> database create <database> 
> transaction <database> schema write
[database]::schema::write> source <path to schema.tql>
[database]::schema::write> commit
```

### Data Export/Import

To create a binary export of a TypeDB database data, make sure that the TypeDB server you wish to export from is
running. After the server is running, use the following command that ships with `typedb`:

```
typedb server export --database=[database] --file=[filename].typedb
```

Note that this will NOT export the schema, only data. This file contains a complete copy of the data of the source
database.

If you have already migrated the schema into a new server distribution, you can import the data export produced using:

```
typedb server import --database=[database] --file=[filename].typedb
```

If a failure occurs during import, please check your database has the correct schema loaded first.

These paths are relative or absolute.

<div class="note">
In versions previous to 2.6.0, the `--database=` and `--file=` named arguments are not used, and you should simply use positional arugments like this:
`old/typedb server export <database> data.typedb` or `old/typedb server import --database=<database> --file=data.typedb`
</div>

## Dealing With Migration Issues

### Migration Errors

If you encounter migration errors, follow this checklist:

* Ensure that you are running the correct `typedb` command (the binary in the TypeDB directory of the server you are
  exporting from or importing to.)
* Ensure that the schema has been imported correctly to the new database.
* Ensure that the correct data import path was specified.
* Ensure that the data was correctly exported by checking the filesize.
* Ensure that any changed labels are remapped in the import options.

If you have any further errors, please join one of our communities and ask for assistance.
