---
pageTitle: Install and Run TypeDB Cluster
keywords: setup, getting started, typedb, download, install, server, linux, mac, windows, docker
longTailKeywords: typedb on linux, typedb on mac, typedb on windows, start typedb cluster
summary: Install and run the TypeDB Cluster on Linux, Mac or Windows.
toc: false
---

## Obtaining Commercial License

TypeDB Cluster is a commercial offering that provides production-grade experience - high-availability, scalability, and security. If you are interested, please contact sales to obtain the license.

## System Requirements
TypeDB Cluster runs on Mac, Linux and Windows. The only requirement is Java (version 11 or higher) which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

## Download and Install TypeDB Cluster

<div class="tabs light">
[tab:Linux]

#### Manual Download

Download the [latest release](https://repo.vaticle.com/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via terminal.

#### Other package managers

If TypeDB Cluster doesn't have a distribution you need, please open an issue [on GitHub](https://github.com/vaticle/typedb/issues).


Having installed or downloaded TypeDB Cluster, we can now start the [Cluster](#start-the-typedb-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Mac OS X]

#### Manual Download
Download the [latest release](https://repo.vaticle.com/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded TypeDB, we can now start the [Server](#start-the-typedb-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://repo.vaticle.com/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded TypeDB, we can now start the [Server](#start-the-typedb-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]


[tab:Docker]

#### Using Docker

To pull the TypeDB Docker image, run:

```
docker pull vaticle/typedb-cluster:latest
```

#### Without an External Volume

For testing purposes, run:
```
docker run --name typedb -d -p 1729:1729 vaticle/typedb-cluster:latest
```

<div class="note">
[Warning]
Running the instance without specifying a volume does NOT save the data if the instance is killed.
</div>

#### With an External Volume

To ensure that data is preserved even when the instance is killed or restarted, run:

```
docker run --name typedb -d -v $(pwd)/db/:/opt/typedb-cluster-all-linux/server/db/ -p 1729:1729 vaticle/typedb-cluster:latest
```

Having started the instance, the TypeDB Cluster is expected to be running on port `1729` on your machine.

To interact with the [TypeDB Console](../02-console/01-console.md), run:

```
docker exec -ti typedb bash -c '/opt/typedb-cluster-all-linux/typedb console'
```
[tab:end]
</div>

## Starting and Stopping Single-node Cluster

### Starting

If you have installed TypeDB using a package manager, to start the TypeDB Cluster, run `typedb server`.

Otherwise, if you have manually downloaded TypeDB, `cd` into the unzipped folder and run `./typedb server`.


### Stopping

To stop the TypeDB Cluster, press Ctrl-C in same terminal as the one where you started it in.


## Starting and Stopping Multi-node Cluster

### Starting

While it's possible to run TypeDB Cluster in a single-node mode, a truly highly-available and fault-tolerant
production-grade setup includes setting up multiple servers to connect and form a cluster. At every time, one
of those servers acts as a leader and others are followers. Increasing number of nodes increases tolerance to
failure: to tolerate N nodes failing, cluster needs to consist of 2*N+1 nodes.
This section describes how it's done on an example 3-node setup (in this case, one node can fail and no data is lost).

Each node binds to two ports: a client port which TypeDB client drivers connect to (`1729`), and a server port (`1730`)
which is used for inter-node server-to-server communication.

For the tutorial, it's assumed that all three nodes are on the same virtual network and have relevant ports
unblocked by the firewall. Node have IP addresses of `10.0.0.1`, `10.0.0.2` and `10.0.0.3` and hostnames of
`node1`, `node2` and `node3`.

<div class="note">
[Note]
If you're using a single machine to host all nodes, you can prefix the port with the node number; this way
`1729` and `1730` would turn into `11729`, `11730`; `21729`, `21730` and so on.
</div>

This is how TypeDB Cluster would be started:

```bash
user@node1:~/typedb-cluster/$ ./typedb server --address=10.0.0.1:1729:1730 --peer 10.0.0.1:1729:1730 --peer 10.0.0.2:1729:1730 --peer 10.0.0.3:1729:1730

user@node2:~/typedb-cluster/$ ./typedb server --address=10.0.0.2:1729:1730 --peer 10.0.0.1:1729:1730 --peer 10.0.0.2:1729:1730 --peer 10.0.0.3:1729:1730

user@node3:~/typedb-cluster/$ ./typedb server --address=10.0.0.3:1729:1730 --peer 10.0.0.1:1729:1730 --peer 10.0.0.2:1729:1730 --peer 10.0.0.3:1729:1730
```  

<div class="note">
[Note]
This guide assumes application accessing TypeDB Cluster resides on the same private network. If this is *not* the case,
TypeDB Cluster also supports using different IP addresses for client and server communication. In order to do that client
and server addresses need to be passed separated by a comma to `--address` and `--peer` options:

```
./typedb server \
    --address external-host-1:1729,10.0.0.1:1730 \
    --peer external-host-1:1729,10.0.0.1:1730 \
    --peer external-host-2:1729,10.0.0.2:1730 \
    --peer external-host-3:1729,10.0.0.3:1730`
```

In this case, port `1729` would need to be open to public and clients would use
`external-host-1`, `external-host-2` and `external-host-3` hostname to communicate with TypeDB Cluster;
inter-server communication would be done over private network using port `1730`.
</div>

### Stopping

Stopping the TypeDB Cluster is done the same way as with single node: pressing Ctrl+C in the terminal that was used to start it.
All nodes would be to be shut down independently.

## Summary
So far we have learned how to download, install and run the TypeDB Cluster.

Next, we learn how to configure the TypeDB Cluster and interact with a TypeDB Cluster knowledge graph via the TypeDB Console.
