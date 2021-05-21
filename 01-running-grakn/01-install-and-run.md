---
pageTitle: Install and Run TypeDB
keywords: setup, getting started, typedb, download, install, server, linux, mac, windows, docker
longTailKeywords: typedb on linux, typedb on mac, typedb on windows, start typedb server
summary: Install and run the TypeDB Server on Linux, Mac or Windows.
toc: false
---

## System Requirements
TypeDB runs on Mac, Linux and Windows. The only requirement is Java (version 11 or higher) which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

## Download and Install TypeDB

<div class="tabs light">
[tab:Linux]

#### Using APT

As a superuser, add the repo:
```
sudo apt install software-properties-common apt-transport-https
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 8F3DA4B5E9AEF44C
sudo add-apt-repository 'deb [ arch=all ] https://repo.vaticle.com/repository/apt/ trusty main'
```

Update the package cache:
```
sudo apt update
```

Install TypeDB Server and TypeDB Console:
```
sudo apt install typedb-all
```

<div class="note">
[Warning]
Ubuntu 16.04 requires some extra steps to be able to install TypeDB, namely upgrading `libstdc++`:

```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-4.9
sudo apt-get install --only-upgrade libstdc++6
```
</div>

#### Manual Download

Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via terminal.

#### Other package managers

If TypeDB doesn't have a distribution you need, please open an issue [on GitHub](https://github.com/vaticle/typedb/issues).


Having installed or downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Mac OS X]

#### Using Homebrew
```
brew tap vaticle/tap
brew install vaticle/tap/typedb
```

To upgrade an existing installation via brew:
```
brew upgrade vaticle/tap/typedb
```

#### Manual Download
Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the [Console](../02-console/01-console.md).

If you see errors such as the following:
```
Exception in thread "main" java.lang.UnsatisfiedLinkError: 
C:\Users\Vaticle\AppData\Local\Temp\ortools-java\win32-x86-64\jniortools.dll: Can't find dependent libraries
```
try following the C++ redistributable installation instructions [here](https://developers.google.com/optimization/install/python/windows#microsoft-visual-c-redistributable).

[tab:end]


[tab:Docker]

#### Using Docker

To pull the TypeDB Docker image, run:

```
docker pull vaticle/typedb:latest
```

#### Without an External Volume

For testing purposes, run:
```
docker run --name typedb -d -p 1729:1729 vaticle/typedb:latest
```

<div class="note">
[Warning]
Running the instance without specifying a volume does NOT save the data if the instance is killed.
</div>

#### With an External Volume

To ensure that data is preserved even when the instance is killed or restarted, run:

```
docker run --name typedb -d -v $(pwd)/db/:/typedb-all-linux/server/db/ -p 1729:1729 vaticle/typedb:latest
```

Having started the instance, the TypeDB Server is expected to be running on port `1729` on your machine.

To interact with the [TypeDB Console](../02-console/01-console.md), run:

```
docker exec -ti typedb bash -c '/opt/typedb-all-linux/typedb console'
```
[tab:end]
</div>

## Start the TypeDB Server
If you have installed TypeDB using a package manager, to start the TypeDB Server, run `typedb server`.

Otherwise, if you have manually downloaded TypeDB, `cd` into the unzipped folder and run `./typedb server`.

## Stop the TypeDB Server
To stop the TypeDB Server, press Ctrl-C in same terminal as the one where you started it in.


## Summary
So far we have learned how to download/install TypeDB and run the TypeDB Server.

Next, we learn how to [configure the TypeDB Server](../01-running-typedb/03-configuration.md) and [interact with a TypeDB knowledge graph via the TypeDB Console](../02-console/01-console.md).
