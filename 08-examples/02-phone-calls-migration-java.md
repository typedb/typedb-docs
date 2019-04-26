---
pageTitle: Migrating CSV, JSON and XML Data with Client Java
keywords: grakn, examples, migration, java
longTailKeywords: grakn java migration
Summary: Learn how to use Client Java to migrate CSV, JSON and XML data into a Grakn Knowledge Graph.
---

## Goal

In this tutorial, our aim is to migrate some actual data to the `phone_calls` knowledge graph that we [defined previously](../08-examples/01-phone-calls-schema.md) using [Client Java](../03-client-api/01-java.md).

## A Quick Look at the Schema

Before we get started with migration, let’s have a quick reminder of how the schema for the `phone_calls` knowledge graph looks like.

![The Visualised Schema](../images/examples/phone_calls_schema.png)

## An Overview

Let’s go through a summary of how the migration takes place.

1.  we need a way to talk to our Grakn [keyspace](../06-management/01-keyspace.md). To do this, we use [Client Java](../03-client-api/01-java.md).
2.  we go through each data file, extracting each data item and parsing it to a JSON object.
3.  we pass each data item (in the form of a JSON object) to its corresponding template. What the template returns is the Graql query for inserting that item into Grakn.
4.  we execute each of those queries to load the data into our target keyspace — `phone_calls`.

Before moving on, make sure you have **Java 1.8** installed and the [**Grakn Server**](/docs/running-grakn/install-and-run#start-the-grakn-server) running on your machine.

## Get Started

### Create a new Maven project
This project uses SDK 1.8 and is named `phone_calls`. I am using IntelliJ as the IDE.

### Set Grakn as a dependency
Modify `pom.xml` to include the latest version of Grakn Core, Graql and Grakn Client Java as dependencies.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
  	<groupId>io.grakn.examples</groupId>
  	<artifactId>migrate-csv-to-grakn</artifactId>
  	<version>1.0.0</version>
  	<repositories>
    	<repository>
      		<id>repo.grakn.ai</id>
            <url>https://repo.grakn.ai/repository/maven/</url>
    	</repository>
  	</repositories>
  	<properties>
    	<maven.compiler.source>1.7</maven.compiler.source>
    	<maven.compiler.target>1.7</maven.compiler.target>
  	</properties>
  	<dependencies>
    	<dependency>
            <groupId>io.grakn.core</groupId>
            <artifactId>concept</artifactId>
            <version>1.5.2</version>
        </dependency>
        <dependency>
            <groupId>io.graql</groupId>
            <artifactId>lang</artifactId>
            <version>1.0.1</version>
        </dependency>
        <dependency>
            <groupId>io.grakn.client</groupId>
            <artifactId>api</artifactId>
            <version>1.5.2</version>
        </dependency>
  	</dependencies>
</project>
```

### Configure logging

We would like to be able to configure what Grakn logs out. To do this, modify `pom.xml` to add `logback` as a dependency.

```xml
<dependency>
	<groupId>ch.qos.logback</groupId>
	<artifactId>logback-classic</artifactId>
	<version>1.2.3</version>
</dependency>
```

Next, add a new file called `logback.xml` with the content below and place it under `src/main/resources`.

```xml
<configuration debug="false">
    <root level="INFO"/>
</configuration>
```

## Include the Data Files

Pick one of the data formats below and download the files. After you download them, place the four files under the `phone_calls/data` directory. We use these to load their data into our `phone_calls` knowledge graph.

**CSV** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/companies.csv) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/people.csv) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/contracts.csv) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/calls.csv)

**JSON** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/companies.json) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/people.json) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/contracts.json) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/calls.json)

**XML** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/companies.xml) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/people.xml) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/contracts.xml) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/calls.xml)

## Specify Details For Each Data File

Before anything, we need a structure to contain the details required for reading data files and constructing Graql queries. These details include:
- The path to the data file, and
- The template function that receives a JSON object and produces a Graql insert query.

For this purpose, we create a new subclass called `Input`.

<!-- test-ignore -->
```java
import mjson.Json;

public class PhoneCallsMigration {
  abstract static class Input {
    String path;

    public Input(String path) {
      this.path = path;
    }

    String getDataPath() {
      return path;
    }

    abstract String template(Json data);
  }
}
```

Later in this tutorial, we see how an instance of the `Input` class can be created, but before we get to that, let’s add the `mjson` dependency to the `dependencies` tag in our `pom.xml` file.

```xml
<dependency>
	<groupId>org.sharegov</groupId>
	<artifactId>mjson</artifactId>
	<version>1.4.1</version>
</dependency>
```

Time to initialise the `inputs`.

The code below calls the `initialiseInputs()` method which returns a collection of `inputs`. We then use each input element in this collection to load each data file into Grakn.

<!-- test-ignore -->
```java
// other imports
import java.util.ArrayList;
import java.util.Collection;

public class PhoneCallsMigration {
  abstract static class Input {...}

  public static void main(String[] args) {
    Collection<Input> inputs = initialiseInputs();
  }

  static Collection<Input> initialiseInputs() {
    Collection<Input> inputs = new ArrayList<>();
    // coming up next
    return inputs;
  }
}
```

## Input Instance For a Company

<!-- test-ignore -->
```java
// imports

public class Migration {
  abstract static class Input {...}
  public static void main(String[] args) {...}

  static Collection<Input> initialiseInputs() {
    Collection<Input> inputs = new ArrayList<>();

    inputs.add(new Input("data/companies") {
      @Override
      public String template(Json company) {
        return "insert $company isa company, has name " + company.at("name") + ";";
      }
    });

    return inputs;
  }
}
```

`input.getDataPath()` returns `data/companies`.

Given the company,

<!-- test-ignore -->
```java
{ name: "Telecom" }
```

`input.template(company)` returns
<!-- test-ignore -->
```graql
insert $company isa company, has name "Telecom";
```


## Input Instance For a Person

<!-- test-ignore -->
```java
// imports

public class PhoneCallsMigration {
  abstract static class Input {...}
  public static void main(String[] args) {...}

  static Collection<Input> initialiseInputs() {
    Collection<Input> inputs = new ArrayList<>();

    inputs.add(new Input("data/companies") {...});

    inputs.add(new Input("data/people") {
      @Override
      public String template(Json person) {
        // insert person
        String graqlInsertQuery = "insert $person isa person, has phone-number " +
        person.at("phone_number");

        if (! person.has("first_name")) {
          // person is not a customer
          graqlInsertQuery += ", has is-customer false";
        } else {
          // person is a customer
          graqlInsertQuery += ", has is-customer true";
            graqlInsertQuery += ", has first-name " + person.at("first_name");
            graqlInsertQuery += ", has last-name " + person.at("last_name");
            graqlInsertQuery += ", has city " + person.at("city");
            graqlInsertQuery += ", has age " + person.at("age").asInteger();
          }

          graqlInsertQuery += ";";
          return graqlInsertQuery;
      }
    });

    return inputs;
  }
}
```

`input.getDataPath()` returns `data/people`.

Given the person,

<!-- test-ignore -->
```java
{ phone_number: "+44 091 xxx" }
```

`input.template(person)` returns
<!-- test-ignore -->
```graql
insert $person has phone-number "+44 091 xxx";
```

And given the person,

<!-- test-ignore -->
```java
{ firs-name: "Jackie", last-name: "Joe", city: "Jimo", age: 77, phone_number: "+00 091 xxx"}
```

`input.template(person)` returns
<!-- test-ignore -->
```graql
insert $person has phone-number "+44 091 xxx", has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

## Input Instance For a Contract

<!-- test-ignore -->
```java
// imports

public class PhoneCallsMigration {
  abstract static class Input {...}
  public static void main(String[] args) {...}

  static Collection<Input> initialiseInputs() {
    Collection<Input> inputs = new ArrayList<>();

    inputs.add(new Input("data/companies") {...});
    inputs.add(new Input("data/people") {...});

    inputs.add(new Input("data/contracts") {
      @Override
      public String template(Json contract) {
        // match company
        String graqlInsertQuery = "match $company isa company, has name " + contract.at("company_name") + ";";
        // match person
        graqlInsertQuery += " $customer isa person, has phone-number " + contract.at("person_id") + ";";
        // insert contract
        graqlInsertQuery += " insert (provider: $company, customer: $customer) isa contract;";
        return graqlInsertQuery;
      }
    });

    return inputs;
  }
}
```

`input.getDataPath()` returns `data/contracts`.

Given the contract,

```javascript
{ company_name: "Telecom", person_id: "+00 091 xxx" }
```

`input.template(contract)` returns
<!-- test-ignore -->
```graql
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

## Input Instance For a Call

<!-- test-ignore -->
```java
// imports

public class PhoneCallsMigration {
  abstract static class Input {...}
  public static void main(String[] args) {...}

  static Collection<Input> initialiseInputs() {
    Collection<Input> inputs = new ArrayList<>();

    inputs.add(new Input("data/companies") {...});
    inputs.add(new Input("data/people") {...});
    inputs.add(new Input("data/contracts") {...});

    inputs.add(new Input("data/calls") {
      @Override
      public String template(Json call) {
        // match caller
        String graqlInsertQuery = "match $caller isa person, has phone-number " + call.at("caller_id") + ";";
        // match callee
        graqlInsertQuery += " $callee isa person, has phone-number " + call.at("callee_id") + ";";
        // insert call
        graqlInsertQuery += " insert $call(caller: $caller, callee: $callee) isa call; $call has started-at " + call.at("started_at").asString() + "; $call has duration " + call.at("duration").asInteger() + ";";
        return graqlInsertQuery;
      }
    });

    return inputs;
  }
}
```

`input.getDataPath()` returns `data/calls`.

Given the call,

<!-- test-ignore -->
```java
{ caller_id: "+44 091 xxx", callee_id: "+00 091 xxx", started_at: 2018-08-10T07:57:51, duration: 148 }
```

`input.template(call)` returns
<!-- test-ignore -->
```graql
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

## Connect and Migrate

Now that we have the datapath and template defined for each of our data files, we can continue to connect with our ` ` knowledge graph and load the data into it.

<!-- test-ignore -->
```java
// other imports
import grakn.client.GraknClient;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlInsert;

public class Migration {
	abstract static class Input {...}

  	public static void main(String[] args) {
    	Collection<Input> inputs = initialiseInputs();
    	connectAndMigrate(inputs);
  	}

  	static void connectAndMigrate(Collection<Input> inputs) {
    	GraknClient client = new GraknClient("localhost:48555");
		GraknClient.Session session = client.session("phone_calls");

		for (Input input : inputs) {
			System.out.println("Loading from [" + input.getDataPath() + "] into Grakn ...");
			loadDataIntoGrakn(input, session);
		}

		session.close();
		client.close();
  	}

  	static Collection<Input> initialiseInputs() {...}
  	static void loadDataIntoGrakn(Input input, Grakn.Session session)
  	throws UnsupportedEncodingException {...}
}
```

`connectAndMigrate(Collection<Input> inputs)` is the only method that is fired to initiate migration of the data into the `phone_calls` knowledge graph.

The following happens in this method:

1. A Grakn Client instance `client` is created, connected to the server we have running locally at `localhost:48555`.
2. A `session` is created, connected to the keyspace `phone_calls`.
3. For each `input` object in the `inputs` collection, we call the `loadDataIntoGrakn(input, session)`. This takes care of loading the data as specified in the `input` object into our keyspace.
4. Finally, the `session` and `client` are both closed.

## Load the Data Into phone_calls

Now that we have a `session` connected to the `phone_calls` keyspace, we can move on to actually loading the data into our knowledge graph.

<!-- test-ignore -->
```java
// imports

public class PhoneCallsMigration {
	abstract static class Input {...}

  	public static void main(String[] args) {
    	Collection<Input> inputs = initialiseInputs();
    	connectAndMigrate(inputs);
  	}

  	static Collection<Input> initialiseInputs() {...}
  	static void connectAndMigrate(Collection<Input> inputs) {...}

  	static void loadDataIntoGrakn(Input input, Grakn.Session session) {
  	  	ArrayList<Json> items = parseDataToJson(input);
		for (Json item : items) {
			GraknClient.Transaction transaction = session.transaction(GraknClient.Transaction.Type.WRITE);
			String graqlInsertQuery = input.template(item);
			System.out.println("Executing Graql Query: " + graqlInsertQuery);
			transaction.execute((GraqlInsert) parse(graqlInsertQuery));
			transaction.commit();
		}
  		System.out.println("\nInserted " + items.size() + " items from [ " + input.getDataPath() + "] into Grakn.\n");
  	}

  	static ArrayList<Json> parseDataToJson(Input input) {...}
}
```

In order to load data from each file into Grakn, we need to:

1. retrieve an `ArrayList` of JSON objects, each of which represents a data item. We do this by calling `parseDataToJson(input)`, and
2. for each JSON object in `items`: a) create a `transaction`, b) construct the `graqlInsertQuery` using the corresponding `template`, c) run the `query` and d)`commit` the transaction.

<div class="note">
[Important]
To avoid running out of memory, it’s recommended that every single query gets created and committed in a single transaction.
However, for faster migration of large datasets, this can happen once for every `n` queries, where `n` is the maximum number of queries guaranteed to run on a single transaction.
</div>

Now that we have done all the above, we are ready to read each file and parse each data item to a JSON object. It’s these JSON objects that is be passed to the `template` method on each `Input` object.

We are going to write the implementation of `parseDataToJson(input)`.

## DataFormat-specific Implementation
The implementation for `parseDataToJson(input)` differs based on the format of our data files.

But regardless of what the data format is, we need the right setup to read the files line by line. For this, we use an `InputStreamReader`.

<!-- test-ignore -->
```java
// other imports
import java.io.InputStreamReader;
import java.io.Reader;


public class PhoneCallsMigration {
  	abstract static class Input {...}
  	public static void main(String[] args) {...}
  	static void connectAndMigrate(Collection<Input> inputs) {...}
  	static Collection<Input> initialiseInputs() {...}
  	static void loadDataIntoGrakn(Input input, Grakn.Session session){...}

  	public static Reader getReader(String relativePath) throws FileNotFoundException {
		return new InputStreamReader(new FileInputStream(relativePath));
	}
}
```

<div class="tabs light">

[tab:CSV]
We use the [Univocity CSV Parser](https://www.univocity.com/pages/univocity_parsers_documentation) for parsing our `.csv` files. Let’s add the dependency for it. We need to add the following to the `dependencies` tag in `pom.xml`.

```xml
&lt;dependency&gt;
	&lt;groupId&gt;com.univocity&lt;/groupId&gt;
  	&lt;artifactId&gt;univocity-parsers&lt;/artifactId&gt;
  	&lt;version&gt;2.7.6&lt;/version&gt;
&lt;/dependency&gt;
```

Having done that, we write the implementation of `parseDataToJson(input)` for parsing `.csv` files.

<!-- test-ignore -->
```java
// other imports

import com.univocity.parsers.csv.CsvParser;
import com.univocity.parsers.csv.CsvParserSettings;

public class PhoneCallsMigration {
    abstract static class Input {...}
    public static void main(String[] args) {...}
    static void connectAndMigrate(Collection&lt;Input&gt; inputs) {...}
    static Collection&lt;Input&gt; initialiseInputs() {...}
    static void loadDataIntoGrakn(Input input, Grakn.Session session) {...}

    static ArrayList&lt;Json&gt; parseDataToJson(Input input) throws FileNotFoundException {
        ArrayList&lt;Json&gt; items = new ArrayList<>();

        CsvParserSettings settings = new CsvParserSettings();
        settings.setLineSeparatorDetectionEnabled(true);
        CsvParser parser = new CsvParser(settings);
        parser.beginParsing(getReader(input.getDataPath() + ".csv"));

        String[] columns = parser.parseNext();
        String[] row;
        while ((row = parser.parseNext()) != null) {
            Json item = Json.object();
            for (int i = 0; i <row.length; i++) {
                item.set(columns[i], row[i]);
            }
            items.add(item);
        }
        return items;
    }

    public static Reader getReader(String relativePath) throws FileNotFoundException {...}
}
```

Besides this implementation, we need to make one more change.

Given the nature of CSV data, the JSON object produced has all the columns of the `.csv` file as its keys, even when the value is not there, it is taken as a `null`.

For this reason, we need to change one line in the `template` method for the `input` instance for person.

`if (! person.has("first_name")) {...}`

becomes

`if (person.at(“first_name”).isNull()) {...}`.

[tab:end]

[tab:JSON]
We’ll use [Gson’s JsonReader](https://google.github.io/gson/apidocs/com/google/gson/stream/JsonReader.html) for reading our `.json` files. Let’s add the dependency for it. We need to add the following to the `dependencies` tag in `pom.xml`.

```xml
&gt;dependency&gt;
	&lt;groupId&gt;com.google.code.gson&lt;/groupId&gt;
  	&lt;artifactId&gt;gson&lt;/artifactId&gt;
  	&lt;version&gt;2.7&lt;/version&gt;
&gt;/dependency&gt;
```

Having done that, we write the implementation of `parseDataToJson(input)` for reading `.json` files.

<!-- test-ignore -->
```java
// other imports
import com.google.gson.stream.JsonReader;

public class PhoneCallsMigration {
    abstract static class Input {...}
    public static void main(String[] args) {...}
    static void connectAndMigrate(Collection&lt;Input&gt; inputs) {...}
    static Collection&t;Input&gt; initialiseInputs() {...}
    static void loadDataIntoGrakn(Input input, Grakn.Session session) {...}

    static ArrayList&lt;Json&gt; parseDataToJson(Input input) throws IOException {
        ArrayList&lt;Json&gt; items = new ArrayList<>();

        JsonReader jsonReader = new JsonReader(getReader(input.getDataPath() + ".json"));

        jsonReader.beginArray();
        while (jsonReader.hasNext()) {
            jsonReader.beginObject();
            Json item = Json.object();
            while (jsonReader.hasNext()) {
                String key = jsonReader.nextName();
                switch (jsonReader.peek()) {
                    case STRING:
                        item.set(key, jsonReader.nextString());
                        break;
                    case NUMBER:
                        item.set(key, jsonReader.nextInt());
                        break;
                }
            }
            jsonReader.endObject();
            items.add(item);
        }
        jsonReader.endArray();
        return items;
    }

    public static Reader getReader(String relativePath) throws FileNotFoundException {...}
}
```
[tab:end]

[tab:XML]
We use Java’s built-in [StAX](https://docs.oracle.com/cd/E13222_01/wls/docs90/xml/stax.html) for parsing our `.xml` files.

For parsing XML data, we need to know the name of the target tag. This needs to be declared in the `Input` class and specified when constructing each `input` object.

<!-- test-ignore -->
```java
// imports

public class PhoneCallsMigration {
    abstract static class Input {
        String path;
        String selector;
        public Input(String path, String selector) {
            this.path = path;
            this.selector = selector;
        }
        String getDataPath(){ return path;}
        String getSelector(){ return selector;}
        abstract String template(Json data);
    }

    public static void main(String[] args)  {...}
	static void connectAndMigrate(Collection&lt;Input&gt; inputs) {...}

    static Collection&lt;Input&gt; initialiseInputs() {
        Collection&lt;Input&gt; inputs = new ArrayList<>();

        inputs.add(new Input("data/companies", "company") {...});
        inputs.add(new Input("data/people", "person") {...});
        inputs.add(new Input("data/contracts", "contract") {...});
        inputs.add(new Input("data/calls", "call") {...});

        return inputs;
    }

    static void loadDataIntoGrakn(Input input, Grakn.Session session) {...}

    public static Reader getReader(String relativePath) throws FileNotFoundException {...}
}
```

And now for the implementation of `parseDataToJson(input)` for parsing `.xml` files.

<!-- test-ignore -->
```java
// other imports
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;

public class XmlMigration {
    abstract static class Input {
        String path;
        String selector;
        public Input(String path, String selector) {
            this.path = path;
            this.selector = selector;
        }
        String getDataPath(){ return path;}
        String getSelector(){ return selector;}
        abstract String template(Json data);
    }

    public static void main(String[] args)  {...}
    static void connectAndMigrate(Collection&lt;Input&gt; inputs) {...}

    static Collection&lt;Input&gt; initialiseInputs() {
        Collection&lt;Input&gt; inputs = new ArrayList<>();

        inputs.add(new Input("data/companies", "company") {...});
        inputs.add(new Input("data/people", "person") {...});
        inputs.add(new Input("data/contracts", "contract") {...});
        inputs.add(new Input("data/calls", "call") {...});

        return inputs;
    }

    static void loadDataIntoGrakn(Input input, Grakn.Session session) {...}

    static ArrayList&lt;Json&gt; parseDataToJson(Input input) throws FileNotFoundException, XMLStreamException {
        ArrayList&lt;Json&gt; items = new ArrayList<>();

        XMLStreamReader r = XMLInputFactory.newInstance().createXMLStreamReader(getReader(input.getDataPath() + ".xml"));
        String key;
        String value = null;
        Boolean inSelector = false;
        Json item = null;
        while(r.hasNext()) {
            int event = r.next();

            switch (event) {
                case XMLStreamConstants.START_ELEMENT:
                    if (r.getLocalName().equals(input.getSelector())) {
                        inSelector = true;
                        item = Json.object();
                    }
                    break;

                case XMLStreamConstants.CHARACTERS:
                    value = r.getText();
                    break;

                case XMLStreamConstants.END_ELEMENT:
                    key = r.getLocalName();
                    if (inSelector && ! key.equals(input.getSelector())) {
                        item.set(key, value);
                    }
                    if (key.equals(input.getSelector())) {
                        inSelector = false;
                        items.add(item);
                    }

                    break;
            }
        }
        return items;
	}

    public static Reader getReader(String relativePath) throws FileNotFoundException {...}
}
```
[tab:end]

</div>

## Putting It All Together
Here is how our `Migrate.java` looks like for each data format.

<div class="tabs dark">

[tab:CSV]
<!-- test-example PhoneCallsCSVMigration.java -->
```java
package grakn.example.phoneCalls;

import grakn.client.GraknClient;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlInsert;

/**
 * a collection of fast and reliable Java-based parsers for CSV, TSV and Fixed Width files
 * @see <a href="https://www.univocity.com/pages/univocity_parsers_documentation">univocity</a>
 */
import com.univocity.parsers.csv.CsvParser;
import com.univocity.parsers.csv.CsvParserSettings;

/**
 * a lean JSON Library for Java,
 * @see <a href="https://bolerio.github.io/mjson/">mjson</a>
 */
import mjson.Json;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;

public class PhoneCallsCSVMigration {
    /**
     * representation of Input object that links an input file to its own templating function,
     * which is used to map a Json object to a Graql query string
     */
    abstract static class Input {
        String path;

        public Input(String path) {
            this.path = path;
        }

        String getDataPath() {
            return path;
        }

        abstract String template(Json data);
    }

    /**
     * 1. creates a Grakn instance
     * 2. creates a session to the targeted keyspace
     * 3. initialises the list of Inputs, each containing details required to parse the data
     * 4. loads the csv data to Grakn for each file
     * 5. closes the session
     */
    public static void main(String[] args) throws FileNotFoundException {
        Collection<Input> inputs = initialiseInputs();
        connectAndMigrate(inputs);
    }

    static void connectAndMigrate(Collection<Input> inputs) throws FileNotFoundException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");

        for (Input input : inputs) {
            System.out.println("Loading from [" + input.getDataPath() + "] into Grakn ...");
            loadDataIntoGrakn(input, session);
        }

        session.close();
        client.close();
    }

    static Collection<Input> initialiseInputs() {
        Collection<Input> inputs = new ArrayList<>();

        // define template for constructing a company Graql insert query
        inputs.add(new Input("files/phone-calls/data/companies") {
            @Override
            public String template(Json company) {
                return "insert $company isa company, has name " + company.at("name") + ";";
            }
        });
        // define template for constructing a person Graql insert query
        inputs.add(new Input("files/phone-calls/data/people") {
            @Override
            public String template(Json person) {
                // insert person
                String graqlInsertQuery = "insert $person isa person, has phone-number " + person.at("phone_number");

                if (person.at("first_name").isNull()) {
                    // person is not a customer
                    graqlInsertQuery += ", has is-customer false";
                } else {
                    // person is a customer
                    graqlInsertQuery += ", has is-customer true";
                    graqlInsertQuery += ", has first-name " + person.at("first_name");
                    graqlInsertQuery += ", has last-name " + person.at("last_name");
                    graqlInsertQuery += ", has city " + person.at("city");
                    graqlInsertQuery += ", has age " + person.at("age").asInteger();
                }

                graqlInsertQuery += ";";
                return graqlInsertQuery;
            }
        });
        // define template for constructing a contract Graql insert query
        inputs.add(new Input("files/phone-calls/data/contracts") {
            @Override
            public String template(Json contract) {
                // match company
                String graqlInsertQuery = "match $company isa company, has name " + contract.at("company_name") + ";";
                // match person
                graqlInsertQuery += " $customer isa person, has phone-number " + contract.at("person_id") + ";";
                // insert contract
                graqlInsertQuery += " insert (provider: $company, customer: $customer) isa contract;";
                return graqlInsertQuery;
            }
        });
        // define template for constructing a call Graql insert query
        inputs.add(new Input("files/phone-calls/data/calls") {
            @Override
            public String template(Json call) {
                // match caller
                String graqlInsertQuery = "match $caller isa person, has phone-number " + call.at("caller_id") + ";";
                // match callee
                graqlInsertQuery += " $callee isa person, has phone-number " + call.at("callee_id") + ";";
                // insert call
                graqlInsertQuery += " insert $call(caller: $caller, callee: $callee) isa call;" +
                        " $call has started-at " + call.at("started_at").asString() + ";" +
                        " $call has duration " + call.at("duration").asInteger() + ";";
                return graqlInsertQuery;
            }
        });
        return inputs;
    }

    /**
     * loads the csv data into our Grakn phone_calls keyspace:
     * 1. gets the data items as a list of json objects
     * 2. for each json object
     * a. creates a Grakn transaction
     * b. constructs the corresponding Graql insert query
     * c. runs the query
     * d. commits the transaction
     * e. closes the transaction
     *
     * @param input   contains details required to parse the data
     * @param session off of which a transaction is created
     * @throws UnsupportedEncodingException
     */
    static void loadDataIntoGrakn(Input input, GraknClient.Session session) throws FileNotFoundException {
        ArrayList<Json> items = parseDataToJson(input); // 1
        for (Json item : items) {
            GraknClient.Transaction transaction = session.transaction().write(); // 2a
            String graqlInsertQuery = input.template(item); // 2b
            System.out.println("Executing Graql Query: " + graqlInsertQuery);
            transaction.execute((GraqlInsert) parse(graqlInsertQuery)); // 2c
            transaction.commit(); // 2d

        }
        System.out.println("\nInserted " + items.size() + " items from [ " + input.getDataPath() + "] into Grakn.\n");
    }

    /**
     * 1. reads a csv file through a stream
     * 2. parses each row to a json object
     * 3. adds the json object to the list of items
     *
     * @param input used to get the path to the data file, minus the format
     * @return the list of json objects
     * @throws UnsupportedEncodingException
     */
    static ArrayList<Json> parseDataToJson(Input input) throws FileNotFoundException {
        ArrayList<Json> items = new ArrayList<>();

        CsvParserSettings settings = new CsvParserSettings();
        settings.setLineSeparatorDetectionEnabled(true);
        CsvParser parser = new CsvParser(settings);
        parser.beginParsing(getReader(input.getDataPath() + ".csv")); // 1

        String[] columns = parser.parseNext();
        String[] row;
        while ((row = parser.parseNext()) != null) {
            Json item = Json.object();
            for (int i = 0; i < row.length; i++) {
                item.set(columns[i], row[i]); // 2
            }
            items.add(item); // 3
        }
        return items;
    }

    public static Reader getReader(String relativePath) throws FileNotFoundException {
        return new InputStreamReader(new FileInputStream(relativePath));
    }
}

```
[tab:end]

[tab:JSON]
<!-- test-example PhoneCallsJSONMigration.java -->
```java
package grakn.example.phoneCalls;

import grakn.client.GraknClient;
import static graql.lang.Graql.*;
import graql.lang.query.GraqlInsert;

/**
 * reads a JSON encoded value as a stream of tokens,
 * @see <a href="https://google.github.io/gson/apidocs/com/google/gson/stream/JsonReader.html">JsonReader</a>
 */
import com.google.gson.stream.JsonReader;

/**
 * a lean JSON Library for Java,
 * @see <a href="https://bolerio.github.io/mjson/">mjson</a>
 */
import mjson.Json;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;

public class PhoneCallsJSONMigration {
    /**
     * representation of Input object that links an input file to its own templating function,
     * which is used to map a Json object to a Graql query string
     */
    abstract static class Input {
        String path;

        public Input(String path) {
            this.path = path;
        }

        String getDataPath() {
            return path;
        }

        abstract String template(Json data);
    }

    /**
     * 1. creates a Grakn instance
     * 2. creates a session to the targeted keyspace
     * 3. initialises the list of Inputs, each containing details required to parse the data
     * 4. loads the csv data to Grakn for each file
     * 5. closes the session
     */
    public static void main(String[] args) throws IOException {
        Collection<Input> inputs = initialiseInputs();
        connectAndMigrate(inputs);
    }

    static void connectAndMigrate(Collection<Input> inputs) throws IOException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");

        for (Input input : inputs) {
            System.out.println("Loading from [" + input.getDataPath() + "] into Grakn ...");
            loadDataIntoGrakn(input, session);
        }

        session.close();
        client.close();
    }

    static Collection<Input> initialiseInputs() {
        Collection<Input> inputs = new ArrayList<>();

        // define template for constructing a company Graql insert query
        inputs.add(new Input("files/phone-calls/data/companies") {
            @Override
            public String template(Json company) {
                return "insert $company isa company, has name " + company.at("name") + ";";
            }
        });
        // define template for constructing a person Graql insert query
        inputs.add(new Input("files/phone-calls/data/people") {
            @Override
            public String template(Json person) {
                // insert person
                String graqlInsertQuery = "insert $person isa person, has phone-number " + person.at("phone_number");

                if (! person.has("first_name")) {
                    // person is not a customer
                    graqlInsertQuery += ", has is-customer false";
                } else {
                    // person is a customer
                    graqlInsertQuery += ", has is-customer true";
                    graqlInsertQuery += ", has first-name " + person.at("first_name");
                    graqlInsertQuery += ", has last-name " + person.at("last_name");
                    graqlInsertQuery += ", has city " + person.at("city");
                    graqlInsertQuery += ", has age " + person.at("age").asInteger();
                }

                graqlInsertQuery += ";";
                return graqlInsertQuery;
            }
        });
        // define template for constructing a contract Graql insert query
        inputs.add(new Input("files/phone-calls/data/contracts") {
            @Override
            public String template(Json contract) {
                // match company
                String graqlInsertQuery = "match $company isa company, has name " + contract.at("company_name") + ";";
                // match person
                graqlInsertQuery += " $customer isa person, has phone-number " + contract.at("person_id") + ";";
                // insert contract
                graqlInsertQuery += " insert (provider: $company, customer: $customer) isa contract;";
                return graqlInsertQuery;
            }
        });
        // define template for constructing a call Graql insert query
        inputs.add(new Input("files/phone-calls/data/calls") {
            @Override
            public String template(Json call) {
                // match caller
                String graqlInsertQuery = "match $caller isa person, has phone-number " + call.at("caller_id") + ";";
                // match callee
                graqlInsertQuery += " $callee isa person, has phone-number " + call.at("callee_id") + ";";
                // insert call
                graqlInsertQuery += " insert $call(caller: $caller, callee: $callee) isa call;" +
                        " $call has started-at " + call.at("started_at").asString() + ";" +
                        " $call has duration " + call.at("duration").asInteger() + ";";
                return graqlInsertQuery;
            }
        });
        return inputs;
    }

    /**
     * loads the csv data into our Grakn phone_calls keyspace:
     * 1. gets the data items as a list of json objects
     * 2. for each json object
     * a. creates a Grakn transaction
     * b. constructs the corresponding Graql insert query
     * c. runs the query
     * d. commits the transaction
     * e. closes the transaction
     *
     * @param input   contains details required to parse the data
     * @param session off of which a transaction is created
     * @throws UnsupportedEncodingException
     */
    static void loadDataIntoGrakn(Input input, GraknClient.Session session) throws IOException {
        ArrayList<Json> items = parseDataToJson(input); // 1
        for (Json item : items) {
            GraknClient.Transaction transaction = session.transaction().write(); // 2a
            String graqlInsertQuery = input.template(item); // 2b
            System.out.println("Executing Graql Query: " + graqlInsertQuery);
            transaction.execute((GraqlInsert) parse(graqlInsertQuery)); // 2c
            transaction.commit(); // 2d

        }
        System.out.println("\nInserted " + items.size() + " items from [ " + input.getDataPath() + "] into Grakn.\n");
    }

    /**
     * 1. reads a json file through a stream
     * 2. parses each json object found in the file to a json object
     * 3. adds the json object to the list of items
     *
     * @param input used to get the path to the data file, minus the format
     * @return the list of json objects
     * @throws IOException
     */
    static ArrayList <Json> parseDataToJson(Input input) throws IOException {
        ArrayList <Json> items = new ArrayList <> ();

        JsonReader jsonReader = new JsonReader(getReader(input.getDataPath() + ".json")); // 1

        jsonReader.beginArray();
        while (jsonReader.hasNext()) {
            jsonReader.beginObject();
            Json item = Json.object();
            while (jsonReader.hasNext()) {
                String key = jsonReader.nextName();
                switch (jsonReader.peek()) {
                    case STRING:
                        item.set(key, jsonReader.nextString()); // 2
                        break;
                    case NUMBER:
                        item.set(key, jsonReader.nextInt()); // 2
                        break;
                }
            }
            jsonReader.endObject();
            items.add(item); // 3
        }
        jsonReader.endArray();
        return items;
    }

    public static Reader getReader(String relativePath) throws FileNotFoundException {
        return new InputStreamReader(new FileInputStream(relativePath));
    }
}

```
[tab:end]

[tab:XML]
<!-- test-example PhoneCallsXMLMigration.java -->
```java
package grakn.example.phoneCalls;

import grakn.client.GraknClient;
import graql.lang.query.GraqlInsert;
import static graql.lang.Graql.*;

/**
 * a lean JSON Library for Java,
 * @see <a href="https://bolerio.github.io/mjson/">mjson</a>
 */
import mjson.Json;

/**
 * provides an easy and intuitive means of parsing and generating XML documents
 * @see <a href="https://docs.oracle.com/cd/E13222_01/wls/docs90/xml/stax.html">StAX</a>
 */
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;

public class PhoneCallsXMLMigration {
    /**
     * representation of Input object that links an input file to its own templating function,
     * which is used to map a Json object to a Graql query string
     */
    abstract static class Input {
        String path;
        String selector;

        public Input(String path, String selector) {
            this.path = path;
            this.selector = selector;
        }

        String getDataPath(){ return path;}
        String getSelector(){ return selector;}

        abstract String template(Json data);
    }

    /**
     * 1. creates a Grakn instance
     * 2. creates a session to the targeted keyspace
     * 3. initialises the list of Inputs, each containing details required to parse the data
     * 4. loads the csv data to Grakn for each file
     * 5. closes the session
     */
    public static void main(String[] args) throws FileNotFoundException, XMLStreamException {
        Collection<Input> inputs = initialiseInputs();
        connectAndMigrate(inputs);
    }

    static void connectAndMigrate(Collection<Input> inputs) throws FileNotFoundException, XMLStreamException {
        GraknClient client = new GraknClient("localhost:48555");
        GraknClient.Session session = client.session("phone_calls");

        for (Input input : inputs) {
            System.out.println("Loading from [" + input.getDataPath() + "] into Grakn ...");
            loadDataIntoGrakn(input, session);
        }

        session.close();
        client.close();
    }

    static Collection<Input> initialiseInputs() {
        Collection<Input> inputs = new ArrayList<>();

        // define template for constructing a company Graql insert query
        inputs.add(new Input("files/phone-calls/data/companies", "company") {
            @Override
            public String template(Json company) {
                return "insert $company isa company, has name " + company.at("name") + ";";
            }
        });
        // define template for constructing a person Graql insert query
        inputs.add(new Input("files/phone-calls/data/people", "person") {
            @Override
            public String template(Json person) {
                // insert person
                String graqlInsertQuery = "insert $person isa person, has phone-number " + person.at("phone_number");

                if (! person.has("first_name")) {
                    // person is not a customer
                    graqlInsertQuery += ", has is-customer false";
                } else {
                    // person is a customer
                    graqlInsertQuery += ", has is-customer true";
                    graqlInsertQuery += ", has first-name " + person.at("first_name");
                    graqlInsertQuery += ", has last-name " + person.at("last_name");
                    graqlInsertQuery += ", has city " + person.at("city");
                    graqlInsertQuery += ", has age " + person.at("age").asInteger();
                }

                graqlInsertQuery += ";";
                return graqlInsertQuery;
            }
        });
        // define template for constructing a contract Graql insert query
        inputs.add(new Input("files/phone-calls/data/contracts", "contract") {
            @Override
            public String template(Json contract) {
                // match company
                String graqlInsertQuery = "match $company isa company, has name " + contract.at("company_name") + ";";
                // match person
                graqlInsertQuery += " $customer isa person, has phone-number " + contract.at("person_id") + ";";
                // insert contract
                graqlInsertQuery += " insert (provider: $company, customer: $customer) isa contract;";
                return graqlInsertQuery;
            }
        });
        // define template for constructing a call Graql insert query
        inputs.add(new Input("files/phone-calls/data/calls", "call") {
            @Override
            public String template(Json call) {
                // match caller
                String graqlInsertQuery = "match $caller isa person, has phone-number " + call.at("caller_id") + ";";
                // match callee
                graqlInsertQuery += " $callee isa person, has phone-number " + call.at("callee_id") + ";";
                // insert call
                graqlInsertQuery += " insert $call(caller: $caller, callee: $callee) isa call;" +
                        " $call has started-at " + call.at("started_at").asString() + ";" +
                        " $call has duration " + call.at("duration").asInteger() + ";";
                return graqlInsertQuery;
            }
        });
        return inputs;
    }

    /**
     * loads the xml data into the Grakn phone_calls keyspace:
     * 1. gets the data items as a list of json objects
     * 2. for each json object:
     *   a. creates a Grakn transaction
     *   b. constructs the corresponding Graql insert query
     *   c. runs the query
     *   d. commits the transaction
     *
     * @param input   contains details required to parse the data
     * @param session off of which a transaction is created
     * @throws UnsupportedEncodingException
     */
    static void loadDataIntoGrakn(Input input, GraknClient.Session session) throws FileNotFoundException, XMLStreamException {
        ArrayList<Json> items = parseDataToJson(input); // 1
        for (Json item : items) {
            GraknClient.Transaction transaction = session.transaction().write(); // 2a
            String graqlInsertQuery = input.template(item); // 2b
            System.out.println("Executing Graql Query: " + graqlInsertQuery);
            transaction.execute((GraqlInsert) parse(graqlInsertQuery)); // 2c
            transaction.commit(); // 2d

        }
        System.out.println("\nInserted " + items.size() + " items from [ " + input.getDataPath() + "] into Grakn.\n");
    }

    /**
     * 1. reads a xml file through a stream
     * 2. parses each tag to a json object
     * 3. adds the json object to the list of items
     *
     * @param input used to get the path to the data file (minus the format) and the tag selector
     * @return the list of json objects
     * @throws UnsupportedEncodingException
     */
    static ArrayList <Json> parseDataToJson(Input input) throws FileNotFoundException, XMLStreamException {
        ArrayList <Json> items = new ArrayList <> ();

        XMLStreamReader r = XMLInputFactory.newInstance().createXMLStreamReader(getReader(input.getDataPath() + ".xml")); // 1
        String key;
        String value = null;
        Boolean inSelector = false;
        Json item = null;
        while (r.hasNext()) {
            int event = r.next();

            switch (event) {
                case XMLStreamConstants.START_ELEMENT:
                    if (r.getLocalName().equals(input.getSelector())) {
                        inSelector = true;
                        item = Json.object();
                    }
                    break;

                case XMLStreamConstants.CHARACTERS:
                    value = r.getText();
                    break;

                case XMLStreamConstants.END_ELEMENT:
                    key = r.getLocalName();
                    if (inSelector && !key.equals(input.getSelector())) {
                        item.set(key, value); // 2
                    }
                    if (key.equals(input.getSelector())) {
                        inSelector = false;
                        items.add(item); // 3
                    }

                    break;
            }
        }

        return items;
    }

    public static Reader getReader(String relativePath) throws FileNotFoundException {
        return new InputStreamReader(new FileInputStream(relativePath));
    }
}

```
[tab:end]
</div>

## Time to Load

Run the main method, sit back, relax and watch the logs while the data starts pouring into Grakn.

### ... So Far With the Migration

We started off by setting up our project and positioning the data files.

Next, we went on to set up the migration mechanism, one that was independent of the data format.

Then, we learned how files with different data formats can be parsed into JSON objects.

Lastly, we ran the `main` method which fired the `connectAndMigrate` method with the given `inputs`. This loaded the data into our Grakn knowledge graph.

## Next

Now that we have some actual data in our knowledge graph, we can go ahead and [query for insights](../08-examples/05-phone-calls-queries.md?tab=java).