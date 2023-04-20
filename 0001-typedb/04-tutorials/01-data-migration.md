---
pageTitle: Data migration tutorial
keywords: typedb, data, dataset, load, import
longTailKeywords: TypeDB load data, dataset load, import data
Summary: A basic tutorial to load data into a TypeDB database.
---

# Data migration tutorial

Migrating data from other sources into TypeDB is an important step. It is considered that we have already 
developed a [schema](../02-dev/02-schema.md) for the TypeDB database according to the data model. Accurate and 
comprehensive schema design will simplify not only data migration but also the design of data queries later on.

<div class="note">
[Note]
This tutorial is based on the **Phone calls** example in [TypeDB Examples](https://github.com/vaticle/typedb-examples) 
repository. Advanced users may find it faster to follow the readme files for 
[Java](https://github.com/vaticle/typedb-examples/tree/master/telecom/phone_calls/java#quickstart), 
[Python](https://github.com/vaticle/typedb-examples/tree/master/telecom/phone_calls/python#quickstart), 
[Node.js](https://github.com/vaticle/typedb-examples/tree/master/telecom/phone_calls/nodejs#quickstart) versions 
directly.
</div>

To load data into a TypeDB database we need to perform [insert](../02-dev/04-write.md#insert-query) queries. 
The following [example](#application) showcases how to load 
[sample data](#dataset) from `CSV`, `JSON`, and `XML` formats using TypeDB Clients for 
[Java](#java), 
[Python](#python), and 
[Node.js](#nodejs). 

The same approach could be used to load data from other sources (e.g. from REST API, or other DB engines using SQL, 
GraphQL, etc.) or using other [TypeDB Clients](../../02-clients/00-clients.md).

## Schema & data

The application described on this page is built to migrate and use the `phone_calls` database schema and dataset, 
which are both provided below.

### Schema

The schema of the `phone_calls` database is defined by the following file:

[schema.tql](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/schema.tql).

See the visualization below.

![phone_calls_schema](../../images/examples/phone_calls_schema.png "phone_calls_schema")

The schema in the file above consists of the following types.

**Entity** types:

* `person`
    * owns `first-name` attribute type
    * owns `last-name` attribute type
    * owns `phone-number` attribute type
    * owns `city` attribute type
    * owns `age` attribute type
    * owns `started-at` attribute type
    * owns `duration` attribute type
* `company`
    * owns `name` attribute type

**Relation** types:

* `call`
    * role `caller` played by `person` type
    * role `callee` played by `person` type
* `contract`
    * role `customer` played by `person` type
    * role `provider` played by `company` type

**Attribute** types:

* `first-name` of `string` value type
* `last-name` of `string` value type
* `phone-number` of `string` value type
* `city` of `string` value type
* `age` of `long` value type
* `started-at` of `datetime` value type
* `duration` of `long` value type
* `name` of `string` value type

Use TypeDB Studio or any other TypeDB Client to create a new database named `phone_calls` in a TypeDB server and 
import the schema [file](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/schema.tql). 
The instructions how to create a database and load a schema with TypeDB Studio can be found in the 
[Quickstart guide](../01-start/03-quickstart.md) 
(make sure to use the schema file above instead of the IAM schema code/file).

### Dataset

Sample data for this example is available in three different formats below.


<!--  
This syntax doesn't work for a single row table without titles:
| **CSV** | [calls.csv](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.csv) | [companies.csv](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.csv) | [contracts.csv](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.csv) | [people.csv](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.csv) |
--->

#### CSV

<table>
  <tr>
   <td> CSV
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.csv">calls.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.csv">companies.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.csv">contracts.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.csv">people.csv</a>
   </td>
  </tr>
</table>

#### JSON

<table>
  <tr>
   <td>JSON
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.json">calls.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.json">companies.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.json">contracts.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.json">people.json</a>
   </td>
  </tr>
</table>

#### XML

<table>
  <tr>
   <td> XML
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.xml">calls.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.xml">companies.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.xml">contracts.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.xml">people.xml</a>
   </td>
  </tr>
</table>

## Application

In this example we will conduct migration by building an application to read through dataset files above and insert 
data into the TypeDB database created. 

The Phone Calls example application showcases:

* importing data into a TypeDB database from:
    * [CSV](#csv)
    * [JSON](#json)
    * [XML](#xml)
* performing TypeQL queries to the database with imported data.

### Prerequirements

Use TypeDB server (v.**2.11.1+**), Java version **11+** and any IDE, for example, IntelliJ IDEA.

| App technology  | Prerequirements                                                                                                                 |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------|
| Java            | To use this sample application the following software needs to be installed: `Bazel` (v5.1.1)                                   |
| Python          | To use this sample application the following software needs to be installed: `Node.js` (v16.16.0 LTS) and `npm` package manager |
| Node.js         | To use this sample application the following software needs to be installed: `Python` (v.3.10.5+) and `pip` package manager     |

### Java

#### Clone the repository

Clone the [TypeDB Examples](https://github.com/vaticle/typedb-examples) repository to the local machine.

#### Start migration

Build the example with the `bazel build //telecom/phone_calls/java/...` command.

Use one of the following commands, depending on the chosen input format:

* `bazel run //telecom/phone_calls/java:csv-migration`
* `bazel run //telecom/phone_calls/java:json-migration`
* `bazel run //telecom/phone_calls/java:xml-migration`

#### Application logic

Data migration code is located inside `{format}Migration.java` file, where {format} is 
[CSV](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/java/CSVMigration.java), 
[JSON](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/java/JSONMigration.java), or 
[XML](https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/java/XMLMigration.java).

The `{format}Migration` class calls the `initialiseInputs()` method, which returns a collection of `Input` called 
`inputs`. We then use each element in this collection to load each file from dataset into TypeDB database with 
`connectAndMigrate(Collection&lt;Input> inputs)` method.

The `Input` subclass contains details required for reading data from dataset files of a chosen format: 
**path to the file** and the **template** function to produce a TypeQL insert **query** out of every element of the 
file. Thus, for every file, there is a separate template for forming a TypeQL insert query using the data from the 
file.

The `connectAndMigrate` initializes TypeDB Java Client, opens a session to the TypeDB database, and calls 
`loadDataIntoTypeDB` for every element in `inputs`.

The `loadDataIntoTypeDB` parses the data from a file using a path from the `inputs` element, and for every item 
parsed from the dataset file it calls `input.template` function (which is specific for this file, defined by its path). 
Template returns a TypeQL insert query in a form of a **string** and it then is sent as a part of a write transaction 
to the TypeDB database.

#### Insert query examples

To insert an instance of a `company` type we have the following template:

<!-- test-ignore -->
```java
inputs.add(new Input("data/companies") {
      @Override
      public String template(Json company) {
        return "insert $company isa company, has name " + company.at("name") + ";";
      }
```

`input.getDataPath()` returns `data/companies`.

Given the `company` item is:

<!-- test-ignore -->
```json
{ name: "Telecom" }
```

`input.template(company)` returns:

<!-- test-ignore -->
```typeql
insert $company isa company, has name "Telecom";
```

To insert an instance of a `person` type we have the following template:

<!-- test-ignore -->
```java
inputs.add(new Input("data/people") {
    @Override
    public String template(Json person) {
        // insert person
        String typeQLInsertQuery = "insert $person isa person, has phone-number " + person.at("phone_number");
        if (! person.at("first_name").isNull()) {
            typeQLInsertQuery += ", has first-name " + person.at("first_name");
            typeQLInsertQuery += ", has last-name " + person.at("last_name");
            typeQLInsertQuery += ", has city " + person.at("city");
            typeQLInsertQuery += ", has age " + person.at("age").asInteger();
        }

        typeQLInsertQuery += ";";
        return typeQLInsertQuery;
    }
```

Given the `person` item is:

<!-- test-ignore -->
```json
{ firs-name: "Jackie", last-name: "Joe", city: "Jimo", age: 77, phone_number: "+00 091 xxx"}
```

`input.template(person)` returns:

<!-- test-ignore -->
```typeql
insert $person isa person, has phone-number "+44 091 xxx", has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

if the person item doesn't have `first-name`:

<!-- test-ignore -->
```json
{ phone_number: "+44 091 xxx" }
```

`input.template(person)` returns:

<!-- test-ignore -->
```typeql
insert $person isa person, has phone-number "+44 091 xxx";
```

But those were entities. To insert a relation we need to use `match` clause to find related instances first.

For example, to insert an instance of a `contract` type we have the following template:

<!-- test-ignore -->
```java
inputs.add(new Input("data/contracts") {
    @Override
    public String template(Json contract) {
        // match company
        String typeQLInsertQuery = "match $company isa company, has name " + contract.at("company_name") + ";";
        // match person
        typeQLInsertQuery += " $customer isa person, has phone-number " + contract.at("person_id") + ";";
        // insert contract
        typeQLInsertQuery += " insert (provider: $company, customer: $customer) isa contract;";
        return typeQLInsertQuery;
    }
```

Given the contract item is:

<!-- test-ignore -->
```json
{ company_name: "Telecom", person_id: "+00 091 xxx" }
```

`input.template(contract)` returns:

<!-- test-ignore -->
```typeql
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

Finally, to insert an instance of a `call` type we have the following template:

<!-- test-ignore -->
```java
inputs.add(new Input("data/calls") {
    @Override
    public String template(Json call) {
        // match caller
        String typeQLInsertQuery = "match $caller isa person, has phone-number " + call.at("caller_id") + ";";
        // match callee
        typeQLInsertQuery += " $callee isa person, has phone-number " + call.at("callee_id") + ";";
        // insert call
        typeQLInsertQuery += " insert $call(caller: $caller, callee: $callee) isa call;" +
                " $call has started-at " + call.at("started_at").asString() + ";" +
                " $call has duration " + call.at("duration").asInteger() + ";";
        return typ
```

Given the call item is:

<!-- test-ignore -->
```json
{ caller_id: "+44 091 xxx", callee_id: "+00 091 xxx", started_at: 2018-08-10T07:57:51, duration: 148 }
```

`input.template(call)` returns:

<!-- test-ignore -->
```typeql
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

#### Performing queries

Use the `bazel run //telecom/phone_calls/java:queries` command to perform simple queries to the database. Run it and 
follow the instructions in the console.

### Python

To migrate the sample dataset into the TypeDB database `phone_calls` follow the steps below. Alternatively, 
clone the [TypeDB repository](https://github.com/vaticle/typedb-examples) and follow the readme file in the 
`telecom/phone_calls/python` directory.

#### Copy the dataset

Create a new directory on the local machine.

Choose one of the input formats, download the files, and place them in the new directory inside a subdirectory named `data`.

<table>
  <tr>
   <td>CSV
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.csv">calls.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.csv">companies.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.csv">contracts.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.csv">people.csv</a>
   </td>
  </tr>
</table>

<table>
  <tr>
   <td>JSON
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.json">calls.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.json">companies.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.json">contracts.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.json">people.json</a>
   </td>
  </tr>
</table>

<table>
  <tr>
   <td>XML
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.xml">calls.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.xml">companies.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.xml">contracts.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.xml">people.xml</a>
   </td>
  </tr>
</table>

#### Copy the source codes

Copy the following source files from the `telecom/phone_calls` directory in the 
[TypeDB Examples](https://github.com/vaticle/typedb-examples) repository into the new directory:

* migrate_csv.py
* migrate_json.py
* migrate_xml.py
* queries.py
* requirements.txt

#### Start migration

Use `pip install -r requirements.txt` to install required dependencies.

Use one of the following commands, depending on the chosen input format:

* `python migrate_csv.py`
* `python migrate_json.py`
* `python migrate_xml.py`

#### Application logic

Data migration code is located inside `migrate_{format}.py` file, where {format} is `csv`, `json`, or `xml`.

The `build_phone_call_graph()` function initializes TypeDB Python Client, opens a session to the TypeDB database, and 
for every element of `inputs` calls `load_data_into_typedb()` function.

The `load_data_into_typedb()` function calls for `parse_data_to_dictionaries()` to parse through the dataset file and 
then iterates through parsed records of the file. For every record it opens a transaction, forms an insert query by 
calling the template function, then sends the insert query and commits the transaction. 

The rest of the file is: 

* the parsing function `parse_data_to_dictionaries()`, 
* the `Inputs` list, 
* and the template functions.

The parsing function parses data from a dataset file into a list of dictionaries. The implementation of the function 
is different for every input format.

The `Inputs` is inserted as `inputs` argument and contains a list of dictionaries with `file` field containing 
filename (without an extension) and `template` field, containing a reference to the template function to process 
the file. 

The template functions are the most important part, as they are needed to create TypeQL insert queries from 
information parsed from dataset files.

#### Insert query examples

To insert an instance of a `company` type we have the following template:

<!-- test-ignore -->
```python
def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'
```

Example:

Given the `company` item is:

<!-- test-ignore -->
```json
{ "name": "Telecom" }
```

Returns:

<!-- test-ignore -->
```typeql
insert $company isa company, has name "Telecom";
```

To insert an instance of a `person` type we have the following template:

<!-- test-ignore -->
```python
def person_template(person):
    # insert person
    typeql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if "first_name" in person:
        # person is a customer
        typeql_insert_query += ", has is-customer true"
        typeql_insert_query += ', has first-name "' + person["first_name"] + '"'
        typeql_insert_query += ', has last-name "' + person["last_name"] + '"'
        typeql_insert_query += ', has city "' + person["city"] + '"'
        typeql_insert_query += ", has age " + str(person["age"])
    else:
        # person is not a customer
        typeql_insert_query += ", has is-customer false"
    typeql_insert_query += ";"
    return typeql_insert_query
```

Example:

Given the `person` item is:

<!-- test-ignore -->
```json
{ "phone_number": "+44 091 xxx" }
```

Returns:

<!-- test-ignore -->
```typeql
insert $person isa person, has phone-number "+44 091 xxx", has is-customer false;
```

or:

Given the `person` item is:

<!-- test-ignore -->
```json
{ "first_name": "Jackie", "last_name": "Joe", "city": "Jimo", "age": 77, "phone_number": "+00 091 xxx"}
```

Returns:

<!-- test-ignore -->
```typeql
insert $person isa person, has phone-number "+00 091 xxx", has is-customer true, has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

To insert an instance of a `contract` type we have the following template:

<!-- test-ignore -->
```python
def contract_template(contract):
    # match company
    typeql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    typeql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    typeql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return typeql_insert_query
```

Example:

Given the `contract` item is:

<!-- test-ignore -->
```json
{ "company_name": "Telecom", "person_id": "+00 091 xxx" }
```

Returns:

<!-- test-ignore -->
```typeql
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

To insert an instance of a `call` type we have the following template:

<!-- test-ignore -->
```python
def call_template(call):
    # match caller
    typeql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    typeql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    typeql_insert_query += " insert $call(caller: $caller, callee: $callee) isa call; $call has started-at " + call["started_at"] + "; $call has duration " + str(call["duration"]) + ";"
    return typeql_insert_query
```

Example:

Given the `call` item is:

<!-- test-ignore -->
```json
{ "caller_id": "+44 091 xxx", "callee_id": "+00 091 xxx", "started_at": 2018-08-10T07:57:51, "duration": 148 }
```

Returns:

<!-- test-ignore -->
```typeql
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

#### Performing queries

Use `queries.py` file to perform simple queries to the database. Run it with the `python queries.py` command and 
follow the instructions in the console.

### Node.js

To migrate the sample dataset into the TypeDB database `phone_calls` follow the steps below. Alternatively, clone the 
[TypeDB repository](https://github.com/vaticle/typedb-examples) and follow the readme file in the 
`telecom/phone_calls/nodejs` directory.

#### Copy the dataset

Create a new directory on the local machine.

Choose one of the input formats, download the files, and place them in the new directory inside a subdirectory 
named `data`.

<table>
  <tr>
   <td>CSV
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.csv">calls.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.csv">companies.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.csv">contracts.csv</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.csv">people.csv</a>
   </td>
  </tr>
</table>

<table>
  <tr>
   <td>JSON
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.json">calls.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.json">companies.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.json">contracts.json</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.json">people.json</a>
   </td>
  </tr>
</table>

<table>
  <tr>
   <td>XML
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/calls.xml">calls.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/companies.xml">companies.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/contracts.xml">contracts.xml</a>
   </td>
   <td><a href="https://github.com/vaticle/typedb-examples/blob/master/telecom/phone_calls/data/people.xml">people.xml</a>
   </td>
  </tr>
</table>

#### Copy the source codes

Copy the following source files from the `telecom/phone_calls` directory in the 
[TypeDB Examples](https://github.com/vaticle/typedb-examples) repository into the new directory:

* migrateCsv.js
* migrateJson.js
* migrateXml.js
* queries.js
* yarn.lock

#### Start migration

Use `npm install` to install required dependencies.

Use one of the following commands, depending on the chosen input format:

* `npm run migrateCsv`
* `npm run migrateJson`
* `npm run migrateXml`

#### Application logic

Data migration code is located inside `migrate{format}.js` file, where {format} is `Csv`, `Json`, or `Xml`.

The `buildPhoneCallGraph()` function initializes TypeDB Node.js Client, opens a session to the TypeDB database, and 
for every element of `inputs` calls `loadDataIntoTypeDB()` function.

The `loadDataIntoTypeDB()` function calls for ` parseDataToObjects()` to parse through the dataset file and then 
iterates through parsed records of the file. For every record, it opens a transaction, forms an insert query by 
calling the template function, then sends the insert query and commits the transaction. 

The rest of the file is: 

* the parsing function `parseDataToObjects()`, 
* the `Inputs` list, 
* and the template functions.

The parsing function parses data from a dataset file into a list of dictionaries. The implementation of the function 
is different for every input format.

The `Inputs` is inserted as the `inputs` argument and contains a list of dictionaries with `file` field containing 
filename (without an extension) and `template` field, containing a reference to the template function to process the 
file. 

The template functions are the most important part, as they are needed to create TypeQL insert queries from information 
parsed from dataset files.

#### Insert query examples

To insert an instance of a `company` type we have the following template:

<!-- test-ignore -->
```javascript
function companyTemplate(company) {
    return `insert $company isa company, has name "${company.name}";`;
}
```

Example:

Given the company item is:

<!-- test-ignore -->
```json
{ name: "Telecom" }
```
Returns:

<!-- test-ignore -->
```typeql
insert $company isa company, has name "Telecom";
```

To insert an instance of a `person` type we have the following template:

<!-- test-ignore -->
```javascript
function personTemplate(person) {
    const { first_name, last_name, phone_number, city, age } = person;
    // insert person
    let typeqlInsertQuery = `insert $person isa person, has phone-number "${phone_number}"`;
    const isNotCustomer = typeof first_name === "undefined";
    if (isNotCustomer) {
        // person is not a customer
        typeqlInsertQuery += ", has is-customer false";
    } else {
        // person is a customer
        typeqlInsertQuery += `, has is-customer true`;
        typeqlInsertQuery += `, has first-name "${first_name}"`;
        typeqlInsertQuery += `, has last-name "${last_name}"`;
        typeqlInsertQuery += `, has city "${city}"`;
        typeqlInsertQuery += `, has age ${age}`;
    }
    typeqlInsertQuery += ";";
    return typeqlInsertQuery;
}
```

Example:

Given the `person` item is:

<!-- test-ignore -->
```json
{ phone_number: "+44 091 xxx" }
```

Returns:

<!-- test-ignore -->
```typeql
insert $person isa person, has phone-number "+44 091 xxx";
```

or:

Given the `person` item is:

<!-- test-ignore -->
```json
{ first_name: "Jackie", last_name: "Joe", city: "Jimo", age: 77, phone_number: "+00 091 xxx"}
```

Returns:

<!-- test-ignore -->
```typeql
insert $person isa person, has phone-number "+44 091 xxx", has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

To insert an instance of a `contract` type we have the following template:

<!-- test-ignore -->
```javascript
function contractTemplate(contract) {
    const { company_name, person_id } = contract;
    // match company
    let typeqlInsertQuery = `match $company isa company, has name "${company_name}"; `;
    // match person
    typeqlInsertQuery += `$customer isa person, has phone-number "${person_id}"; `;
    // insert contract
    typeqlInsertQuery +=
        "insert (provider: $company, customer: $customer) isa contract;";
    return typeqlInsertQuery;
}
```

Example:

Given the `contract` item is:

<!-- test-ignore -->
```json
{ company_name: "Telecom", person_id: "+00 091 xxx" }
```

Returns:

<!-- test-ignore -->
```typeql
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

To insert an instance of a `call` type we have the following template:

<!-- test-ignore -->
```javascript
function callTemplate(call) {
    const { caller_id, callee_id, started_at, duration } = call;
    // match caller
    let typeqlInsertQuery = `match $caller isa person, has phone-number "${caller_id}"; `;
    // match callee
    typeqlInsertQuery += `$callee isa person, has phone-number "${callee_id}"; `;
    // insert call
    typeqlInsertQuery += `insert $call(caller: $caller, callee: $callee) isa call; $call has started-at ${started_at}; $call has duration ${duration};`;
    return typeqlInsertQuery;
}
```

Example:

Given the `call` item is:

<!-- test-ignore -->
```typeql
{ caller_id: "+44 091 xxx", callee_id: "+00 091 xxx", started_at: 2018-08-10T07:57:51, duration: 148 }
```

Returns:

<!-- test-ignore -->
```typeql
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

#### Performing queries

Use `queries.js` file to perform simple queries to the database. Run it with the
 `npm run queries` command and follow the instructions in the console.
