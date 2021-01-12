---
pageTitle: Install and Run Grakn
keywords: setup, getting started, grakn, download, install, server, linux, mac, windows, docker
longTailKeywords: grakn on linux, grakn on mac, grakn on windows, start grakn server
summary: Install and run the Grakn Server on Linux, Mac or Windows.
toc: false
---

## System Requirements
Grakn runs on Mac, Linux and Windows. The only requirement is Java 8 which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).

## Download and Install Grakn

<div class="tabs light">
[tab:Linux]
  
#### Using RPM/DNF

As a superuser, add the repo:
```
sudo dnf config-manager --add-repo https://repo.grakn.ai/repository/meta/rpm.repo
```

Install Grakn Server and Grakn Console:
```
sudo dnf install grakn-core-all
```


#### Using RPM/Yum

As a superuser, add the repo:
```
sudo yum-config-manager --add-repo https://repo.grakn.ai/repository/meta/rpm.repo
```

Update the package cache:
```
sudo yum update
```

Install Grakn Server and Grakn Console:
```
sudo yum install grakn-core-all
```

#### Using APT

As a superuser, add the repo:
```
sudo apt install software-properties-common apt-transport-https
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 8F3DA4B5E9AEF44C
sudo add-apt-repository 'deb [ arch=all ] https://repo.grakn.ai/repository/apt/ trusty main'
```

Update the package cache:
```
sudo apt update
```

Install Grakn Server and Grakn Console:
```
sudo apt install grakn-core-all
```

#### Manual Download

Download the [latest release](https://grakn.ai/download?os=linux#core), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](../02-running-grakn/02-console.md).

[tab:end]

[tab:Mac OS X]

#### Using Homebrew
```
brew tap graknlabs/tap
brew install graknlabs/tap/grakn-core
```

To upgrade an existing installation via brew:
```
brew upgrade graknlabs/tap/grakn-core
```

#### Manual Download
Download the [latest release](https://grakn.ai/download?os=mac_os_x#core), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](../02-running-grakn/02-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://grakn.ai/download?os=windows#core), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](../02-running-grakn/02-console.md).

[tab:end]


[tab:Docker]

#### Using Docker

To pull the Grakn Docker image, run:

```
docker pull graknlabs/grakn:latest
```

#### Without an External Volume

For testing purposes, run:
```
docker run --name grakn -d -p 1729:1729 graknlabs/grakn:latest
```

<div class="note">
[Warning]
Running the instance without specifying a volume does NOT save the data if the instance is killed.
</div>

#### With an External Volume

To ensure that data is preserved even when the instance is killed or restarted, run:

```
docker run --name grakn -d -v $(pwd)/db/:/grakn-core-all-linux/server/db/ -p 1729:1729 graknlabs/grakn:latest
```

Having started the instance, the Grakn Server is expected to be running on port `1729` on your machine.

To interact with the [Grakn Console](../02-running-grakn/02-console.md), run:

```
docker exec -ti grakn bash -c '/opt/grakn-core-all-linux/grakn console'
```
[tab:end]
</div>

## Start the Grakn Server
If you have installed Grakn using a package manager, to start the Grakn Server, run `grakn server`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server`.

## Stop the Grakn Server
To stop the Grakn Server, press Ctrl-C in same terminal as the one where you started it in.


## Summary
So far we have learned how to download/install Grakn and run the Grakn Server.

Next, we learn how to [configure the Grakn Server](../02-running-grakn/03-configuration.md) and [interact with a Grakn knowledge graph via the Grakn Console](../02-running-grakn/02-console.md).
