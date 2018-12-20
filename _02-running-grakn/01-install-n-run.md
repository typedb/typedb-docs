---
sidebarTitle: Install & Run
pageTitle: Install and Run Grakn
keywords:
tags: []
summary: ""
permalink: /docs/running-grakn/install-n-run
---

## System Requirements
Grakn runs on Mac, Linux and Windows. The only requirement is Java 8 which can be downloaded from [OpenJDK](http://openjdk.java.net/install/){:target="_blank"} or [Oracle Java](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html){:target="_blank"}.


## Download and Install Grakn
<div class="gtabs light">
[tab:Mac OS X]

### To download the latest release
#### Using Homebrew
```
brew install grakn
```
#### Manual Download
Download the [latest 1.4.2 release](https://github.com/graknlabs/grakn/releases/download/v1.4.2/grakn-core-1.4.2.zip), unzip it in a location on your machine that is easily accessible via terminal.

Having downloaded Grakn, we can now interact with the [Grakn server](#starting-the-grakn-server) and the [Graql console](/docs/install-n-run/console).

### To download an older version
Refer to the [Grakn releases on Github](https://github.com/graknlabs/grakn/releases) to download a previous version of Grakn.

<div class="galert">
[Warning]
Take into account that many features of previous versions are deprecated and so no longer supported.
</div>

[tab:end]

[tab:Linux]

### To download the latest release
Download the [latest 1.4.2 release](https://github.com/graknlabs/grakn/releases/download/v1.4.2/grakn-core-1.4.2.zip), unzip it in a location on your machine that is easily accessible via terminal.

Having downloaded Grakn, we can now interact with the [Grakn server](#starting-the-grakn-server) and the [Graql console](/docs/install-n-run/console).

### To download an older version
Refer to the [Grakn releases on Github](https://github.com/graknlabs/grakn/releases) to download a previous version of Grakn.

<div class="galert">
[Warning]
Take into account that many features of previous versions are deprecated and so no longer supported.
</div>

[tab:end]

[tab:Windows]

### To download the latest release
Download the [latest 1.4.2 release](https://github.com/graknlabs/grakn/releases/download/v1.4.2/grakn-core-1.4.2.zip), unzip it in a location on your machine that is easily accessible via terminal.

Having downloaded Grakn, we can now interact with the [Grakn server](#starting-the-grakn-server) and the [Graql console](/docs/install-n-run/console).

### To download an older version
Refer to the [Grakn releases on Github](https://github.com/graknlabs/grakn/releases) to download a previous version of Grakn.

<div class="galert">
[Warning]
Take into account that many features of previous versions are deprecated and so no longer supported.
</div>

[tab:end]
</div>

## Start the Grakn Server
If you have installed Grakn using Homebrew, to start the Grakn Server, run `grakn server start`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server start`.

## Stop the Gran Server
If you have installed Grakn using Homebrew, to stop the Grakn Server, run `grakn server stop`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server stop`.

## Check the Server Status
If you have installed Grakn using Homebrew, to check the status of the Grakn Server, run `grakn server status`.

Otherwise, if you have manually downloaded Grakn, `cd` into the unzipped folder and run `./grakn server status`.

## Summary
So far we have learned how to download/install Grakn and run the Grakn Server.

Next, we will find about how to [configure the Grakn Server](/docs/running-grakn/configuration) and [interact with a Grakn knowledge graph via the Graql Console](/docs/running-grakn/console).