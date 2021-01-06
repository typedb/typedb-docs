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

### Grakn Core 2.0
Grakn Core 2.0 is currently in alpha, and will be updated frequently - the latest release of Client Java 2.0 can be found in the Grakn [public Maven repository](https://repo.grakn.ai/#browse/browse:maven:io%2Fgrakn%2Fclient%2Fgrakn-client).

## Quickstart
First make sure, the [Grakn Server](/docs/running-grakn/install-and-run#start-the-grakn-server) is running.

Import `grakn.client.GraknClient`, instantiate a client and open a session to a [database](../06-management/01-database.md).

<!-- test-example GraknQuickstartA.java -->
```java
package grakn.examples;

import grakn.client.Grakn;
import grakn.client.GraknClient;

public class GraknQuickstartA {
    public static void main(String[] args) {
        Grakn.Client client = new GraknClient("localhost:1729");
        // client is open
        Grakn.Session session = client.session("social_network", Grakn.Session.Type.DATA);
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

import grakn.client.Grakn;
import grakn.client.Grakn.Session;
import grakn.client.Grakn.Transaction;
import grakn.client.GraknClient;

public class GraknQuickstartB {
    public static void main(String[] args) {
        Grakn.Client client = new GraknClient("localhost:1729");
        Session session = client.session("social_network", Session.Type.DATA);

        // creating a write transaction
        Transaction writeTransaction = session.transaction(Transaction.Type.WRITE);
        // write transaction is open
        // write transaction must always be committed (closed)
        writeTransaction.commit();

        // creating a read transaction
        Transaction readTransaction = session.transaction(Transaction.Type.READ);
        // read transaction is open
        // read transaction must always be closed
        readTransaction.close();

        session.close();
        client.close();
    }
}
```

Running basic retrieval and insertion queries.

<!-- test-example GraknQuickstartC.java -->
```java
package grakn.examples;

import grakn.client.Grakn;
import grakn.client.Grakn.Session;
import grakn.client.Grakn.Transaction;
import grakn.client.GraknClient;
import graql.lang.Graql;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlMatch;
import graql.lang.query.GraqlInsert;
import grakn.client.concept.answer.ConceptMap;

import java.util.List;
import java.util.stream.Stream;
import java.util.stream.Collectors;

public class GraknQuickstartC {
  public static void main(String[] args) {
    Grakn.Client client = new GraknClient("localhost:1729");
    Session session = client.session("social_network", Session.Type.DATA);

    // Insert a person using a WRITE transaction
    Transaction writeTransaction = session.transaction(Transaction.Type.WRITE);
    GraqlInsert insertQuery = Graql.insert(var("x").isa("person").has("email", "x@email.com"));
    List<ConceptMap> insertedId = writeTransaction.query().insert(insertQuery).collect(Collectors.toList());
    System.out.println("Inserted a person with ID: " + insertedId.get(0).get("x").asThing().getIID());
    // to persist changes, a write transaction must always be committed (closed)
    writeTransaction.commit();

    // Read the person using a READ only transaction
    Transaction readTransaction = session.transaction(Transaction.Type.READ);
    GraqlMatch.Limited getQuery = Graql.match(var("p").isa("person")).get("p").limit(10);
    Stream<ConceptMap> answers = readTransaction.query().match(getQuery);
    answers.forEach(answer -> System.out.println(answer.get("p").asThing().getIID()));

    // transactions, sessions and clients must always be closed
    readTransaction.close();
    session.close();
    client.close();
  }
}

```
<div class="note">
[Important]
Remember that transactions always need to be closed. Commiting a write transaction closes it. A read transaction, however, must be explicitly closed by calling the `close()` method on it.
</div>

Check out the [Concept API](../04-concept-api/00-overview.md) to learn about the available methods on the concepts retrieved as the answers to Graql queries.

To view examples of running various Graql queries using the Grakn Client Java, head over to their dedicated documentation pages as listed below.

- [Insert](../11-query/03-insert-query.md)
- [Get](../11-query/02-get-query.md)
- [Delete](../11-query/04-delete-query.md)
- [Aggregate](../11-query/06-aggregate-query.md)

<hr style="margin-top: 40px;" />

## API Reference

{% include api/generic.html data=site.data.03_client_api.references.grakn language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.client language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.session language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.transaction language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.options language="java" %}

{% include api/generic.html data=site.data.03_client_api.references.graql language="java" %}

{% include api/answers.html data=site.data.03_client_api.references.answer language="java" %}


 
## Dependencies

| Client Java   | Grakn Core     | Grakn Cluster  |
| :---------:   | :-------------:| :------------: |
| 2.0.0-alpha-2 | 2.0.0-alpha    | N/A            |
| 1.8.3         | 1.8.0 to 1.8.4 | N/A            |
| 1.8.2         | 1.8.0, 1.8.1   | N/A            |
| 1.8.1         | 1.8.0          | N/A            |
| 1.8.0         | 1.8.0          | N/A            |
| 1.7.3         | 1.7.1, 1.7.2   | N/A            |
| 1.7.2         | 1.7.1, 1.7.2   | N/A            |
| 1.6.2         | 1.6.2          | 1.6.2          |
| 1.6.1         | 1.6.0, 1.6.1   | N/A            |
| 1.5.5         | 1.5.8, 1.5.9   | 1.5.8          |
| 1.5.4         | 1.5.8, 1.5.9   | 1.5.8          |
| 1.5.3         | 1.5.2 to 1.5.7 | 1.5.2 to 1.5.7 |
| 1.5.2         | 1.5.2, 1.5.3   | 1.5.2 to 1.5.4 |
| 1.5.0         | 1.5.0          | N/A            |
| 1.4.3         | 1.4.3          | 1.4.3          |
| 1.4.2         | 1.4.2          | 1.2.0          |
| 1.4.1         | 1.4.0          | 1.2.0          |
| 1.4.0         | 1.4.0          | 1.2.0          |
| 1.3.0         | 1.3.0          | 1.2.0          |
