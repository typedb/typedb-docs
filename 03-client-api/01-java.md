---
pageTitle: Client Java
keywords: grakn, client, java
longTailKeywords: grakn java client, grakn client java, client java, java client
Summary: API Reference of Grakn Client Java.
templatePath: 03-client-api/references/
---

## Installation

#### To use this client, you need a compatible Grakn Server running. Visit our [Compatibility Table](#dependencies)

```xml
<repositories>
    <repository>
        <id>repo.grakn.ai</id>
        <url>https://repo.grakn.ai/repository/maven/</url>
    </repository>
</repositories>
<dependencies>
    <dependency>
        &lt;groupId&gt;io.grakn.client&lt;/groupId&gt;
        &lt;artifactId&gt;grakn-client&lt;/artifactId&gt;
        <version>{version}</version>
    </dependency>
</dependencies>
```

If you want to depend on snapshot versions of Client Java, by referring to the GitHub commit `sha`, you can add our snapshot repository to your list of Maven repositories.

```xml
<repositories>
    <repository>
        <id>repo.grakn.ai.snapshot</id>
        <name>repo.grakn.ai</name>
        <url>https://repo.grakn.ai/repository/maven-snapshot/</url>
    </repository>
</repositories>
```

## Quickstart
First make sure, the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

Import `grakn.client.Grakn`, instantiate a Grakn Core client and open a session to a [database](../06-management/01-database.md).

<!-- test-example GraknQuickstartA.java -->
```java
package grakn.examples;


import grakn.client.api.GraknClient;
import grakn.client.api.GraknSession;
import grakn.client.Grakn;

public class GraknQuickstartA {
    public static void main(String[] args) {
        GraknClient client = Grakn.coreClient("localhost:1729");
        // client is open
        GraknSession session = client.session("social_network", GraknSession.Type.DATA);
        // session is open
        session.close();
        // session is closed
        client.close();
        // client is closed
    }
}
```

Create transactions to use for reading and writing data.

<!-- test-example GraknQuickstartB.java -->
```java
package grakn.examples;

import grakn.client.api.GraknClient;
import grakn.client.api.GraknSession;
import grakn.client.api.GraknTransaction;
import grakn.client.Grakn;

public class GraknQuickstartB {
    public static void main(String[] args) {
        GraknClient client = Grakn.coreClient("localhost:1729");

        try (GraknSession session = client.session("social_network", GraknSession.Type.DATA)) {
            // creating a write transaction
            GraknTransaction writeTransaction = session.transaction(GraknTransaction.Type.WRITE);
            // write transaction is open
            // write transaction must always be committed (closed)
            writeTransaction.commit();
    
            // creating a read transaction
            GraknTransaction readTransaction = session.transaction(GraknTransaction.Type.READ);
            // read transaction is open
            // read transaction must always be closed
            readTransaction.close();
        }

        client.close();
    }
}
```

Running basic retrieval and insertion queries.

<!-- test-example GraknQuickstartC.java -->
```java
package grakn.examples;


import grakn.client.api.GraknClient;
import grakn.client.api.GraknSession;
import grakn.client.api.GraknTransaction;
import grakn.client.Grakn;
import graql.lang.Graql;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlMatch;
import graql.lang.query.GraqlInsert;
import grakn.client.api.answer.ConceptMap;

import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Collectors;

public class GraknQuickstartC {
    public static void main(String[] args) {
        GraknClient client = Grakn.coreClient("localhost:1729");

        try (GraknSession session = client.session("social_network", GraknSession.Type.DATA)) {
            
            try (GraknTransaction writeTransaction = session.transaction(GraknTransaction.Type.WRITE)) {
                // Insert a person using a WRITE transaction
                GraqlInsert insertQuery = Graql.insert(var("x").isa("person").has("email", "x@email.com"));
                List<ConceptMap> insertedId = writeTransaction.query().insert(insertQuery).collect(Collectors.toList());
                System.out.println("Inserted a person with ID: " + insertedId.get(0).get("x").asThing().getIID());
                // to persist changes, a write transaction must always be committed (closed)
                writeTransaction.commit();
            }
            
            try (GraknTransaction readTransaction = session.transaction(GraknTransaction.Type.READ)) {
                // Read the person using a READ only transaction
                GraqlMatch.Limited getQuery = Graql.match(var("p").isa("person")).get("p").limit(10);
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

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Java, head over to their dedicated documentation pages as listed below.

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Update](../11-query/05-update-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)

<hr style="margin-top: 40px;" />

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.grakn language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.options language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.graql language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.query_manager language="java" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.query_future language="java" %}


## Version Compatibility

| Client Java | Grakn Core     | Grakn Cluster  |
| :---------: | :-------------:| :------------: |
| 2.0.1       | 2.0.2          | 2.0.2          |
| 2.0.0       | 2.0.0, 2.0.1   | 2.0.0, 2.0.1   |
| 1.8.3       | 1.8.0 to 1.8.4 | N/A            |
| 1.8.2       | 1.8.0, 1.8.1   | N/A            |
| 1.8.1       | 1.8.0          | N/A            |
| 1.8.0       | 1.8.0          | N/A            |
| 1.7.3       | 1.7.1, 1.7.2   | N/A            |
| 1.7.2       | 1.7.1, 1.7.2   | N/A            |
| 1.6.2       | 1.6.2          | 1.6.2          |
| 1.6.1       | 1.6.0, 1.6.1   | N/A            |
| 1.5.5       | 1.5.8, 1.5.9   | 1.5.8          |
| 1.5.4       | 1.5.8, 1.5.9   | 1.5.8          |
| 1.5.3       | 1.5.2 to 1.5.7 | 1.5.2 to 1.5.7 |
| 1.5.2       | 1.5.2, 1.5.3   | 1.5.2 to 1.5.4 |
| 1.5.0       | 1.5.0          | N/A            |
| 1.4.3       | 1.4.3          | 1.4.3          |
| 1.4.2       | 1.4.2          | 1.2.0          |
| 1.4.1       | 1.4.0          | 1.2.0          |
| 1.4.0       | 1.4.0          | 1.2.0          |
| 1.3.0       | 1.3.0          | 1.2.0          |
