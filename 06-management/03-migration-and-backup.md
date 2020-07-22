---
pageTitle: Migration and Backup
keywords: grakn, migration, backup
longTailKeywords: grakn migration
Summary: Backing up and migrating data between versions of Grakn.
toc: false
---

# Migration and Backup

Some versions of Grakn include tools to backup and migrate data between versions of grakn that are not data-level compatible. Please note the chart below for which versions are data-level compatible:

| Data-level Versions | Versions at Data-level | Earliest Version With Migration Available |
| ------------------- | ---------------------- | ----------------------------------------- |
| 1.7                 | 1.5.x, 1.6.x, 1.7.x    | 1.7.3                                     |
| 1.8                 | 1.8.x                  | 1.8.1                                     |

When migrating data between versions of grakn with the same data-level, you should instead copy your `server/db/cassandra/data` directory from one installation to the other, as this will be faster and can be done to move from a version of Grakn without migration tools to a one which has them.

<div class="note">
[Important]
When upgrading with Homebrew, copy your data folder **outside** of the installation directory before upgrade, otherwise you **may lose your data**. Cautious users should back up their entire Grakn directory.
</div>

The migration features describe beyond this point are designed for use with databases that can reasonably fit on a local disk multiple times (in the order of Gigabytes), as they make use of files to contain your data. If you have use cases for migrating data that will not fit onto disk, please reach out to us on our [Discord](https://discord.com/invite/graknlabs) community or [Forums](https://discuss.grakn.ai/) where we can advise you further.

## Backup

You can backup your data in a version-independent file using:

```
grakn server export [keyspace] [filename].grakn
```

You can import a backup using:

```
grakn server import [keyspace] [filename].grakn
```

Importing a backup will not delete existing data in the keyspace, so you should clean the keyspace using console and reload the schema prior to the operation.

## Migration

### Schema Migration

The first step of migraiton is to migrate your schema. The  `grakn server schema` command allows you to get the current schema of a Grakn keyspace as a single Graql `define` query. This schema query can then be loaded via `grakn console` to the new server.

You can skip the step of exporting schema if you already have a copy of your schema to import.

```
old/grakn server schema [keyspace] > schema.gql
new/grakn console -k [keyspace] -f schema.gql
```

### Data Migration

Data migration is performed using an export followed by an import.

```
old/grakn server export [keyspace] data.grakn
new/grakn server import [keyspace] data.grakn
```

This requires your keyspace in the new grakn to have a valid schema that is compatible with your data. If a failure occurs during import, please check your keyspace has the schema you expect.

Once the data has been successfully imported, you can safely delete the temporary data file with `rm data.grakn`.

## Upgrading Grakn with Homebrew

When upgrading a Grakn installation via homebrew, we recommend that you always back up your grakn directory first to preserve your data in case the upgrade cannot be completed successfully. This is because homebrew automatically removes your installation directly after the upgrade.

`cp -R /usr/local/Cellar/grakn-core/[version]/libexec ./grakn-backup`.

Before upgrading, your should first export your schema and data. You should perform this step for every keyspace you want to upgrade.

```
grakn server schema [keyspace] > [keyspace].gql
grakn server export [keyspace] [keyspace].grakn
```

## Dealing With Migration Issues

### Migration Errors

If you encounter migration errors, follow this checklist:

* Ensure that you are running the correct Grakn command (the binary in the Grakn directory of the server you are exporting from or importing to.)
* Ensure that the schema has been imported correctly to the new keyspace.
* Ensure that the correct data import path was specified.
* Ensure that the data was correctly exported by checking the filesize.
* Ensure that any changed labels are remapped in the import options.

If you have any further errors, please join one of our communities and ask for assistance.

### Incompatible Schema

Between versions, some schemas will become incompatible due to syntax change. Whilst most issues can be corrected in the schema before importing it, it is possible for a label to become invalid (if the label becomes a keyword in a new version). In order to handle this scenario, we have added an option to import from 1.8 onwards that allows you to remap labels during the import.

```
grakn server import <keyspace> <file>.grakn <old_label>=<new_label>...
```

### Implicit Relations

Schemas that use implicit relations in 1.7 and earlier (e.g. `@has-attribute`) are not supported by migration tools since they were removed in 1.8. It is therefore recommended that you convert any usage of implicit relations to real relations before migrating to 1.8.

## About `.grakn` Files

For advanced users, operating on the `.grakn` file directly may be useful, such as to refactor various elements for a new schema. The format is a delimited protobuf stream of `Item`s which are defined (along with a more detailed description of the protocol rules) in the Grakn core source code at `server/migrate/proto/data.proto`.
