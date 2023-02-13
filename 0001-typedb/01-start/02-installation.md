---
pageTitle: Installation
keywords: setup, getting started, typedb, download, install, server, linux, mac, windows, docker
longTailKeywords: typedb on linux, typedb on mac, typedb on windows, start typedb server
summary: Install and run the TypeDB Server on Linux, Mac or Windows.
toc: false
---

# Installation

<div class="tabs light">

[tab:Docker]

Use `docker run` to download an image `vaticle/typedb` and run a container with it. To ensure that data is preserved
even when the instance is killed or restarted, mount an external volume to your Docker container:

```
docker run --name try-typedb -d -v /opt/typedb-all-linux/server/data/ -p 1729:1729 vaticle/typedb:latest
```

`vaticle/typedb:latest` — is the image name. You can change `latest` for any version you might need. We recommend using
TypeDB and TypeDB Studio of the same versions.

The TypeDB Server is expected to be running on port `1729` on your machine in a docker container.

You can connect to this instance with TypeDB Studio or any other instrument via address `127.0.0.1:1729`.
To interact with the local [TypeDB Console](../../02-clients/01-studio.md), run:

```
docker exec -ti typedb bash -c '/opt/typedb-all-linux/typedb console'
```

## Start the TypeDB Server

TypeDB server should work while the Docker container is active.

## Stop the TypeDB Server

To stop the TypeDB server you can stop the container.

[tab:end]

[tab:Linux]

## Using APT

### Add the repository

```
sudo apt install software-properties-common apt-transport-https gpg
gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 8F3DA4B5E9AEF44C 
gpg --export 8F3DA4B5E9AEF44C | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null
echo "deb [ arch=all ] https://repo.vaticle.com/repository/apt/ trusty main" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null
```

### Update the package cache

```
sudo apt update
```

### Install

```
sudo apt install typedb-all
```

<div class="note">
[Note]
The typed-all package installs typedb-bin, typedb-consol, typedb-server and openjdk-11-jre.
</div>

<div class="note">
[Note]
APT will always try to install the latest version of all dependencies that a package depends on. TypeDB's release 
strategy allows depended upon packages (such as `typedb-bin`) to be released faster than TypeDB itself to facilitate 
feature upgrades.

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
</div>
  
## Manual Installation

### Prerequisites

The only requirement is Java (**version 11** or higher) which can be downloaded from
[OpenJDK](http://openjdk.java.net/install/) or
[Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

### Download

Download the [latest release](https://vaticle.com/download#typedb) of TypeDB.

### Extract

Copy the archive to any desired location and extract the downloaded archive:

```bash
tar -xzf typedb-all-linux-x.yy.z.tar.gz
```

`typedb-all-linux-x.yy.z.tar.gz` — this shall be substituted with the exact name of the archive you've downloaded.

### Update PATH environment variable

To be able to launch TypeDB from anywhere without addressing the full path to the bin file we should set the 
environment variable `PATH` to look for bin file in the extracted folder. To do so we can run:

```bash
export PATH=$PATH:/path/to/dir
```

`/path/to/dir` — is the path to and the name of the extracted folder. There should be a `typedb` file at that location.

### Other package managers

If TypeDB doesn't have a distribution you need, please open an issue 
[on GitHub](https://github.com/vaticle/typedb/issues).

## Start the TypeDB Server

Now we can start the TypeDB Server by using the `typedb server` command in local terminal.

<div class="note">
[Note]
Command `typedb server` will run in the foreground of your current terminal, so to do other operations such as using 
TypeDB Console, it's best to use another terminal. Closing the terminal where the TypeDB server is running will result 
in termination of the program.
</div>

## Stop the TypeDB Server

To stop the TypeDB Server, press Ctrl-C in the terminal, where you started it in.

[tab:end]

[tab:MacOS]

## Homebrew

Install [Homebrew](https://brew.sh/).

Use Homebrew to install typedb:

```sh
brew install typedb
```

## Manual Install

### Prerequisites

The only requirement is Java (**version 11** or higher) which can be downloaded from
[OpenJDK](http://openjdk.java.net/install/) or
[Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

### Download

Download the [latest release](https://vaticle.com/download#typedb) of TypeDB.

### Extract

Copy the archive to any desired location and extract the downloaded archive by double clicking on it.

### Update PATH environment variable

To be able to launch TypeDB from anywhere without addressing the full path to the bin file we should set the
environment variable `PATH` to look for bin file in the extracted folder. To do so we can edit the `~/.zshrc` file 
in any available editor to add this text as a separate line at the end:

```bash
export PATH=$PATH:/path/to/dir
```

`/path/to/dir` — is the path to and the name of the extracted folder. There should be a `typedb` file at that location.

## Start the TypeDB Server

Now we can start the TypeDB Server by using the `typedb server` command in local terminal.

<div class="note">
[Note]
Command `typedb server` will run in the foreground of your current terminal, so to do other operations such as using 
TypeDB Console, it's best to use another terminal. Closing the terminal where the TypeDB server is running will result 
in termination of the program.
</div>

## Stop the TypeDB Server

To stop the TypeDB Server, press Ctrl-C in the terminal, where you started it in.

[tab:end]

[tab:Windows]

## Manual Install

### Prerequisites

The only requirement is Java (**version 11** or higher) which can be downloaded from
[OpenJDK](http://openjdk.java.net/install/) or
[Oracle Java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html).

### Download

Download the [latest release](https://vaticle.com/download#typedb) of TypeDB.

### Extract

Copy the archive to any desired location and extract the downloaded archive.

### Update PATH environment variable

To be able to launch TypeDB from anywhere without addressing the full path to the bin file we should set the
environment variable `PATH` to look for bin file in the extracted folder. To do so we can use GUI or console. 

For instructions on how to do it with GUI — follow [these instructions](https://www.java.com/en/download/help/path.html) 
minding the OS version. 

For console approach run:

```powershell
setx /M path "%path%;C:\path\to\dir"
```

`C:\path\to\dir` — is the path to and the name of the extracted folder. There should be a `typedb` file at that 
location.

<div class="note">
[Note]
If the following error occurs, please try to install the "C++ redistributable" by following the instructions 
[here](https://developers.google.com/optimization/install/python/windows#microsoft-visual-c-redistributable).

```
Exception in thread "main" java.lang.UnsatisfiedLinkError: 
C:\Users\Vaticle\AppData\Local\Temp\ortools-java\win32-x86-64\jniortools.dll: Can't find dependent libraries
```

## Start the TypeDB Server

Now we can start the TypeDB Server by using the `typedb server` command in local terminal.

<div class="note">
[Note]
Command `typedb server` will run in the foreground of your current terminal, so to do other operations such as using 
TypeDB Console, it's best to use another terminal. Closing the terminal where the TypeDB server is running will result 
in termination of the program.
</div>

## Stop the TypeDB Server

To stop the TypeDB Server, press Ctrl-C in the terminal, where you started it in.

</div>

[tab:end]

</div>

Having installed or downloaded TypeDB, we can now [start the Server](#start-the-typedb-server) and interact with the
[TypeDB Studio](../../02-clients/01-studio.md), [TypeDB Console](../../02-clients/02-console.md) or any other 
[client](../02-dev/04-clients.md).




