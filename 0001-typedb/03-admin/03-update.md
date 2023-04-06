---
pageTitle: Upgrading TypeDB server version
keywords: typedb, upgrade, version, update, migration, compatibility
longTailKeywords: updating TypeDB, upgrading TypeDB, migrating TypeDB
summary: TypeDB update procedures.
toc: false
---

# Upgrading TypeDB server version

Upgrading TypeDB installation to a newer version of TypeDB server and keeping all the data can be performed in two 
different ways:

* by reusing or copying data files used for persistent storage by the server itself.
* by exporting schema and data of databases needed and them importing them to a newer installation.

The data files method usually is the fastest one, but it may not always be possible due to compatibility issues 
in case there were some breaking changes in stored data internal format. You can check what versions of TypeDB are 
compatible with each other in the [Compatibility](#compatibility) section below.

## Copying the data files

One of the methods to migrate data from one TypeDB server version to another is by copying the data directory between 
server installations. 

To do this, simply shut down the servers of the old version, and copy the database you wish to migrate from the data 
directory (set by the `storage.data` parameter in the 
[config](01-configuration.md#the-default-location-of-the-config-file)) into the data directory of the new TypeDB server 
installation. 

Alternatively, just update the new servers 
[configuration file](01-configuration.md#the-default-location-of-the-config-file) to the use the same **data directory**
path as the old one. That is why we [recommend](01-configuration.md#storage-configuration) storing your data separately 
from your TypeDB server files.

### Compatibility

TypeDB will prevent you from using the same data files across incompatible database encoding versions. For more information on TypeDB server databases compatibility see table below.

| Database encoding Version | Compatible TypeDB Versions |
|:-------------------------:|:--------------------------:|
|             0             |       2.0.0 - 2.5.0        |
|             1             |       2.6.0 - 2.7.1        |
|             2             |       2.8.0 - latest       |

To migrate data between different database encoding versions use the [Export and import](#export-and-import) features.

## Export and import

You can use export/import functionality to migrate your data while switching to a newer version of TypeDB server. 
Please see the [Export/import](02-export-import.md) page to see how to do that.
