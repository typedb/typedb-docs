---
pageTitle: Client Java
keywords: grakn, client, java
longTailKeywords: grakn java client, grakn client java, client java, java client
Summary: API Reference of Grakn Client Java.
templatePath: 03-client-api/references/
---

## Dependencies

| Client Java | Grakn Core | Grakn KGMS |
| :---------: | :--------: | :--------: |
| 1.5.2       | 1.5.2      | 1.5.2      |
| 1.5.0       | 1.5.0      | N/A        |
| 1.4.3       | 1.4.3      | 1.4.3      |
| 1.4.2       | 1.4.2      | 1.2.0      |
| 1.4.1       | 1.4.0      | 1.2.0      |
| 1.4.0       | 1.4.0      | 1.2.0      |
| 1.3.0       | 1.3.0      | 1.2.0      |

<div class="tabs dark">

[tab:Grakn Core]
```xml
<repositories>
    <repository>
        <id>repo.grakn.ai</id>
        <url>https://repo.grakn.ai/repository/maven/</url>
    </repository>
</repositories>
<dependencies>
    <dependency>
        <groupId>io.grakn.client</groupId>
        <artifactId>api</artifactId>
        <version>1.5.0</version>
    </dependency>
</dependencies>
```
[tab:end]

[tab:Grakn KGMS]
```xml
<repositories>
    <repository>
        <id>mavencentral</id>
        <url>https://oss.sonatype.org/content/repositories/releases</url>
    </repository>
</repositories>
<dependencies>
    <dependency>
        <groupId>ai.grakn.kgms</groupId>
        <artifactId>client</artifactId>
        <version>1.4.3</version>
    </dependency>
</dependencies>
```
[tab:end]

</div>

## Quickstart
First make sure, the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

Import `grakn.client.GraknClient`, instantiate a client and open a session to a [keyspace](../06-management/01-keyspace.md).

<!-- test-example GraknQuickstartA.java -->
```java
package grakn.examples;

import grakn.client.GraknClient;

public class GraknQuickstartA {
    public static void main(String[] args) {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");
        // session is open
        session.close();
        // session is closed
    }
}
```

[KGMS ONLY] Using Client Java 1.4.3, we can also pass the credentials, as specified when [configuring authentication via Grakn Console](../06-management/02-users.md).

<!-- test-ignore -->
```java
SimpleURI localGrakn = new SimpleURI("localhost", 48555);
Grakn grakn = new ClientFactory(localGrakn, "<username>", "<password>").client();
```

Create transactions to use for reading and writing data.

<!-- test-example GraknQuickstartB.java -->
```java
package grakn.examples;

import grakn.client.GraknClient;

public class GraknQuickstartB {
    public static void main(String[] args) {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("social_network");

        // creating a write transaction
        GraknClient.Transaction writeTransaction = session.transaction().write();
        // write transaction is open
        // write transaction must always be committed (closed)
        writeTransaction.commit();

        // creating a read transaction
        GraknClient.Transaction readTransaction = session.transaction().read();
        // read transaction is open
        // read transaction must always be closed
        readTransaction.close();

        session.close();
    }
}

```

Running basic retrieval and insertion queries.

<!-- test-example GraknQuickstartC.java -->
```java
package grakn.examples;

import grakn.client.GraknClient;
import graql.lang.Graql;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlGet;
import graql.lang.query.GraqlInsert;
import grakn.core.concept.answer.ConceptMap;

import java.util.List;
import java.util.stream.Stream;

public class GraknQuickstartC {
  public static void main(String[] args) {
    GraknClient client = new GraknClient("localhost:48555");
    GraknClient.Session session = client.session("social_network");

    // Insert a person using a WRITE transaction
    GraknClient.Transaction writeTransaction = session.transaction().write();
    GraqlInsert insertQuery = Graql.insert(var("x").isa("person").has("email", "x@email.com"));
    List<ConceptMap> insertedId = writeTransaction.execute(insertQuery);
    System.out.println("Inserted a person with ID: " + insertedId.get(0).get("x").id());
    // to persist changes, a write transaction must always be committed (closed)
    writeTransaction.commit();

    // Read the person using a READ only transaction
    GraknClient.Transaction readTransaction = session.transaction().read();
    GraqlGet getQuery = Graql.match(var("p").isa("person")).get().limit(10);
    Stream<ConceptMap> answers = readTransaction.stream(getQuery);
    answers.forEach(answer -> System.out.println(answer.get("p").id()));

    // a read transaction and session must always be closed
    readTransaction.close();
    session.close();
  }
}

```
<div class="note">
[Important]
Remember that transactions always need to be closed. Commiting a write transaction closes it. A read transaction, however, must be explicitly clased by calling the `close()` method on it.
</div>

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Java, head over to their dedicated documentation pages as listed below.

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)
- [Compute](../11-query/07-compute-query.md)

<hr style="margin-top: 40px;" />

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.grakn language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.graql language="java" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="java" %}
