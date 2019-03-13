---
sidebarTitle: Install & Run
pageTitle: Install and Run Grakn
permalink: /docs/running-grakn/install-and-run
toc: false
---

## System Requirements
Grakn runs on Mac, Linux and Windows. The only requirement is Java 8 which can be downloaded from [OpenJDK](http://openjdk.java.net/install/) or [Oracle Java](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).


## Download and Install Grakn
<div class="tabs light">
[tab:Mac OS X]

### To download the latest release
#### Using Homebrew
```
$ brew install grakn
```
#### Manual Download
Download the [latest release](https://grakn.ai/download?os=mac_os_x#core), unzip it in a location on your machine that is easily accessible via terminal.

Having downloaded Grakn, we can now interact with the [Grakn server](#start-the-grakn-server) and the [Graql console](/docs/running-grakn/console).
[tab:end]

[tab:CentOS]

### To download the latest release

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

Having installed Grakn, we can now interact with the [Grakn server](#start-the-grakn-server) and the [Graql console](/docs/running-grakn/console).

[tab:end]

[tab:Ubuntu]

### To download the latest release

As a superuser, add the repo:
```
sudo bash <<EOF
echo "deb [ arch=all ] https://repo.grakn.ai/repository/deb/ trusty main" >> /etc/apt/sources.list.d/grakn-core.list
apt-key adv --keyserver keyserver.ubuntu.com --recv 8F3DA4B5E9AEF44C
EOF
```

Update the package cache:
```
# apt update
```

Install Grakn Server and Grakn Console:
```
# apt install grakn-core-server grakn-core-console
```

Having installed Grakn, we can now interact with the [Grakn server](#start-the-grakn-server) and the [Graql console](/docs/running-grakn/console).

[tab:end]

[tab:Docker]

Run :
```
$ docker run -d -p 48555:48555 graknlabs/grakn
```


Having started Grakn, we can now interact with the [Grakn server](#start-the-grakn-server) and the [Graql console](/docs/running-grakn/console).

[tab:end]

[tab:Linux]

### To download the latest release
Download the [latest release](https://grakn.ai/download?os=linux#core), unzip it in a location on your machine that is easily accessible via terminal.

Having downloaded Grakn, we can now interact with the [Grakn server](#start-the-grakn-server) and the [Graql console](/docs/running-grakn/console).

[tab:end]

[tab:Windows]

### To download the latest release
Download the [latest release](https://grakn.ai/download?os=windows#core), unzip it in a location on your machine that is easily accessible via command prompt.

Having downloaded Grakn, we can now interact with the [Grakn server](#start-the-grakn-server) and the [Graql console](/docs/running-grakn/console).

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