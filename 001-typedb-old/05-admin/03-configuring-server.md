---
pageTitle: Configuring TypeDB
keywords: typedb, configure
longTailKeywords: configure typedb, typedb configuration
summary: Configure the TypeDB Server based on your production and development needs.
---

## Configure TypeDB

In this section, we learn how to configure TypeDB to have it tailored to our production and development needs.

There are two primary ways configuring TypeDB: via command line arguments, and via the configuration file.

## Command line

When we use the command `typedb server`, we can configure the server using arguments. All arguments must either be separated
by an `=` or a space. All arguments start with the prefix `--`.

Some arguments are exclusive to the command line interface:

- `--help`: print out the help menu and exit
- `--version`: print out the version of the server and exit
- `--config /path/to/external/typedb-config.yml`: use a configuration file on a specific path

Additional arguments available are derived from the configuration Yaml file. 
**Any value** from the configuration file can be overridden from the command line, as shown in
a [following section](/docs/typedb/configuration/#configuration-file-options-via-command-line).

### Getting help

The best place to get help for all available commands via the command line is using the help command:

```
typedb server --help
```

This will also list out how to use options derived from the configuration file.

## Configuration file

TypeDB accepts a configuration file with a specific Yaml format, outlined below.

<div class="note">
[Note]
In order for any new configuration to take affect, we must [stop](/docs/typedb/install-and-run/#stop-the-typedb-server) the TypeDB Server 
and [start](/docs/typedb/install-and-run/#start-the-typedb-server) it again.
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
/opt/typedb/core/server/conf/config.yml
```

### Sample Configuration

Here is a sample configuration file for TypeDB:

```
server:
  address: 0.0.0.0:1729

storage:
  data: server/data
  database-cache:
    # configure storage-layer data and index cache per database 
    # it is recommended to keep these at equal sizes
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
  connections from the local machine.

### Storage configuration

The `storage` section of the configuration file configures the storage layer of TypeDB.

- `data`: the location to write user data to. Defaults to within the server distribution under `server/data`.

<div class="note">
[Important]
For production use, it is recommended that the `server.data` is set to a path outside of `$TYPEDB_HOME`. 
This helps to make the process of upgrading TypeDB easier.
</div>

- `database-cache`: **per-database** configuration for storage-level caching
    - `data`: cache for often used data regions.
    - `index`: cache for data indexes.
  

If the index cache is too small relative to your dataset, you may find severely degraded performance. We recommend
allocating at least 2% of your database size equivalent to the index cache. For example, with
100gb of on-disk data in a database, allocate 2gb of index cache at minimum. Allocating more can improve performance.

As additional rule of thumb, we recommend the sum of `data` and `index` caches equal about 20% of the total
memory of the server.

### Logging configuration

The `log` section of the configuration file configures the logging behaviour of TypeDB.

There are three subsections:

- `output`: Define destinations to write logs to. Allowed types are `type: file`, and `type: stdout` in TypeDB. TypeDB Cluster
  also supports `type: logstash`.
- `logger`: Set up logging for code packages in TypeDB, along with a log level and output targets (referencing outputs by name
  the defined under `output`s).
- `debugger`: Set up TypeDB-specific debuggers. Right now, the only defined type is `type: reasoner`.

## Configuration file options via command line

Any option in the configuration file, we can override from the command line.

So, for example, the configuration file sets the server address as:

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
define a new logger subsection to print out all query plans, we could do the following to set the package
`com.vaticle.typedb.core.traversal` to output on a more verbose level:

```
./typedb server  \
  --server.address 0.0.0.0:1730  \
  --log.logger.traversal.filter com.vaticle.typedb.core.traversal  \
  --log.logger.traversal.level debug \
  --log.logger.traversal.output "[ file, stdout ]"
```

## Machine configuration

The minimum machine size for running a single TypeDB database is 4 (v)CPUs, 10gb memory, with SSD.
The recommended starting configuration is 8 (v)CPUs, 16gb memory, and SSD. Bulk loading is scaled effectively
by adding more CPU cores.

The memory breakdown of TypeDB is the following:
- the JVM memory: configurable when booting the server with `JAVAOPTS="-Xmx4g" typedb server`. This gives the JVM 4gb of memory. Defaults to 25% of system memory on most machines.
- storage-layer baseline consumption: approximately 2gb.
- storage-layer caches: this is about 2*cache size per database. If the `data` and `index` caches sum up to 1gb, the memory requirement is 2gb in working memory.
- memory per cpu: approximately 0.5gb additional per (v)CPU under full load.

We can estimate the amount of memory the server will need to run a single database with these factors:
```
required memory = JVM memory + 2gb + 2*(configured db-caches in gb) + 0.5gb*CPUs
```

So on a 4 cpu machine, with the default 1gb of per-database storage caches, and the JVM using 4gb of ram, 
we compute a requirement of `4gb + 2gb + 2*1gb + 0.5gb*4 = 10gb`.

Each additional database will consume at least an additional amount equal to the cache requirements (in this example, an additional 2gb of memory each).

### Open file limit 

To support large data volumes, it is important to check the open file limit the operating system imposes. 
Some unix distributions default to 1024 open file descriptors. This can be checked with:
```
ulimit -n
```

We recommend this is increased to at least 50,000.
