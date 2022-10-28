---
pageTitle: Install and Run TypeDB Cluster
keywords: setup, getting started, typedb, download, install, server, linux, mac, windows, docker
longTailKeywords: typedb cluster on linux, typedb cluster on mac, typedb cluster on windows, start typedb cluster, run typedb cluster
summary: Install and run the TypeDB Cluster on Linux, Mac or Windows.
toc: false
---

## Obtaining Commercial License

TypeDB Cluster is a commercial offering that provides a production-grade experience - high-availability, scalability, and security. A license can be obtained from our [sales team](mailto:commercial@vaticle.com).

## System Requirements
TypeDB Cluster runs on macOS, Linux and Windows. The only requirement is Java (version 11 or higher) which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

## Download and Install TypeDB Cluster

<div class="tabs light">
[tab:Linux]

#### Manual Download

Download the [latest release](https://repo.vaticle.com/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via terminal.

#### Other package managers

If TypeDB Cluster doesn't have a distribution you need, please open an issue [on GitHub](https://github.com/vaticle/typedb/issues).

Having installed or downloaded TypeDB Cluster, we can now start the [Cluster](#starting-and-stopping-a-single-node-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:macOS]

#### Manual Download
Download the [latest release](https://repo.vaticle.com/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via a terminal.

Having installed or downloaded TypeDB, we can now start the [Server](#starting-and-stopping-a-single-node-cluster) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://repo.vaticle.com/#browse/browse:private-artifact), unzip it in a location on your machine that is easily accessible via a command prompt.

Having downloaded TypeDB, we can now start the [Server](#starting-and-stopping-a-single-node-cluster) and interact with the [Console](../02-console/01-console.md).

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

**NOTE:** Running the instance without specifying a volume does NOT save the data if the instance is killed.

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

## Starting and Stopping a single node Cluster

### Starting

If you have installed TypeDB using a package manager, to start the TypeDB Cluster, open a terminal and run `typedb cluster`.

Otherwise, if you have manually downloaded TypeDB, `cd` into the unzipped folder and run `./typedb cluster`.


### Stopping

To stop the TypeDB Cluster, press Ctrl+C in the terminal session you are running TypeDB Cluster from.


## Starting and Stopping a multi-node Cluster

### Starting

While it's possible to run TypeDB Cluster in a single-node mode, a truly highly-available and fault-tolerant
production-grade setup includes setting up multiple servers to connect and form a cluster. At any given point in time, one
of those servers acts as a leader and the others are followers. Increasing the number of nodes increases the Cluster's tolerance to
failure: to tolerate N nodes failing, Cluster needs to consist of 2*N+1 nodes.
This section describes how you can set up a 3-node cluster (in this case, one node can fail and no data is lost).

Each node binds to three ports: a client port which TypeDB client drivers connect to (`1729`), and two server ports (`1730` and `1731`) for server-to-server communication.

For this tutorial, it's assumed that all three nodes are on the same virtual network and have the relevant ports open and are
uninhibited by any firewall. The nodes have IP addresses `10.0.0.1`, `10.0.0.2` and `10.0.0.3` respectively.

<div class="note">
[Note]
If you're using a single machine to host all nodes, you can prefix the port with the node number; this way
the ports `1729`, `1730`, `1731` would turn into `11729`, `11730`, `11731`; `21729`, `21730`, `21731` and so on.
</div>

This is how 3-node TypeDB Cluster would be started on three separate machines.

```bash
# On 10.0.0.1:
$ ./typedb cluster \
    --server.address=10.0.0.1:1729 \
    --server.internal-address.zeromq=10.0.0.1:1730 \
    --server.internal-address.grpc=10.0.0.1:1731 \
    --server.peers.peer-1.address=10.0.0.1:1729 \
    --server.peers.peer-1.internal-address.zeromq=10.0.0.1:1730 \
    --server.peers.peer-1.internal-address.grpc=10.0.0.1:1731 \
    --server.peers.peer-2.address=10.0.0.2:1729 \
    --server.peers.peer-2.internal-address.zeromq=10.0.0.2:1730 \
    --server.peers.peer-2.internal-address.grpc=10.0.0.2:1731 \
    --server.peers.peer-3.address=10.0.0.3:1729 \
    --server.peers.peer-3.internal-address.zeromq=10.0.0.3:1730 \
    --server.peers.peer-3.internal-address.grpc=10.0.0.3:1731

# On 10.0.0.2:
$ ./typedb cluster \
    --server.address=10.0.0.2:1729 \
    --server.internal-address.zeromq=10.0.0.2:1730 \
    --server.internal-address.grpc=10.0.0.2:1731 \
    --server.peers.peer-1.address=10.0.0.1:11729 \
    --server.peers.peer-1.internal-address.zeromq=10.0.0.1:1730 \
    --server.peers.peer-1.internal-address.grpc=10.0.0.1:1731 \
    --server.peers.peer-2.address=10.0.0.2:1729 \
    --server.peers.peer-2.internal-address.zeromq=10.0.0.2:1730 \
    --server.peers.peer-2.internal-address.grpc=10.0.0.2:1731 \
    --server.peers.peer-3.address=10.0.0.3:1729 \
    --server.peers.peer-3.internal-address.zeromq=10.0.0.3:1730 \
    --server.peers.peer-3.internal-address.grpc=10.0.0.3:1731

# On 10.0.0.3:
$ ./typedb cluster \
    --server.address=10.0.0.3:1729 \
    --server.internal-address.zeromq=10.0.0.3:1730 \
    --server.internal-address.grpc=10.0.0.3:1731 \
    --server.peers.peer-1.address=10.0.0.1:1729 \
    --server.peers.peer-1.internal-address.zeromq=10.0.0.1:1730 \
    --server.peers.peer-1.internal-address.grpc=10.0.0.1:1731 \
    --server.peers.peer-2.address=10.0.0.2:1729 \
    --server.peers.peer-2.internal-address.zeromq=10.0.0.2:1730 \
    --server.peers.peer-2.internal-address.grpc=10.0.0.2:1731 \
    --server.peers.peer-3.address=10.0.0.3:1729 \
    --server.peers.peer-3.internal-address.zeromq=10.0.0.3:1730 \
    --server.peers.peer-3.internal-address.grpc=10.0.0.3:1731
```  

<div class="note">
[Note]
This guide assumes the application accessing TypeDB Cluster resides on the same private network. If this is *not* the case,
TypeDB Cluster also supports using different IP addresses for client and server communication. In order to do so, the
relevant external hostname should be passed as arguments using the `--server.address` and `--server.peers` flags as below.

```bash
$ ./typedb cluster \
    --server.address=external-host-1:1729 \
    --server.internal-address.zeromq=10.0.0.1:1730 \
    --server.internal-address.grpc=10.0.0.1:1731 \
    --server.peers.peer-1.address=external-host-1:1729 \
    --server.peers.peer-1.internal-address.zeromq=10.0.0.1:1730 \
    --server.peers.peer-1.internal-address.grpc=10.0.0.1:1731 \
    --server.peers.peer-2.address=external-host-2:1729 \
    --server.peers.peer-2.internal-address.zeromq=10.0.0.2:1730 \
    --server.peers.peer-2.internal-address.grpc=10.0.0.2:1731 \
    --server.peers.peer-3.address=external-host-3:1729 \
    --server.peers.peer-3.internal-address.zeromq=10.0.0.3:1730 \
    --server.peers.peer-3.internal-address.grpc=10.0.0.3:1731
```
and so on.

In this case, port `1729` would need to be open to public and clients would use the
`external-host-1`, `external-host-2` and `external-host-3` hostnames to communicate with TypeDB Cluster;
inter-server communication would be done over a private network using ports `1730` and `1731`.
</div>

### Stopping

Stopping TypeDB Cluster is done the same way as on a single node: pressing Ctrl+C in the terminal that was used to start it.
All nodes must be shut down independently in the same way.

## Summary
So far we have learned how to download, install and run TypeDB Cluster in an ad-hoc way. 

Next, we'll learn how to deploy TypeDB Cluster using Kubernetes and Helm.
