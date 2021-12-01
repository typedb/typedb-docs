---
pageTitle: Configuring TypeDB keywords: typedb, configure longTailKeywords: configure typedb, typedb configuration
summary: Configure the TypeDB Server based on your production and development needs.
---

## Configure TypeDB

In this section, we learn how to configure TypeDB to have it tailored to our production and development needs.

There are two primary ways configuring TypeDB: via command line arguments, and via the configuration file.

## Command line configuration

When we use the command `typedb server`, we configure the server using arguments. All arguments must either be separated
by an `=`, or a space. All arguments start with the prefix `--`.

Some arguments are exclusive to the command line interface:

- `--help`: print out the help menu and exit
- `--version`: print out the version of the server and exit
- `--config /path/to/external/typedb-config.yml`: use a configuration file on a specific path

All other arguments are derived from the configuration Yaml file. **Any value** from the configuration file can be
overridden from the command line, as shown in
a [following section](/docs/running-typedb/configuration/#command-line-configuration).

### Getting help

The best place to get help for all available commands via the command line is using the help command:

```
typedb server --help
```

This will also list out all ways to setting options derived from the configuration file.

## Configuration file

TypeDB accepts a configuration file with a specific Yaml format, outlined below.

<div class="note">
[Note]
In order for any new configuration to take affect, we must [stop](/docs/running-typedb/install-and-run/#stop-the-typedb-server) the TypeDB Server 
and [start](/docs/running-typedb/install-and-run/#start-the-typedb-server) it again.
</div>

### Locating the default configuration file

TypeDB ships with a default configuration file. The location of this file varies based on how TypeDB has been installed.

If downloaded manually, we can find the configuration file in the `server/conf` directory inside the unzipped folder.

If installed using Homebrew:

```
/usr/local/Cellar/typedb/{version-number}/libexec/server/conf/
```

If installed using APT:

```
/opt/typedb/core/server/conf/typedb.yml
```

### Sample Configuration

Here is a sample configuration file for TypeDB:

```
server:
  address: 0.0.0.0:1729

storage:
  data: server/data
  db-cache:
    # configure data and index per database in the storage layer
    # for large datasets, it is more important to have a large index cache than a large data cache
    data: 500mb
    index: 500mb

log:
  output:
    stdout:    # note: this is a user-defined name
      type: stdout
    file:      # note: this is a user-defined name
      type: file
      directory: server/logs
      file-size-cap: 50mb
      archives-size-cap: 1gb
  logger:
    default:   # note: the default logger must be defined
      level: warn
      output: [ stdout, file ]
    typedb:    # note: this is a user-defined name
      filter: com.vaticle.typedb.core
      level: info
      output: [ stdout, file ]
    storage:
      filter: com.vaticle.typedb.core.rocks
      level: warn # on 'debug' the server will periodically log storage layer properties
      output: [ stdout, file ]
  debugger:
    reasoner:   # note: this is a user-defined name
      enable: false
      type: reasoner
      output: file

vaticle-factory:
  enable: false
```

### Server configuration

The `server` section of the configuration file configures network and RPC options.

- `address`: the address to listen for GRPC clients on. Use `0.0.0.0` to listen to all connections, and `localhost` for
  connections from the local machine

### Storage configuration

The `storage` section of the configuration file configures the storage layer of TypeDB

- `data`: the location to write user data to. Defaults to within the server distribution under `server/data`.

<div class="note">
[Important]
For production use, it is recommended that the `server.data` is set to a path outside of `$TYPEDB_HOME`. This helps to make the process of upgrading TypeDB easier.
</div>

- `db-cache`: **per-database** configuration for storage-level caching
    - `data`: cache for often used data regions. Increasing this can improve performance, particularly within a transaction.
    - `index`: cache for data indexes. Increasing this can improve performance for large datasets.
  
We recommend that the sum of `data` and `index` caches equal about 20% of the total memory of the server.

### Logging configuration

The `log` section of the configuration file configures the logging behaviour of TypeDB.

There are three subsections:

- `output`: Define destinations to write logs to. Allowed types are `type: file`, and `type: stdout` in TypeDB. Cluster
  also supports `type: logstash`.
- `logger`: Set up logging for code packages in TypeDB, along with a log level and output targets (referencing by name
  the defined `output`s).
- `debugger`: Set up TypeDB-specific debuggers. Right now, the only defined type is `type: reasoner`.

## Command line configuration

Any option in the configuration file, we can override of extend from the command line.

So, for example, if the configuration file sets the server address as:

```
server:
  address: 0.0.0.0:1729
```

If we want to use port 1730 instead of 1729, we can either update the configuration file, or override it from the
command line using:

```
./typedb server --server.address 0.0.0.0:1730
```

To set a completely new section of the configuration that isn't present yet, we follow the same pattern. For example, to
define a new logger to print out all query plans, we could do the following to set the package
`com.vaticle.typedb.core.traversal` to output on a more verbose level:

```
./typedb server  \
  --server.address 0.0.0.0:1730  \
  --log.logger.traversal.filter com.vaticle.typedb.core.traversal  \
  --log.logger.traversal.level debug \
  --log.logger.traversal.output "[ file, stdout ]"
```

## Machine configuration

The minimum recommended machine size for running a single database is 4 cores, 10gb memory, with SSD.

The memory breakdown of TypeDB is the following:
- the JVM memory: configurable when booting the server with `JAVAOPTS="-Xmx4g" typedb server`. This gives the JVM 4gb of memory. Defaults to 25% of system memory on most machines.
- storage-layer baseline consumption: approximately 2gb.
- storage-layer caches: this is about 2*cache size per database. If your `data` and `index` caches sum up to 1gb, the memory requirement is 2gb in working memory.
- a scaling amount of memory in the number of cores available: approximately 0.5gb additional per core when fully utilised.

We can estimate the amount of memory your server will need to run a single database with these factors:
```
required memory = JVM memory + 2gb + 2*(configured db-caches in gb) + 0.5gb*CPUs
```

So on a 4 core machine, with the default 1gb of caches, and the JVM using 4gb of ram, we compute a requirement of `4gb + 2gb + 2*1gb + 0.5*4 = 10gb`.

Each additional database will consume at least an additional amount equal to the cache requirements (in this example, an additional 2gb of memory each).

### Open file limit 

To support large data volumes, it is important to check the open file limit the operating system imposes. 
Some unix distributions default to 1024 open file descriptors. This can be checked with:
```
ulimit -n
```

We recommend this is increased to at least 50,000.