---
pageTitle: Client Java installation
keywords: typedb, client, java, install, repository
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: Tutorial for TypeDB Client Java.
---

## Installation

### Prerequisites

To use the Java Driver, you need a compatible version of TypeDB Server running. Please see the
[Compatibility Table](03-java.md#version-compatibility) to check what version do you need, depending on the TypeDB 
server version being used.

### Add a repository with TypeDB Java client to Maven

Add the code below to the `pom.xml` file in your Maven project.

<div class="note">
[Important]
Be sure to replace the `{version}` placeholder tag with the version of Client Java you want to install.
</div>

```xml

<repositories>
    <repository>
        <id>repo.vaticle.com</id>
        <url>https://repo.vaticle.com/repository/maven/</url>
    </repository>
</repositories>
<dependencies>
<dependency>
    &lt;groupId&gt;com.vaticle.typedb&lt;/groupId&gt;
    &lt;artifactId&gt;typedb-client&lt;/artifactId&gt;
    <version>{version}</version>
</dependency>
</dependencies>
```

If you want to depend on snapshot versions of Client Java, by referring to the GitHub commit `sha`, you can add our
snapshot repository to your list of Maven repositories.

```xml

<repositories>
    <repository>
        <id>repo.vaticle.com.snapshot</id>
        <name>repo.vaticle.comai</name>
        <url>https://repo.vaticle.com/repository/maven-snapshot/</url>
    </repository>
</repositories>
```

### (Optional) Add logging config

By default, the Java Driver uses Logback to print errors and debugging info to standard output. As it is quite verbose, 
use the following steps to set the minimum log level to `ERROR`:

1. Create a file in the `resources` path (`src/main/resources` by default in a Maven project) named `logback.xml`.
2. Copy the following document into the `logback.xml`:

```xml

<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="ERROR">
        <appender-ref ref="STDOUT"/>
    </root>

</configuration>
```

### Resources

- [Client Java on GitHub](https://github.com/vaticle/typedb-client-java)
- [Releases](https://github.com/vaticle/typedb-client-java/releases)
- [Examples](https://github.com/vaticle/typedb-examples)
