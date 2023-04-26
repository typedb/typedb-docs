---
pageTitle: Client Java
keywords: typedb, client, java
longTailKeywords: typedb java client, typedb client java, client java, java client
Summary: API Reference of TypeDB Client Java.
templatePath: 03-client-api/references/
---

## Installation

### Prerequisites

To use this client, you need a compatible version of TypeDB Server running. Please see the
[Compatibility Table](#version-compatibility) to check what version do you need, depending on the TypeDB server version
being used.

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

By default, Client Java uses Logback to print errors and debugging info to standard output. As it is quite verbose, 
use the following steps to set the minimum log level to ERROR:

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

## Quickstart

First make sure, the [TypeDB Server](/docs/running-typedb/install-and-run#start-the-typedb-server) is running.

Import `com.vaticle.typedb.client.TypeDB`, instantiate a TypeDB Core client and open a session to
a [database](../06-management/01-database.md).

<!-- test-example TypeDBQuickstartA.java -->
```java
package com.vaticle.doc.examples;


import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.TypeDB;

public class TypeDBQuickstartA {
    public static void main(String[] args) {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");
        // client is open
        TypeDBSession session = client.session("social_network", TypeDBSession.Type.DATA);
        // session is open
        session.close();
        // session is closed
        client.close();
        // client is closed
    }
}
```

Create transactions to use for reading and writing data.

<!-- test-example TypeDBQuickstartB.java -->
```java
package com.vaticle.doc.examples;

import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.TypeDB;

public class TypeDBQuickstartB {
    public static void main(String[] args) {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");

        try (TypeDBSession session = client.session("social_network", TypeDBSession.Type.DATA)) {
            // creating a write transaction
            TypeDBTransaction writeTransaction = session.transaction(TypeDBTransaction.Type.WRITE);
            // write transaction is open
            // write transaction must always be committed (closed)
            writeTransaction.commit();

            // creating a read transaction
            TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ);
            // read transaction is open
            // read transaction must always be closed
            readTransaction.close();
        }

        client.close();
    }
}
```

Running basic retrieval and insertion queries.

<!-- test-example TypeDBQuickstartC.java -->
```java
package com.vaticle.doc.examples;


import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typeql.lang.TypeQL;

import static com.vaticle.typeql.lang.TypeQL.*;

import com.vaticle.typeql.lang.query.TypeQLMatch;
import com.vaticle.typeql.lang.query.TypeQLInsert;
import com.vaticle.typedb.client.api.answer.ConceptMap;

import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Collectors;

public class TypeDBQuickstartC {
    public static void main(String[] args) {
        TypeDBClient client = TypeDB.coreClient("localhost:1729");

        try (TypeDBSession session = client.session("social_network", TypeDBSession.Type.DATA)) {

            try (TypeDBTransaction writeTransaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
                // Insert a person using a WRITE transaction
                TypeQLInsert insertQuery = TypeQL.insert(var("x").isa("person").has("email", "x@email.com"));
                List<ConceptMap> insertedId = writeTransaction.query().insert(insertQuery).collect(Collectors.toList());
                System.out.println("Inserted a person with ID: " + insertedId.get(0).get("x").asThing().getIID());
                // to persist changes, a write transaction must always be committed (closed)
                writeTransaction.commit();
            }

            try (TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ)) {
                // Read the person using a READ only transaction
                TypeQLMatch.Limited getQuery = TypeQL.match(var("p").isa("person")).get("p").limit(10);
                Stream<ConceptMap> answers = readTransaction.query().match(getQuery);
                answers.forEach(answer -> System.out.println(answer.get("p").asThing().getIID()));
            }
        }

        client.close();
    }
}

```

<div class="note">
[Important]
Remember that transactions always need to be closed. Committing a write transaction closes it. A read transaction, however, must be explicitly closed by calling the `close()` method on it.
</div>

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts
retrieved as the answers to queries.

To view examples of running various TypeQL queries using the Java client, head over to their dedicated documentation
pages as listed below.

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Update](../11-query/05-update-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)

<hr style="margin-top: 40px;" />

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.typedb language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.options language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.typeql language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="java" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.query_future language="java" %}

## Version Compatibility

|   Client Java    |      TypeDB      |  TypeDB Cluster  |
|:----------------:|:----------------:|:----------------:|
| 2.17.0 to 2.17.1 |      2.17.0      |      2.17.0      |
|      2.16.1      |      2.16.1      |      2.16.1      |
| 2.14.1 to 2.14.3 | 2.14.1 to 2.15.0 | 2.14.1 to 2.15.0 |
|      2.12.0      | 2.12.0 to 2.13.0 |      2.13.0      |
| 2.9.0 to 2.11.1  | 2.9.0 to 2.11.1  | 2.9.0 to 2.11.2  |
|      2.8.0       |      2.8.0       |       N/A        |
|  2.6.0 to 2.6.2  |  2.6.0 to 2.7.1  |       N/A        |
|      2.5.0       |  2.1.2 to 2.5.0  |      2.5.0       |
|  2.1.0 to 2.4.0  |  2.1.2 to 2.5.0  |  2.1.2 to 2.3.0  |
|      2.0.1       |      2.0.2       |      2.0.2       |
|      2.0.0       |   2.0.0, 2.0.1   |   2.0.0, 2.0.1   |
|      1.8.3       |  1.8.0 to 1.8.4  |       N/A        |
|      1.8.2       |   1.8.0, 1.8.1   |       N/A        |
|  1.8.0 to 1.8.1  |      1.8.0       |       N/A        |
