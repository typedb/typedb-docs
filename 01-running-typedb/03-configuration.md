---
pageTitle: Configuring TypeDB
keywords: typedb, configure
longTailKeywords: configure typedb, typedb configuration
summary: Configure the TypeDB Server based on your production and development needs.
---

## Configure TypeDB
In this section, we learn how to configure TypeDB to have it tailored to our production and development needs.
Prior to starting, the TypeDB Server and Console read configurations from a file named `typedb.properties`.
The location of this file varies based on how TypeDB has been installed.

If downloaded manually, we can find the configuration file in the `server/conf` directory inside the unzipped folder.

If installed using Homebrew:

```
/usr/local/Cellar/typedb/{version-number}/libexec/conf/
```

If installed using APT:

```
/opt/typedb/core/server/conf/typedb.properties
```

<div class="note">
[Note]
In order for any new configuration to take affect, we must [stop](/docs/running-typedb/install-and-run/#stop-the-typedb-server) the TypeDB Server 
and [start](/docs/running-typedb/install-and-run/#start-the-typedb-server) it again.
</div>


## Where data is stored
The `server.data` config sets the path to the directory where the data for all databases gets stored. The default value is `server/data/`.

<div class="note">
[Important]
For production use, it is recommended that the `server.data` is set to a path outside of `$TYPEDB_HOME`. This helps to make the process of upgrading TypeDB easier.
</div>

## Port number
The `server.port` config sets the port on which the TypeDB Server listens to (defaults to `1729`).
TypeDB listens on all IP addresses and will be publicly accessible if the port is exposed.

## Logging
The `server.logs` config holds the path to the directory where the logs get stored. The default value is `server/logs/`.

On TypeDB Cluster it's possible to push logs into [Logstash](https://www.elastic.co/logstash/) by using configuration properties
`logstash` and `logstash.uri`.
