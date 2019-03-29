---
pageTitle: Configuring Grakn
keywords: grakn, configure
longTailKeywords: configure grakn, grakn configuration
summary: Configure the Grakn Server based on your production and development needs.
---

## Configure Grakn
In this section, we learn how to configure Grakn to have it tailored to our production and development needs.
Prior to starting, the Grakn Server and Console read configurations from a file named `grakn.properties`. The location of this file varies based on how Grakn has been installed.

If downloaded manually, we can find the configuration file in the `conf` directory inside the unzipped folder.

If installed using Homebrew:

```
/usr/local/Cellar/grakn/{installed-version}/libexec/conf/
```

If installed using RPM/Yum or Debian:

```
/opt/grakn/core/conf/grakn.properties
```

<div class="note">
[Note]
In order for any new configuration to take affect, we must [stop](/docs/running-grakn/install-and-run/#stop-the-grakn-server) the Grakn Sever and [start](/docs/running-grakn/install-and-run/#start-the-grakn-server) it again.
</div>

## The default keyspace
The `knowledge-base.default-keyspace` config sets the default keyspace that the Grakn Console falls back on when no [`--keyspace` option](../02-running-grakn/02-console.md#console-options) is specified. The default value is `grakn`.

## Mitigating the supernode problem
Grakn uses sharding to mitigate against supernodes. The `knowledge-base.sharding-threshold` config specifies the number of instances after which Grakn shards any type node. A larger threshold increases runtime as a Grakn knowledge graph grows while decreasing the likelihood of supernodes. A smaller threshold creates supernodes more frequently. The default value is `10000`.

## Where data is stored
The `data-dir` config sets the path to the directory where the data for all keyspaces gets stored. The default value is `server/db/`.

<div class="note">
[Important]
For production use, it is recommended that the `data-dir` is set to a path outside of `$GRAKN_HOME`. This helps to make the process of upgrading Grakn easier.
</div>

## Host and port
The `server.host` and `grpc.port` configs set the IP address and the port on which the Grakn Server listens to. The default values are `0.0.0.0` and `48555` respectively.

## Where logs are stored
The `log.dirs` config holds the path to the directory where the logs get stored. The default value is `logs/`.

## Verbosity of the logs
The `log.level` config specifies the verbosity of the logs. The default value is `INFO` and the options are as follows:
- `ERROR`: critical errors indicating that the application has failed.
- `WARN`: errors that do not affect the overall running of the application.
- `INFO`: minimally verbose, including Grakn server lifecycle events.
- `DEBUG`: verbose, non-production use, server task lifecycle events.
- `TRACE`: extraordinarily verbose, including graql query traversal paths, extra task lifecycle events and Kafka consumer offsets.

## Connection timeout
The `storage.connection-timeout` config holds the maximum number of milliseconds that Grakn waits for a response from the storage backend before terminating the request. The default value is `2000`.
