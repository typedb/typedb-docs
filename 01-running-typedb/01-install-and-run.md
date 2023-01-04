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
sudo gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 8F3DA4B5E9AEF44C 
sudo gpg --export 8F3DA4B5E9AEF44C | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null
echo "deb [ arch=all ] https://repo.vaticle.com/repository/apt/ trusty main" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null
```

Update the package cache:
```
sudo apt update
```

Install TypeDB Server and TypeDB Console:
```
sudo apt install typedb-all
```
  
#### APT conflicts

APT will always try to install the latest version of all dependencies that a package depends on. TypeDB's release strategy allows
depended upon packages (such as `typedb-bin`) to be released faster than TypeDB itself to facilitate feature upgrades.
  
In these situations, you will encounter the following type of errors:

```
> sudo apt-get install typedb-all=2.11.0
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies.
typedb-all : Depends: typedb-server (= 2.11.0) but it is not going to be installed
```

To solve this, specify each of the depended upon packages by exact version as well:
```
> sudo apt-get install typedb-all=2.11.0 typedb-server=2.11.0
```
 
This command would produce a similar error, but requiring that `typedb-bin=2.9.0`. We try again
```
> sudo apt-get install typedb-all=2.11.0 typedb-server=2.11.0 typedb-bin=2.9.0
```

Which successfully installs all required packages for `typedb-all=2.11.0`.
  
#### Manual Download

Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via terminal.

#### Other package managers

If TypeDB doesn't have a distribution you need, please open an issue [on GitHub](https://github.com/vaticle/typedb/issues).


Having installed or downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:macOS]

#### Using Homebrew
```sh
brew install typedb
```

To upgrade an existing installation via brew:
```sh
brew upgrade typedb
```

#### Manual Download
Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the [Console](../02-console/01-console.md).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the [Console](../02-console/01-console.md).

**NOTE**: If you are experiencing the following error,

```
Exception in thread "main" java.lang.UnsatisfiedLinkError: 
C:\Users\Vaticle\AppData\Local\Temp\ortools-java\win32-x86-64\jniortools.dll: Can't find dependent libraries
```

please try to install the "C++ redistributable" by following the instructions [here](https://developers.google.com/optimization/install/python/windows#microsoft-visual-c-redistributable).

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

**NOTE**: Running the instance without specifying a volume does NOT save the data if the instance is killed.

#### With an External Volume

To ensure that data is preserved even when the instance is killed or restarted, mount an external volume:

```
docker run --name typedb -d -v {external-volume}:/opt/typedb-all-linux/server/data/ -p 1729:1729 vaticle/typedb:latest
```

`{external-volume}` should be configured to where you want the data to be stored in the host machine.

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

This command will run in the foreground of your current terminal, so to do other operations such as using console, it's best to use another terminal.

## Stop the TypeDB Server
To stop the TypeDB Server, press Ctrl-C in same terminal as the one where you started it in.


## Summary
So far we have learned how to download/install TypeDB and run the TypeDB Server.

Next, we learn how to [configure the TypeDB Server](../01-running-typedb/03-configuration.md) and [interact with a TypeDB knowledge graph via the TypeDB Console](../02-console/01-console.md).
