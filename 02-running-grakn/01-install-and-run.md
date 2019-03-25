---
pageTitle: Install and Run Grakn
keywords: setup, getting started, grakn, download, install, server, linux, mac, windows
longTailKeywords: grakn on linux, grakn on mac, grakn on windows, start grakn server
summary: Install and run the Grakn Server on Linux, Mac or Windows.
toc: false
permalink: /docs/running-grakn/install-and-run
---

## System Requirements
Grakn runs on Mac, Linux and Windows. The only requirement is Java 8 which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).

## Download and Install Grakn
<div class="tabs light">
[tab:Linux]

#### Using RPM/Yum

As a superuser, add the repo:
```
# yum-config-manager --add-repo https://repo.grakn.ai/repository/meta/grakn-core.repo
```

Update the package cache:
```
# yum update
```

Install Grakn Server and Grakn Console:
```
# yum install grakn-core-server grakn-core-console
```

#### Using Debian

As a superuser, add the repo:
```
sudo apt install software-properties-common
sudo add-apt-repository 'deb [ arch=all ] https://repo.grakn.ai/repository/deb/ trusty main'
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 8F3DA4B5E9AEF44C
```

Update the package cache:
```
# apt update
```

Install Grakn Server and Grakn Console:
```
# apt install grakn-core-server grakn-core-console
```

#### Manual Download

Download the [latest release](https://grakn.ai/download?os=linux#core), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](/docs/running-grakn/console).

[tab:end]

[tab:Mac OS X]

#### Using Homebrew
```
$ brew tap graknlabs/tap
$ brew tap-pin graknlabs/tap
$ brew install grakn-core
```

#### Manual Download
Download the [latest release](https://grakn.ai/download?os=mac_os_x#core), unzip it in a location on your machine that is easily accessible via terminal.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](/docs/running-grakn/console).

[tab:end]

[tab:Windows]

#### Manual Download
Download the [latest release](https://grakn.ai/download?os=windows#core), unzip it in a location on your machine that is easily accessible via command prompt.

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](/docs/running-grakn/console).

[tab:end]


[tab:Docker]

Run :
```
$ docker run -d -p 48555:48555 graknlabs/grakn
```

Having installed or downloaded Grakn, we can now start the [Server](#start-the-grakn-server) and interact with the [Console](/docs/running-grakn/console).

[tab:end]
</div>

## Start the Grakn Server
If you have installed Grakn using Homebrew, to start the Grakn Server, run `grakn server start`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server start`.

## Stop the Grakn Server
If you have installed Grakn using Homebrew, to stop the Grakn Server, run `grakn server stop`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server stop`.

## Check the Server Status
If you have installed Grakn using Homebrew, to check the status of the Grakn Server, run `grakn server status`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server status`.

## Summary
So far we have learned how to download/install Grakn and run the Grakn Server.

Next, we learn how to [configure the Grakn Server](/docs/running-grakn/configuration) and [interact with a Grakn knowledge graph via the Grakn Console](/docs/running-grakn/console).