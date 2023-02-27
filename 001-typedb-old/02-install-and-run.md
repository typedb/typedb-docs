---
pageTitle: Install and Run TypeDB
keywords: setup, getting started, typedb, download, install, server, linux, mac, windows, docker
longTailKeywords: typedb on linux, typedb on mac, typedb on windows, start typedb server
summary: Install and run the TypeDB Server on Linux, Mac or Windows.
toc: true
---

# Install and Run

<!---
List: 
- Prerequisites, [√]
- Installation on windows/mac/linux/docker, [√]
- starting TypeDB (esp note that will run in foreground of terminal) [√]
-->

## Prerequisites

TypeDB runs on:
- Linux 
- MacOS
- Windows

The only requirement is Java (**version 11** or higher) which can be downloaded from 
[OpenJDK](http://openjdk.java.net/install/) or 
[Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

## Download and Install TypeDB

<div class="tabs light">

[tab:Docker]

Use `docker run` to download an image `vaticle/typedb` and run a container with it. To ensure that data is preserved
even when the instance is killed or restarted, mount an external volume to your Docker container:

```
docker run --name typedb -d -v ~/typedb:/opt/typedb-all-linux/server/data/ -p 1729:1729 vaticle/typedb:latest
```

`~/typedb` — should be a location where you want the data to be stored in the host machine.

`vaticle/typedb:latest` — is the image name. You can change `latest` for any version you might need. We recommend using
TypeDB and TypeDB Studio of the same versions.

The TypeDB Server is expected to be running on port `1729` on your machine in a docker container.

You can connect to this instance with TypeDB Studio or any other instrument via address `127.0.0.1:1729`.
To interact with the local [TypeDB Console](../02-console/01-console.md), run:

```
docker exec -ti typedb bash -c '/opt/typedb-all-linux/typedb console'
```
[tab:end]

[tab:Linux]

#### Using package manager, like APT

As a superuser, add the repo:
```
sudo apt install software-properties-common apt-transport-https gpg
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 8F3DA4B5E9AEF44C 
gpg --export 8F3DA4B5E9AEF44C | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null
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
depended upon packages (such as `typedb-bin`) to be released slower than TypeDB itself to facilitate feature upgrades. For example, `typedb-all` 2.11 requires `typedb-bin` version 2.9.

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

Download the [latest release](https://github.com/vaticle/typedb/releases), unzip it in a location on your machine that 
is easily accessible via terminal.

#### Other package managers

If TypeDB doesn't have a distribution you need, please open an issue 
[on GitHub](https://github.com/vaticle/typedb/issues).

Having installed or downloaded TypeDB, we can now start the [Server](#start-the-typedb-server) and interact with the 
[Console](../02-console/01-console.md).

[tab:end]

[tab:MacOS]

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

</div>

## Start the TypeDB Server
If you have installed TypeDB using a package manager, to start the TypeDB Server, run `typedb server`.

Otherwise, if you have manually downloaded TypeDB, navigate into the folder with unzipped TypeDB and run it by issuing
`./typedb server` command.

If you have used the docker way TypeDB should work while the docker container is active.

<div class="note">
[Note]
Command `typedb server` will run in the foreground of your current terminal, so to do other operations such as using 
TypeDB Console, it's best to use another terminal. Closing the terminal where the TypeDB server is running will result 
in termination of the program.
</div>

## Stop the TypeDB Server
To stop the TypeDB Server, press Ctrl-C in the terminal, where you started it in.

If you have used docker — stop the container.
