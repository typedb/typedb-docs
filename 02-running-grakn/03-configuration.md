---
pageTitle: Configuring Grakn
keywords: grakn, configure
longTailKeywords: configure grakn, grakn configuration
summary: Configure the Grakn Server based on your production and development needs.
---

## Configure Grakn
In this section, we learn how to configure Grakn to have it tailored to our production and development needs.
Prior to starting, the Grakn Server and Console read configurations from a file named `grakn.properties`.
The location of this file varies based on how Grakn has been installed.

If downloaded manually, we can find the configuration file in the `server/conf` directory inside the unzipped folder.

If installed using Homebrew:

```
/usr/local/Cellar/grakn/{installed-version}/libexec/conf/
```

If installed using RPM or APT:

```
/opt/grakn/core/server/conf/grakn.properties
```

<div class="note">
[Note]
In order for any new configuration to take affect, we must [stop](/docs/running-grakn/install-and-run/#stop-the-grakn-server) the Grakn Server 
and [start](/docs/running-grakn/install-and-run/#start-the-grakn-server) it again.
</div>


## Where data is stored
The `server.data` config sets the path to the directory where the data for all databases gets stored. The default value is `server/data/`.

<div class="note">
[Important]
For production use, it is recommended that the `server.data` is set to a path outside of `$GRAKN_HOME`. This helps to make the process of upgrading Grakn easier.
</div>

## Host and port
The `server.port` config sets the port on which the Grakn Server listens to (defaults to `1729`).
Grakn listens on all IP addresses and will be publicly accessible if the port is exposed.

## Where logs are stored
The `server.logs` config holds the path to the directory where the logs get stored. The default value is `server/logs/`.
