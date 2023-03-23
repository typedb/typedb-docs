---
pageTitle: Installation
keywords: setup, getting started, typedb, download, install, server, linux, mac, windows, docker
longTailKeywords: typedb on linux, typedb on mac, typedb on windows, start typedb server
summary: Install and run the TypeDB Server on Linux, Mac or Windows.
toc: false
---

# Installation

<!--- Reimplement tabs when they are product ready -->

## Docker

### Install

1. Ensure [Docker](https://docs.docker.com/get-docker/) is installed and running:

<!-- test-ignore -->
   ```bash
   docker version
   ```

2. Pull the latest TypeDB Docker image:

<!-- test-ignore -->
   ```bash
   docker pull vaticle/typedb:latest
   ```


### Start

The TypeDB container exposes TypeDB’s default port, `1729`, and uses its default data directory, 
`/opt/typedb-all-linux/server/data`.

The following command starts a named TypeDB container, maps its exposed port to the host machine and creates a named 
volume mapped to the data directory — making it persistent across container restarts.

<!-- test-ignore -->
```bash
docker run --name try-typedb -d -v try-typedb-data:/opt/typedb-all-linux/server/data/ -p 1729:1729 --platform linux/amd64 vaticle/typedb:latest
```

<div class="note">
[Note]
The `--platform linux/amd64` parameter is required to run the TypeDB container on MacOS with an ARM64 architecture 
(e.g. M1 processor).
</div>

The following variables should be noted and can be modified:

- `try-typedb` – the name of the container,
- `try-typedb-data` – the name of the volume to persist data,
- `latest` – the version of TypeDB.

### Stop

<!-- test-ignore -->
```bash
docker stop try-typedb
```

## Windows

### Install

1. Ensure Java 11+ is installed

      TypeDB supports the [OpenJDK](https://jdk.java.net) and 
      [Oracle JDK](https://www.oracle.com/java/technologies/downloads/).

2. Download TypeDB
   
   Download the latest release of [TypeDB](https://vaticle.com/download).

3. Extract archive
   
   Create a new directory, extract the contents of the zip file and move them (hereinafter replace `2.15.0` with the 
   version downloaded):

   <!-- test-ignore -->
   ```shell
   mkdir "C:\Program Files\TypeDB"
   tar xvf ./Downloads/typedb-all-windows-2.15.0.zip
   move ./Downloads/typedb-all-windows-2.15.0/* "C:\Program Files\TypeDB"
   ```

4. Update the PATH environment variable with the TypeDB installation directory:

   <!-- test-ignore -->
   ```shell
   setx /M PATH "%path%;C:\Program Files\TypeDB"
   ```

### Start

Run the following command in a terminal:

<!-- test-ignore -->
```shell
typedb server
```

<div class="note">
[Note]
TypeDB will run in the foreground. If the terminal running TypeDB is closed, TypeDB will be shut down. We recommend 
opening a new terminal to run TypeDB Console.
</div>



<div class="note">
[Note]
If the following error occurs, please try to install the "C++ redistributable" by following the instructions here.

<!-- test-ignore -->
```shell
Exception in thread "main" java.lang.UnsatisfiedLinkError:
C:\Users\Vaticle\AppData\Local\Temp\ortools-java\win32-x86-64\jniortools.dll: Can't find dependent libraries
```
</div>

### Stop

Press Ctrl-C in the terminal running TypeDB.

## Linux

### Install

#### APT

1. Add the TypeDB repository:
   
   <!-- test-ignore -->
   ```bash
   sudo apt install software-properties-common apt-transport-https gpg
   gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 8F3DA4B5E9AEF44C
   gpg --export 8F3DA4B5E9AEF44C | sudo tee /etc/apt/trusted.gpg.d/vaticle.gpg > /dev/null
   echo "deb [ arch=all ] https://repo.vaticle.com/repository/apt/ trusty main" | sudo tee /etc/apt/sources.list.d/vaticle.list > /dev/null
   ```

2. Update the package cache:

   <!-- test-ignore -->
   ```bash
   sudo apt update
   ```
3. Ensure Java 11+ is installed:

   <!-- test-ignore -->
   ```bash
   sudo apt install openjdk-11-jre
   ```

   TypeDB supports the [OpenJDK](https://jdk.java.net) and
   [Oracle JDK](https://www.oracle.com/java/technologies/downloads/).

4. Check the latest version number for typedb-server and its dependencies:

   <!-- test-ignore -->
   ```bash
   apt show typedb-server
   ```

   This will show you console output like this:

   <!-- test-ignore -->
   ```bash
   Package: typedb-server
   Version: 2.15.0
   Priority: optional
   Section: contrib/devel
   Maintainer: Vaticle <community@vaticle.com>
   Installed-Size: unknown
   Depends: openjdk-11-jre, typedb-bin (=2.12.0)
   Download-Size: 71.8 MB
   APT-Sources: https://repo.vaticle.com/repository/apt trusty/main all Packages
   Description: TypeDB (server)
   ```

   Take a note of the latest typedb-server version shown at the `Package` field and the correspondent `typedb-bin` 
   package version shown at the `Depends` field.

   If we want some other version of TypeDB installed, we can use the `apt show typedb-server=2.14.1` where `2.14.1` — 
   is the version we need.

5. Install TypeDB using the versions from the previous command (here we will use typedb-server version 2.15 for 
   example):

   <!-- test-ignore -->
   ```bash
   sudo apt install typedb-server=2.15.0 typedb-console=2.15.0 typedb-bin=2.12.0
   ```

<div class="note">
[Note]
The `typedb-server` and `typedb-console` packages are updated more often than `typedb-bin` that is why their version 
numbers might differ. By default, APT will look for the exact same version of `typedb-bin` and that will result in an 
error. To prevent this we use apt show as shown above to display the dependencies of `typedb-server`, take note of 
the `typedb-bin` version required and invoke an `apt install` command with the specific version of every package.
</div>

#### Manual

1. Ensure Java 11+ is installed:

   TypeDB supports the [OpenJDK](https://jdk.java.net) and
   [Oracle JDK](https://www.oracle.com/java/technologies/downloads/).

2. Download TypeDB:

   Download the latest release of [TypeDB](https://vaticle.com/download).

3. Extract archive:

   Create a new directory, extract the contents of the zip file and move them
   (hereinafter replace `2.15.0` with the version downloaded):
   
   <!-- test-ignore -->
   ```bash
   mkdir /opt/typedb
   tar -xzf ~/Downloads/typedb-all-linux-2.15.0.tar.gz
   mv ~/Downloads/typedb-all-linux-2.15.0 /opt/typedb
   ```
   
4. Add a symlink to the TypeDB executable in the /usr/local/bin directory:

   <!-- test-ignore -->
   ```bash
   ln -s /opt/typedb/typedb /usr/local/bin/typedb
   ```

### Start

Run the following command in a terminal:

<!-- test-ignore -->
```shell
typedb server
```

<div class="note">
[Note]
TypeDB will run in the foreground. If the terminal running TypeDB is closed, TypeDB will be shut down. We recommend 
opening a new terminal to run TypeDB Console.
</div>

### Stop

Press Ctrl-C in the terminal running TypeDB.

## macOS

### Install

#### Homebrew

1. Ensure [Homebrew](https://brew.sh/) is installed.

2. Install TypeDB:

   <!-- test-ignore -->
   ```sh
   brew install typedb
   ```

#### Manual

1. Ensure Java 11+ is installed

   TypeDB supports the [OpenJDK](https://jdk.java.net) and
   [Oracle JDK](https://www.oracle.com/java/technologies/downloads/).

2. Download TypeDB

   Download the latest release of TypeDB to the `~/Downloads` directory.

3. Extract archive

   Extract the downloaded archive (hereinafter replace `2.15.0` with the version downloaded):
   
   <!-- test-ignore -->
   ```bash
   unzip ~/Downloads/typedb-all-mac-2.15.0.zip
   ```   

4. Create a new directory and move the contents of the extracted zip file to it:

   <!-- test-ignore -->  
   ```bash
   sudo mkdir /opt/typedb
   sudo mv ~/Downloads/typedb-all-mac-2.15.0/*(DN) /opt/typedb
   ```

5. Add a symlink to typedb executable in the /usr/local/bin directory:
   
   <!-- test-ignore -->
   ```bash
   ln -s /opt/typedb/typedb /usr/local/bin/typedb
   ```
   
### Start

Run the following command in a terminal:

<!-- test-ignore -->
```bash
typedb server
```

Now we can start the TypeDB Server by using the `typedb server` command in local terminal.

<div class="note">
[Note]
TypeDB will run in the foreground. If the terminal running TypeDB is closed, TypeDB server will be shut down. We 
recommend opening a new terminal to run TypeDB Console.
</div>

### Stop

Press Ctrl-C in the terminal running TypeDB.

## After installation

Having installed or downloaded TypeDB, we can now interact with the [TypeDB Studio](../../02-clients/01-studio.md), 
[TypeDB Console](../../02-clients/02-console.md) or one of the [TypeDB drivers](../../02-clients/00-clients.md).
