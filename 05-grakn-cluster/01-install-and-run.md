---
pageTitle: Install and Run Grakn Cluster
keywords: setup, getting started, grakn, download, install, server, linux, mac, windows, docker
longTailKeywords: grakn on linux, grakn on mac, grakn on windows, start grakn cluster
summary: Install and run the Grakn Cluster on Linux, Mac or Windows.
toc: false
---

## System Requirements
Grakn Cluster runs on Mac, Linux and Windows. The only requirement is Java 8 or higher which can be downloaded from [OpenJDK](https://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).

## Download and Install Grakn Cluster

<div class="tabs light">
[tab:Linux]

#### Manual Download

Download the [latest release](https://repo.grakn.ai/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via terminal.

#### Other package managers

If Grakn Cluster doesn't have a distribution you need, please open an issue [on GitHub](https://github.com/graknlabs/grakn/issues).


Having installed or downloaded Grakn Cluster, we can now start the [Cluster](#start-the-grakn-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Mac OS X]

#### Manual Download
Download the [latest release](https://repo.grakn.ai/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://repo.grakn.ai/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded Grakn, we can now start the [Server](#start-the-grakn-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]


[tab:Docker]

#### Using Docker

To pull the Grakn Docker image, run:

```
docker pull graknlabs/grakn-cluster:latest
```

#### Without an External Volume

For testing purposes, run:
```
docker run --name grakn -d -p 1729:1729 graknlabs/grakn-cluster:latest
```

<div class="note">
[Warning]
Running the instance without specifying a volume does NOT save the data if the instance is killed.
</div>

#### With an External Volume

To ensure that data is preserved even when the instance is killed or restarted, run:

```
docker run --name grakn -d -v $(pwd)/db/:/opt/grakn-cluster-all-linux/server/db/ -p 1729:1729 graknlabs/grakn-cluster:latest
```

Having started the instance, the Grakn Cluster is expected to be running on port `1729` on your machine.

To interact with the [Grakn Console](../02-console/01-console.md), run:

```
docker exec -ti grakn bash -c '/opt/grakn-cluster-all-linux/grakn console'
```
[tab:end]
</div>

## Starting and Stopping Single-node Cluster

### Starting

If you have installed Grakn using a package manager, to start the Grakn Cluster, run `grakn server`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server`.


### Stopping

To stop the Grakn Cluster, press Ctrl-C in same terminal as the one where you started it in.


## Starting and Stopping Multi-node Cluster

### Starting

While it's possible to run Grakn Cluster in a single-node mode, a truly highly-available and fault-tolerant
production-grade setup includes setting up multiple servers to connect and form a cluster. At every time, one
of those servers acts as a leader and others are followers. Increasing number of nodes increases tolerance to
failure: to tolerate N nodes failing, cluster needs to consist of 2*N+1 nodes.
This section describes how it's done on an example 3-node setup (in this case, one node can fail and no data is lost).

Each node binds to two ports: a client port which Grakn client drivers connect to (`1729`), and a server port (`1730`)
which is used for inter-node server-to-server communication.

For the tutorial, it's assumed that all three nodes are on the same virtual network and have relevant ports
unblocked by the firewall. Node have IP addresses of `10.0.0.1`, `10.0.0.2` and `10.0.0.3` and hostnames of
`node1`, `node2` and `node3`.

<div class="note">
[Note]
If you're using a single machine to host all nodes, you can prefix the port with the node number; this way
`1729` and `1730` would turn into `11729`, `11730`; `21729`, `21730` and so on.
</div>

This is how Grakn Cluster would be started:

```bash
user@node1:~/grakn-cluster/$ ./grakn server --address=10.0.0.1:1729:1730 --peer 10.0.0.1:1729:1730 --peer 10.0.0.2:1729:1730 --peer 10.0.0.3:1729:1730

user@node2:~/grakn-cluster/$ ./grakn server --address=10.0.0.2:1729:1730 --peer 10.0.0.1:1729:1730 --peer 10.0.0.2:1729:1730 --peer 10.0.0.3:1729:1730

user@node3:~/grakn-cluster/$ ./grakn server --address=10.0.0.3:1729:1730 --peer 10.0.0.1:1729:1730 --peer 10.0.0.2:1729:1730 --peer 10.0.0.3:1729:1730
```  

<div class="note">
[Note]
This guide assumes application accessing Grakn Cluster resides on the same private network. If this is *not* the case,
Grakn Cluster also supports using different IP addresses for client and server communication. In order to do that client
and server addresses need to be passed separated by a comma to `--address` and `--peer` options:

```
./grakn server \
    --address external-host-1:1729,10.0.0.1:1730 \
    --peer external-host-1:1729,10.0.0.1:1730 \
    --peer external-host-2:1729,10.0.0.2:1730 \
    --peer external-host-3:1729,10.0.0.3:1730`
```

In this case, port `1729` would need to be open to public and clients would use
`external-host-1`, `external-host-2` and `external-host-3` hostname to communicate with Grakn Cluster;
inter-server communication would be done over private network using port `1730`.
</div>

### Stopping

Stopping the Grakn Cluster is done the same way as with single node: pressing Ctrl+C in the terminal that was used to start it.
All nodes would be to be shut down independently.

## Summary
So far we have learned how to download, install and run the Grakn Cluster.

Next, we learn how to configure the Grakn Cluster and interact with a Grakn Cluster knowledge graph via the Grakn Console.
