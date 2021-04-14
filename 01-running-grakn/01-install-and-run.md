---
pageTitle: Install and Run Grakn
keywords: setup, getting started, grakn, download, install, server, linux, mac, windows, docker
longTailKeywords: grakn on linux, grakn on mac, grakn on windows, start grakn server
summary: Install and run the Grakn Server on Linux, Mac or Windows.
toc: false
---

## System Requirements
Grakn runs on Mac, Linux and Windows. The only requirement is Java (version 11 or higher) which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

<div class="note">
[Warning]
If upgrading from Grakn 1.8, please note that Java 8 is **no longer supported in 2.0.** You should upgrade to the latest version of Java in order to use Grakn 2.0.
</div>

## Download and Install Grakn

<div class="tabs light">
[tab:Linux]

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

<div class="note">
[Warning]
Ubuntu 16.04 requires some extra steps to be able to install Grakn Core, namely upgrading `libstdc++`:

```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-4.9
sudo apt-get install --only-upgrade libstdc++6
```
</div>

#### Manual Download

Download the [latest release](https://github.com/graknlabs/grakn/releases), unzip it in a location on your machine that is easily accessible via terminal.

#### Other package managers

If Grakn Core doesn't have a distribution you need, please open an issue [on GitHub](https://github.com/graknlabs/grakn/issues).


Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](../02-console/01-console.md).

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
Download the [latest release](https://github.com/graknlabs/grakn/releases), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://github.com/graknlabs/grakn/releases), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](../02-console/01-console.md).

If you see errors such as the following:
```
Exception in thread "main" java.lang.UnsatisfiedLinkError: 
C:\Users\graknlabs\AppData\Local\Temp\ortools-java\win32-x86-64\jniortools.dll: Can't find dependent libraries
```
try following the C++ redistributable installation instructions [here](https://developers.google.com/optimization/install/python/windows#microsoft-visual-c-redistributable).

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

To interact with the [Grakn Console](../02-console/01-console.md), run:

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

Next, we learn how to [configure the Grakn Server](../01-running-grakn/03-configuration.md) and [interact with a Grakn knowledge graph via the Grakn Console](../02-console/01-console.md).
