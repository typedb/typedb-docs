---
pageTitle: Migrating CSV, JSON and XML Data with Client Node.js
keywords: typedb, examples, migration, node.js
longTailKeywords: typedb node.js migration
Summary: Learn how to use Client Node.js to migrate CSV, JSON and XML data into a TypeDB Knowledge Graph.
---

## Goal

In this tutorial, our aim is to migrate some actual data to the `phone_calls` knowledge graph that we [defined previously](../08-examples/01-phone-calls-schema.md) using [Client Node.js](../02-clients/05-nodejs.md).

## A Quick Look at the Schema

Before we get started with migration, let’s have a quick reminder of how the schema for the `phone_calls` knowledge graph looks like.

![The Visualised Schema](../images/examples/phone_calls_schema.png)

## An Overview

Let’s go through a summary of how the migration takes place.

1.  we need a way to talk to our TypeDB [database](../06-management/01-database.md). To do this, we use [Client Node.js](../02-clients/05-nodejs.md).
2.  we go through each data file, extracting each data item and parsing it to a Javascript object.
3.  we pass each data item (in the form of a Javascript object) to its corresponding template function, which in turn gives us the constructed TypeQL query for inserting that item into TypeDB.
4.  we execute each of those queries to load the data into our target database — `phone_calls`.

Before moving on, make sure you have **npm** installed and the [**TypeDB Server**](/docs/typedb/install-and-run#start-the-typedb-server) running on your machine.

## Get Started

1.  Create a directory named `phone_calls` on your desktop.
2.  `cd` to the `phone_calls` directory via terminal.
3.  Run `npm install typedb-client` to install the TypeDB [Client Node.js](../02-clients/05-nodejs.md).
4.  Open the `phone_calls` directory in your favourite text editor.
5.  Create a `migrate.js` file in the root directory. This is where we’re going to write all our code.

## Include the Data Files

Pick one of the data formats below and download the files. After you download them, place the four files under the `files/phone-calls/data` directory. We use these to load their data into our `phone_calls` knowledge graph.

**CSV** | [companies](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/companies.csv) | [people](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/people.csv) | [contracts](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/contracts.csv) | [calls](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/calls.csv)

**JSON** | [companies](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/companies.json) | [people](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/people.json) | [contracts](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/contracts.json) | [calls](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/calls.json)

**XML** | [companies](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/companies.xml) | [people](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/people.xml) | [contracts](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/contracts.xml) | [calls](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/calls.xml)

## Set up the migration mechanism

All code that follows is to be written in `phone_calls/migrate.js`.

```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");

const inputs = [
    {
        dataPath: "files/phone-calls/data/companies",
        template: companyTemplate
    },
    {
        dataPath: "files/phone-calls/data/people",
        template: personTemplate
    },
    {
        dataPath: "files/phone-calls/data/contracts",
        template: contractTemplate
    },
    {
        dataPath: "files/phone-calls/data/calls",
        template: callTemplate
    }
];

buildPhoneCallGraph(inputs);
```

First thing first, we require the typedb module. We use it for connecting to our `phone_calls` database.

Next, we declare the `inputs`. More on this later. For now, what we need to understand about inputs — it’s an array of objects, each one containing:
- The path to the data file
- The template function that receives an object and produces the TypeQL insert query. we define these template functions in a bit.

Let’s move on.

## buildPhoneCallGraph(inputs)

```javascript
async function buildPhoneCallGraph(inputs) {
    const client = TypeDB.coreClient("localhost:1729");
    const session = await client.session("phone_calls", SessionType.DATA);

    for (input of inputs) {
        await loadDataIntoTypeDB(input, session);
    }
    await session.close();
    client.close();
}
```

This is the main and only function we need to call to start loading data into TypeDB.

What happens in this function, is as follows:

1.  A `typedb` instance is created, connected to the server we have running locally.
2.  A `session` is created, connected to the database `phone_calls`.
3.  For each `input` object in `inputs`, we call the `loadDataIntoTypeDB(input, session)`. This takes care of loading the data as specified in the input object into our database.
4.  The `session` is closed.

## loadDataIntoTypeDB(input, session)

```javascript
async function loadDataIntoTypeDB(input, session) {
    const items = await parseDataToObjects(input);

    for (item of items) {
        const transaction = await session.transaction(TransactionType.WRITE);
        const typeqlInsertQuery = input.template(item);
        await transaction.query(typeqlInsertQuery);
        await transaction.commit();
    }
}
```

In order to load data from each file into TypeDB, we need to:

1.  retrieve a list containing objects, each of which represents a data item. We do this by calling `parseDataToObjects(input)`
2.  for each object in `items`: a) create a `transaction`, b) construct the `typeqlInsertQuery` using the corresponding template function, c) run the query and d) commit the transaction.

<div class="note">
[Important]
We recommend loading a small batch of queries (< 50) per transaction before committing. This will help keep memory usage low,
offer better parallelism, and minimise duplicate work if the loader has to retry a rejected transaction.
</div>

Before we move on to parsing the data into objects, let’s start with the template functions.

## The Template Functions

Templates are simple functions that accept an object, representing a single data item. The values within this object fill in the blanks of the query template. The result is a TypeQL insert query.

We need 4 of them. Let’s go through them one by one.

### companyTemplate

```javascript
function companyTemplate(company) {
    return `insert $company isa company, has name "${company.name}";`;
}
```

Example:

- Goes in:

```javascript
{ name: "Telecom" }
```

- Comes out:

```typeql
insert $company isa company, has name "Telecom";
```

### personTemplate

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

- Goes in:
```javascript
{ phone_number: "+44 091 xxx" }
```

- Comes out:

```typeql
insert $person isa person, has phone-number "+44 091 xxx";
```

or:

- Goes in:
```javascript
{ first_name: "Jackie", last_name: "Joe", city: "Jimo", age: 77, phone_number: "+00 091 xxx"}
```

- Comes out:

```typeql
insert $person isa person, has phone-number "+44 091 xxx", has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

### contractTemplate

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

- Goes in:
```javascript
{ company_name: "Telecom", person_id: "+00 091 xxx" }
```

- Comes out:

```typeql
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

### callTemplate

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

- Goes in:
```javascript
{ caller_id: "+44 091 xxx", callee_id: "+00 091 xxx", started_at: 2018-08-10T07:57:51, duration: 148 }
```

- Comes out:

```typeql
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

We’ve now created a template for each and all four concepts that were [previously](../08-examples/01-phone-calls-schema.md) defined in the schema.

It’s time for the implementation of `parseDataToObjects(input)`.

## DataFormat-specific Implementation

The implementation for `parseDataToObjects(input)` differs based on the format of our data files.

<div class="tabs light">

[tab:CSV]
We use [Papaparse](https://www.papaparse.com/), a CSV (or delimited text) parser.

Via the terminal, while in the `phone_calls` directory, run `npm install papaparse` and require the module for it.

```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");
const fs = require("fs");
const papa = require("papaparse");
...
```

Moving on, we write the implementation of `parseDataToObjects(input)` for parsing `.csv` files.

```javascript
function parseDataToObjects(input) {
    const items = [];

    return new Promise(function (resolve, reject) {
        papa.parse(
            fs.createReadStream(input.dataPath + ".csv"),
            {
                header: true, // a Papaparse config option
                step: function (result, parser) {
                    items.push(result.data[0]);
                },

                complete: function () {
                    resolve(items);
                }
            }
        );
    });
}
```

Besides this function, we need to make one more change.

Given the nature of CSV files, the object produced has all the columns of the `.csv` file as its keys, even when the value is not there, it’ll be taken as a blank string.

For this reason, we need to change one line in our person_template function.

`const isNotCustomer = typeof first_name === "undefined";`

becomes

`const isNotCustomer = first_name === “”;`
[tab:end]

[tab:JSON]
We use [stream-json](https://github.com/uhop/stream-json) for custom JSON processing pipelines with a minimal memory footprint.

Via the terminal, while in the `phone_calls` directory, run `npm install stream-json` and require the modules for it.

```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");
const fs = require("fs");
const { parser } = require("stream-json");
const { streamArray } = require("stream-json/streamers/StreamArray");
const { chain } = require("stream-chain");
...
```

Moving on, we write the implementation of `parseDataToObjects(input)` for processing `.json` files.

```javascript
function parseDataToObjects(input) {
    const items = [];
    return new Promise(function (resolve, reject) {
        const pipeline = chain([
            fs.createReadStream(input.dataPath + ".json"),
            parser(),
            streamArray()
        ]);

        pipeline.on("data", function (result) {
            items.push(result.value);
        });

        pipeline.on("end", function () {
            resolve(items);
        });
    });
}
```
[tab:end]

[tab:XML]
We use xml-stream, an xml stream parser.

Via the terminal, while in the `phone_calls` directory, run `npm install xml-stream` and require the module for it.

```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");
const fs = require("fs");
const xmlStream = require("xml-stream");
...
```

For parsing XML data, we need to know the target tag name. This needs to be specified for each data file in our `inputs` deceleration.

```javascript
...
const inputs = [
    {
        dataPath: "files/phone-calls/data/companies",
        template: companyTemplate,
        selector: "company"
    },
    {
        dataPath: "files/phone-calls/data/people",
        template: personTemplate,
        selector: "person"
    },
    {
        dataPath: "files/phone-calls/data/contracts",
        template: contractTemplate,
        selector: "contract"
    },
    {
        dataPath: "files/phone-calls/data/calls",
        template: callTemplate,
        selector: "call"
    }
];
...
```

And now for the implementation of `parseDataToObjects(input)` for parsing `.xml` files.

```javascript
function parseDataToObjects(input) {
    const items = [];
    return new Promise((resolve, reject) => {
        const pipeline = new xmlStream(
            fs.createReadStream(input.dataPath + ".xml")
        );

        pipeline.on(`endElement: ${input.selector}`, function (result) {
            items.push(result);
        });

        pipeline.on("end", () => {
            resolve(items);
        });
    });
}
```
[tab:end]

</div>

## Putting It All Together

Here is how our `migrate.js` looks like for each data format.

<div class="tabs dark">

[tab:CSV]
<!-- test-example phoneCallsCSVMigration.js -->
```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");
const fs = require("fs");
const papa = require("papaparse");

const inputs = [
    { dataPath: "files/phone-calls/data/companies", template: companyTemplate },
    { dataPath: "files/phone-calls/data/people", template: personTemplate },
    { dataPath: "files/phone-calls/data/contracts", template: contractTemplate },
    { dataPath: "files/phone-calls/data/calls", template: callTemplate }
];

/**
 * gets the job done:
 * 1. creates a TypeDB instance
 * 2. creates a session to the targeted database
 * 3. loads csv to TypeDB for each file
 * 4. closes the session
 * 5. closes the client
 */
async function buildPhoneCallGraph() {
    const client = TypeDB.coreClient("localhost:1729"); // 1
    const session = await client.session("phone_calls", SessionType.DATA); // 2

    for (input of inputs) {
        console.log("Loading from [" + input.dataPath + "] into TypeDB ...");
        await loadDataIntoTypeDB(input, session); // 3
    }

    await session.close(); // 4
    client.close(); // 5
}

/**
 * loads the csv data into our TypeDB phone_calls database
 * @param {object} input contains details required to parse the data
 * @param {object} session a TypeDB session, off of which a transaction will be created
 */
async function loadDataIntoTypeDB(input, session) {
    const items = await parseDataToObjects(input);

    for (item of items) {
        let transaction;
        transaction = await session.transaction(TransactionType.WRITE);

        const typeqlInsertQuery = input.template(item);
        console.log("Executing TypeQL Query: " + typeqlInsertQuery);
        await transaction.query.insert(typeqlInsertQuery);
        await transaction.commit();
    }

    console.log(
        `\nInserted ${items.length} items from [${input.dataPath}] into TypeDB.\n`
    );
}

function companyTemplate(company) {
    return `insert $company isa company, has name "${company.name}";`;
}

function personTemplate(person) {
    const { first_name, last_name, phone_number, city, age } = person;
    // insert person
    let typeqlInsertQuery = `insert $person isa person, has phone-number "${phone_number}"`;
    const isNotCustomer = first_name === "";
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

/**
 * 1. reads the file through a stream,
 * 2. parses the csv line to a json object
 * 3. adds the parsed object to the list of items
 * @param {string} input.dataPath path to the data file
 * @returns items that is, a list of objects each representing a row in the csv file
 */
function parseDataToObjects(input) {
    const items = [];
    return new Promise(function (resolve, reject) {
        papa.parse(
            fs.createReadStream(input.dataPath + ".csv"), // 1
            {
                header: true, // a Papaparse config option
                // 2
                step: function (results, parser) {
                    items.push(results.data[0]); // 3
                },
                complete: function () {
                    resolve(items);
                }
            }
        );
    });
}

buildPhoneCallGraph();
```
[tab:end]

[tab:JSON]
<!-- test-example phoneCallsJSONMigration.js -->
```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");
const fs = require("fs");
const { parser } = require("stream-json");
const { streamArray } = require("stream-json/streamers/StreamArray");
const { chain } = require("stream-chain");

const inputs = [
    { dataPath: "files/phone-calls/data/companies", template: companyTemplate },
    { dataPath: "files/phone-calls/data/people", template: personTemplate },
    { dataPath: "files/phone-calls/data/contracts", template: contractTemplate },
    { dataPath: "files/phone-calls/data/calls", template: callTemplate }
];

/**
 * gets the job done:
 * 1. creates a TypeDB instance
 * 2. creates a session to the targeted database
 * 3. loads json to TypeDB for each file
 * 4. closes the session
 * 5. closes the client
 */

async function buildPhoneCallGraph() {
    const client = TypeDB.coreClient("localhost:1729"); // 1
    const session = await client.session("phone_calls", SessionType.DATA); // 2

    for (input of inputs) {
        console.log("Loading from [" + input.dataPath + "] into TypeDB ...");
        await loadDataIntoTypeDB(input, session); // 3
    }

    await session.close(); // 4
    client.close(); // 5
}

/**
 * loads the json data into our TypeDB phone_calls database
 * @param {object} input contains details required to parse the data
 * @param {object} session a TypeDB session, off of which a transaction will be created
 */
async function loadDataIntoTypeDB(input, session) {
    const items = await parseDataToObjects(input);

    for (item of items) {
        const transaction = await session.transaction(TransactionType.WRITE);

        const typeqlInsertQuery = input.template(item);
        console.log("Executing TypeQL Query: " + typeqlInsertQuery);
        await transaction.query.insert(typeqlInsertQuery);
        await transaction.commit();
    }

    console.log(
        `\nInserted ${items.length} items from [${input.dataPath}] into TypeDB.\n`
    );
}

function companyTemplate(company) {
    return `insert $company isa company, has name "${company.name}";`;
}

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

/**
 * 1. reads the file through a stream,
 * 2. adds the  object to the list of items
 * @param {string} input.dataPath path to the data file
 * @returns items that is, a list of objects each representing a data item
 */
function parseDataToObjects(input) {
    const items = [];
    return new Promise(function (resolve, reject) {
        const pipeline = chain([
            fs.createReadStream(input.dataPath + ".json"), // 1
            parser(),
            streamArray()
        ]);

        // 2
        pipeline.on("data", function (result) {
            items.push(result.value);
        });

        pipeline.on("end", function () {
            resolve(items);
        });
    });
}

buildPhoneCallGraph();
```
[tab:end]

[tab:XML]
<!-- test-example phoneCallsXMLMigration.js -->
```javascript
const { TypeDB, SessionType, TransactionType } = require("typedb-client");
const fs = require("fs");
const xmlStream = require("xml-stream");

const inputs = [
    {
        dataPath: "files/phone-calls/data/companies",
        template: companyTemplate,
        selector: "company"
    },
    {
        dataPath: "files/phone-calls/data/people",
        template: personTemplate,
        selector: "person"
    },
    {
        dataPath: "files/phone-calls/data/contracts",
        template: contractTemplate,
        selector: "contract"
    },
    {
        dataPath: "files/phone-calls/data/calls",
        template: callTemplate,
        selector: "call"
    }
];

/**
 * gets the job done:
 * 1. creates a TypeDB instance
 * 2. creates a session to the targeted database
 * 3. loads xml to TypeDB for each file
 * 4. closes the session
 * 5. closes the client
 */
async function buildPhoneCallGraph() {
    const client = TypeDB.coreClient("localhost:1729"); // 1
    const session = await client.session("phone_calls", SessionType.DATA); // 2

    for (input of inputs) {
        console.log("Loading from [" + input.dataPath + "] into TypeDB ...");
        await loadDataIntoTypeDB(input, session); // 3
    }

    await session.close(); // 4
    client.close(); // 5
};

/**
 * loads the xml data into our TypeDB phone_calls database
 * @param {object} input contains details required to parse the data
 * @param {object} session a TypeDB session, off of which a transaction will be created
 */
async function loadDataIntoTypeDB(input, session) {
    const items = await parseDataToObjects(input);

    for (item of items) {
        const transaction = await session.transaction(TransactionType.WRITE);

        const typeqlInsertQuery = input.template(item);
        console.log("Executing TypeQL Query: " + typeqlInsertQuery);
        await transaction.query.insert(typeqlInsertQuery);
        await transaction.commit();
    }

    console.log(
        `\nInserted ${items.length} items from [${input.dataPath}] into TypeDB.\n`
    );
}

function companyTemplate(company) {
    return `insert $company isa company, has name "${company.name}";`;
}

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

/**
 * 1. reads the file through a stream,
 * 2. parses the xml element to a json object
 * 3. adds it to items
 * @param {string} input.dataPath path to the data file
 * @param {string} input.selector an xml-stream option to determine the main selector to be parsed
 * @returns items that is, a list of objects each representing a data item the TypeDB database
 */
function parseDataToObjects(input) {
    const items = [];
    return new Promise((resolve, reject) => {
        const pipeline = new xmlStream(
            fs.createReadStream(input.dataPath + ".xml") // 1
        );
        // 2
        pipeline.on(`endElement: ${input.selector}`, function (result) {
            items.push(result); // 3
        });

        pipeline.on("end", () => {
            resolve(items);
        });
    });
}

buildPhoneCallGraph();
```
[tab:end]

</div>

## Time to Load

Run `node migrate.js`

Sit back, relax and watch the logs while the data starts pouring into TypeDB.

### … So Far With the Migration

We started off by setting up our project and positioning the data files.

Next, we went on to set up the migration mechanism, one that was independent of the data format.

Then, we went ahead and wrote a template function for each concept. A template’s sole purpose was to construct a TypeQL insert query for each data item.

After that, we learned how files with different data formats can be parsed into Javascript objects.

Lastly, we ran `node migrate.js` which fired the `buildPhoneCallGraph` function with the given `inputs`. This loaded the data into our TypeDB knowledge graph.

## Next

Now that we have some actual data in our knowledge graph, we can go ahead and [query for insights](../08-examples/05-phone-calls-queries.md?tab=javascript).
