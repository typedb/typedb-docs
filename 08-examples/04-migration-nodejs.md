---
sidebarTitle: Migrate - Node.js
pageTitle: Migrating CSV, JSON and XML Data with Client Node.js
permalink: /docs/examples/phone-calls-migration-nodejs
---

## Goal

In this tutorial, our aim is to migrate some actual data to the `phone_calls` knowledge graph that we [defined previously](/docs/examples/phone-calls-schema) using [Client Node.js](/docs/client-api/nodejs).

## A Quick Look at the Schema

Before we get started with migration, let’s have a quick reminder of how the schema for the `phone_calls` knowledge graph looks like.

![The Visualised Schema](/docs/images/examples/phone_calls_schema.png)

## An Overview

Let’s go through a summary of how the migration takes place.

1.  we need a way to talk to our Grakn [keyspace](/docs/management/keyspace). To do this, we use [Client Node.js](/docs/client-api/nodejs).
2.  we go through each data file, extracting each data item and parsing it to a Javascript object.
3.  we pass each data item (in the form of a Javascript object) to its corresponding template function, which in turn gives us the constructed Graql query for inserting that item into Grakn.
4.  we execute each of those queries to load the data into our target keyspace — `phone_calls`.

Before moving on, make sure you have **npm** installed and the [**Grakn Server**](/docs/running-grakn/install-and-run#start-the-grakn-server) running on your machine.

## Get Started

1.  Create a directory named `phone_calls` on your desktop.
2.  cd to the `phone_calls` directory via terminal.
3.  Run `npm install grakn` to install the Grakn [Client Node.js](/docs/client-api/nodejs).
4.  Open the `phone_calls` directory in your favourite text editor.
5.  Create a `migrate.js` file in the root directory. This is where we’re going to write all our code.

## Include the Data Files

Pick one of the data formats below and download the files. After you download them, place the four files under the `phone_calls/data` directory. We use these to load their data into our `phone_calls` knowledge graph.

**CSV** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/companies.csv) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/people.csv) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/contracts.csv) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/calls.csv)

**JSON** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/companies.json) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/people.json) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/contracts.json) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/json/data/calls.json)

**XML** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/companies.xml) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/people.xml) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/contracts.xml) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/xml/data/calls.xml)

## Set up the migration mechanism

All code that follows is to be written in `phone_calls/migrate.js`.

```javascript
const Grakn = require("grakn");

const inputs = [
  {
    dataPath: "./data/companies",
    template: companyTemplate
  },
  {
    dataPath: "./data/people",
    template: personTemplate
  },
  {
    dataPath: "./data/contracts",
    template: contractTemplate
  },
  {
    dataPath: "./data/calls",
    template: callTemplate
  }
];

buildPhoneCallGraph(inputs);
```

First thing first, we require the grakn module. We use it for connecting to our `phone_calls` keyspace.

Next, we declare the `inputs`. More on this later. For now, what we need to understand about inputs — it’s an array of objects, each one containing:
- The path to the data file
- The template function that receives an object and produces the Graql insert query. we define these template functions in a bit.

Let’s move on.

## buildPhoneCallGraph(inputs)

```javascript
async function buildPhoneCallGraph(inputs) {
  const grakn = new Grakn("localhost:48555");
  const session = grakn.session("phone_calls");

  for (input of inputs) {
    await loadDataIntoGrakn(parsingInput, session);
  }
  session.close();
}
```

This is the main and only function we need to call to start loading data into Grakn.

What happens in this function, is as follows:

1.  A `grakn` instance is created, connected to the server we have running locally.
2.  A `session` is created, connected to the keyspace `phone_calls`.
3.  For each `input` object in `inputs`, we call the `loadDataIntoGrakn(input, session)`. This takes care of loading the data as specified in the input object into our keyspace.
4.  The `session` is closed.

## loadDataIntoGrakn(input, session)

```javascript
async function loadDataIntoGrakn(input, session) {
  const items = await parseDataToObjects(input);

  for (item of items) {
    const tx = await session.transaction(Grakn.txType.WRITE);
    const graqlInsertQuery = input.template(item);
    await tx.query(graqlInsertQuery);
    await tx.commit();
  }
}
```

In order to load data from each file into Grakn, we need to:

1.  retrieve a list containing objects, each of which represents a data item. We do this by calling `parseDataToObjects(input)`
2.  for each object in `items`: a) create a transaction `tx`, b) construct the `graqlInsertQuery` using the corresponding template function, c) run the query and d)commit the transaction.

<div class="note">
[Important]
To avoid running out of memory, it’s recommended that every single query gets created and committed in a single transaction.
However, for faster migration of large datasets, this can happen once for every `n` queries, where `n` is the maximum number of queries guaranteed to run on a single transaction.
</div>

Before we move on to parsing the data into objects, let’s start with the template functions.

## The Template Functions

Templates are simple functions that accept an object, representing a single data item. The values within this object fill in the blanks of the query template. The result is a Graql insert query.

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
```javascript
insert $company isa company, has name "Telecom";
```

### personTemplate

```javascript
function personTemplate(person) {
  const { first_name, last_name, phone_number, city, age } = person;

  // insert person
  let graqlInsertQuery = `insert $person isa person, has phone-number "${phone_number}"`;
  const isNotCustomer = typeof first_name === "undefined";

  if (isNotCustomer) {
    // person is not a customer
    graqlInsertQuery += ", has is-customer false";
  } else {
    // person is a customer
    graqlInsertQuery += `, has is-customer true`;
    graqlInsertQuery += `, has first-name "${first_name}"`;
    graqlInsertQuery += `, has last-name "${last_name}"`;
    graqlInsertQuery += `, has city "${city}"`;
    graqlInsertQuery += `, has age ${age}`;
  }

  graqlInsertQuery += ";";
  return graqlInsertQuery;
}
```

Example:

- Goes in:
```javascript
{ phone_number: "+44 091 xxx" }
```

- Comes out:
```javascript
insert $person has phone-number "+44 091 xxx";
```

or:

- Goes in:
```javascript
{ firs_name: "Jackie", last_name: "Joe", city: "Jimo", age: 77, phone_number: "+00 091 xxx"}
```

- Comes out:
```javascript
insert $person has phone-number "+44 091 xxx", has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

### contractTemplate

```javascript
function contractTemplate(contract) {
  const { company_name, person_id } = contract;
  // match company
  let graqlInsertQuery = `match $company isa company, has name "${company_name}"; `;
  // match person
  graqlInsertQuery += `$customer isa person, has phone-number "${person_id}"; `;
  // insert contract
  graqlInsertQuery +=
    "insert (provider: $company, customer: $customer) isa contract;";
  return graqlInsertQuery;
}
```

Example:

- Goes in:
```javascript
{ company_name: "Telecom", person_id: "+00 091 xxx" }
```

- Comes out:
```javascript
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

### callTemplate

```javascript
function callTemplate(call) {
  const { caller_id, callee_id, started_at, duration } = call;

  // match caller
  let graqlInsertQuery = `match $caller isa person, has phone-number "${caller_id}"; `;

  // match callee
  graqlInsertQuery += `$callee isa person, has phone-number "${callee_id}"; `;

  // insert call
  graqlInsertQuery += `insert $call(caller: $caller, callee: $callee) isa call; $call has started-at ${started_at}; $call has duration ${duration};`;
  return graqlInsertQuery;
}
```

Example:

- Goes in:
```javascript
{ caller_id: "+44 091 xxx", callee_id: "+00 091 xxx", started_at: 2018–08–10T07:57:51, duration: 148 }
```

- Comes out:
```javascript
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018–08–10T07:57:51; $call has duration 148;
```

We’ve now created a template for each and all four concepts that were [previously](./defining-the-schema) defined in the schema.

It’s time for the implementation of `parseDataToObjects(input)`.

## DataFormat-specific Implementation

The implementation for `parseDataToObjects(input)` differs based on the format of our data files.

<div class="tabs light">

[tab:CSV]
We use [Papaparse](https://www.papaparse.com/), a CSV (or delimited text) parser.

Via the terminal, while in the `phone_calls` directory, run `npm install papaparse` and require the module for it.

```javascript
const Grakn = require("grakn");
const fs = require("fs");
const papa = require("papaparse");
...
```

Moving on, we write the implementation of `parseDataToObjects(input)` for parsing `.csv` files.

```javascript
function parseDataToObjects(input) {
  const items = [];

  return new Promise(function(resolve, reject) {
    papa.parse(
      fs.createReadStream(input.dataPath + ".csv"),
      {
        header: true, // a Papaparse config option
        step: function(result, parser) {
          items.push(result.data[0]);
        },

        complete: function() {
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
const Grakn = require("grakn");
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
  return new Promise(function(resolve, reject) {
    const pipeline = chain([
      fs.createReadStream(input.dataPath + ".json"),
      parser(),
      streamArray()
    ]);

    pipeline.on("data", function(result) {
      items.push(result.value);
    });

    pipeline.on("end", function() {
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
const Grakn = require("grakn");
const fs = require("fs");
const xmlStream = require("xml-stream");
...
```

For parsing XML data, we need to know the target tag name. This needs to be specified for each data file in our `inputs` deceleration.

```javascript
...
const inputs = [
  {
    dataPath: "./data/companies",
    template: companyTemplate,
    selector: "company"
  },
  {
    dataPath: "./data/people",
    template: personTemplate,
    selector: "person"
  },
  {
    dataPath: "./data/contracts",
    template: contractTemplate,
    selector: "contract"
  },
  {
    dataPath: "./data/calls",
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

    pipeline.on(`endElement: ${input.selector}`, function(result) {
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
```javascript
const Grakn = require("grakn");
const fs = require("fs");
const papa = require("papaparse");

const inputs = [
  { dataPath: "./data/companies", template: companyTemplate },
  { dataPath: "./data/people", template: personTemplate },
  { dataPath: "./data/contracts", template: contractTemplate },
  { dataPath: "./data/calls", template: callTemplate }
];

// Go
buildPhoneCallGraph(inputs);

async function buildPhoneCallGraph() {
  const grakn = new Grakn("localhost:48555");
  const session = grakn.session("phone_calls");

  for (input of inputs) {
    console.log("Loading from [" + input.dataPath + "] into Grakn ...");
    await loadDataIntoGrakn(input, session);
  }

  session.close();
}

async function loadDataIntoGrakn(input, session) {
  const items = await parseDataToObjects(input);

  for (item of items) {
    let tx;
    tx = await session.transaction(Grakn.txType.WRITE);

    const graqlInsertQuery = input.template(item);
    console.log("Executing Graql Query: " + graqlInsertQuery);
    await tx.query(graqlInsertQuery);
    await tx.commit();
  }

  console.log(
    `\nInserted ${items.length} items from [${input.dataPath}] into Grakn.\n`
  );
}

async function loadDataIntoGrakn(input, session) {
  const items = await parseDataToObjects(input);

  for (item of items) {
    const tx = await session.transaction(Grakn.txType.WRITE);

    const graqlInsertQuery = input.template(item);
    console.log("Executing Graql Query: " + graqlInsertQuery);
    tx.query(graqlInsertQuery);
    tx.commit();
  }

  console.log(
    `\nInserted ${items.length} items from [${input.dataPath}] into Grakn.\n`
  );
}

function companyTemplate(company) {
  return `insert $company isa company, has name "${company.name}";`;
}

function personTemplate(person) {
  const { first_name, last_name, phone_number, city, age } = person;
  // insert person
  let graqlInsertQuery = `insert $person isa person, has phone-number "${phone_number}"`;
  const isNotCustomer = first_name === "";
  if (isNotCustomer) {
    // person is not a customer
    graqlInsertQuery += ", has is-customer false";
  } else {
    // person is a customer
    graqlInsertQuery += `, has is-customer true`;
    graqlInsertQuery += `, has first-name "${first_name}"`;
    graqlInsertQuery += `, has last-name "${last_name}"`;
    graqlInsertQuery += `, has city "${city}"`;
    graqlInsertQuery += `, has age ${age}`;
  }

  graqlInsertQuery += ";";
  return graqlInsertQuery;
}

function contractTemplate(contract) {
  const { company_name, person_id } = contract;
  // match company
  let graqlInsertQuery = `match $company isa company, has name "${company_name}"; `;
  // match person
  graqlInsertQuery += `$customer isa person, has phone-number "${person_id}"; `;
  // insert contract
  graqlInsertQuery +=
    "insert (provider: $company, customer: $customer) isa contract;";
  return graqlInsertQuery;
}

function callTemplate(call) {
  const { caller_id, callee_id, started_at, duration } = call;
  // match caller
  let graqlInsertQuery = `match $caller isa person, has phone-number "${caller_id}"; `;
  // match callee
  graqlInsertQuery += `$callee isa person, has phone-number "${callee_id}"; `;
  // insert call
  graqlInsertQuery += "insert $call(caller: $caller, callee: $callee) isa call; " +
    `$call has started-at ${started_at}; $call has duration ${duration};`;
  return graqlInsertQuery;
}

function parseDataToObjects(input) {
  const items = [];
  return new Promise(function(resolve, reject) {
    papa.parse(
      fs.createReadStream(input.dataPath + ".csv"),
      {
        header: true, // a Papaparse config option
        step: function(results, parser) {
          items.push(results.data[0]);
        },
        complete: function() {
          resolve(items);
        }
      }
    );
  });
}
```
[tab:end]

[tab:JSON]
```javascript
const Grakn = require("grakn");
const fs = require("fs");
const { parser } = require("stream-json");
const { streamArray } = require("stream-json/streamers/StreamArray");
const { chain } = require("stream-chain");

const inputs = [
  { dataPath: "./data/companies", template: companyTemplate },
  { dataPath: "./data/people", template: personTemplate },
  { dataPath: "./data/contracts", template: contractTemplate },
  { dataPath: "./data/calls", template: callTemplate }
];

// Go
buildPhoneCallGraph(inputs);

async function buildPhoneCallGraph() {
  const grakn = new Grakn("localhost:48555"); // 1
  const session = grakn.session("phone_calls"); // 2

  for (input of inputs) {
    console.log("Loading from [" + input.dataPath + "] into Grakn ...");
    await loadDataIntoGrakn(input, session); // 3
  }

  session.close(); // 4
}

async function loadDataIntoGrakn(input, session) {
  const items = await parseDataToObjects(input);

  for (item of items) {
    const tx = await session.transaction(Grakn.txType.WRITE);

    const graqlInsertQuery = input.template(item);
    console.log("Executing Graql Query: " + graqlInsertQuery);
    tx.query(graqlInsertQuery);
    tx.commit();
  }

  console.log(
    `\nInserted ${items.length} items from [${input.dataPath}] into Grakn.\n`
  );
}

function companyTemplate(company) {
  return `insert $company isa company, has name "${company.name}";`;
}

function personTemplate(person) {
  const { first_name, last_name, phone_number, city, age } = person;
  // insert person
  let graqlInsertQuery = `insert $person isa person, has phone-number "${phone_number}"`;
  const isNotCustomer = typeof first_name === "undefined";
  if (isNotCustomer) {
    // person is not a customer
    graqlInsertQuery += ", has is-customer false";
  } else {
    // person is a customer
    graqlInsertQuery += `, has is-customer true`;
    graqlInsertQuery += `, has first-name "${first_name}"`;
    graqlInsertQuery += `, has last-name "${last_name}"`;
    graqlInsertQuery += `, has city "${city}"`;
    graqlInsertQuery += `, has age ${age}`;
  }

  graqlInsertQuery += ";";
  return graqlInsertQuery;
}

function contractTemplate(contract) {
  const { company_name, person_id } = contract;
  // match company
  let graqlInsertQuery = `match $company isa company, has name "${company_name}"; `;
  // match person
  graqlInsertQuery += `$customer isa person, has phone-number "${person_id}"; `;
  // insert contract
  graqlInsertQuery +=
    "insert (provider: $company, customer: $customer) isa contract;";
  return graqlInsertQuery;
}

function callTemplate(call) {
  const { caller_id, callee_id, started_at, duration } = call;
  // match caller
  let graqlInsertQuery = `match $caller isa person, has phone-number "${caller_id}"; `;
  // match callee
  graqlInsertQuery += `$callee isa person, has phone-number "${callee_id}"; `;
  // insert call
  graqlInsertQuery += "insert $call(caller: $caller, callee: $callee) isa call; " +
    `$call has started-at ${started_at}; $call has duration ${duration};`;
  return graqlInsertQuery;
}

function parseDataToObjects(input) {
  const items = [];
  return new Promise(function(resolve, reject) {
    const pipeline = chain([
      fs.createReadStream(input.dataPath + ".json"),
      parser(),
      streamArray()
    ]);

    pipeline.on("data", function(result) {
      items.push(result.value);
    });

    pipeline.on("end", function() {
      resolve(items);
    });
  });
}
```
[tab:end]

[tab:XML]
```javascript
const Grakn = require("grakn");
const fs = require("fs");
const xmlStream = require("xml-stream");

const inputs = [
  {
    dataPath: "./data/companies",
    template: companyTemplate,
    selector: "company"
  },
  {
    dataPath: "./data/people",
    template: personTemplate,
    selector: "person"
  },
  {
    dataPath: "./data/contracts",
    template: contractTemplate,
    selector: "contract"
  },
  {
    dataPath: "./data/calls",
    template: callTemplate,
    selector: "call"
  }
];

// Go
buildPhoneCallGraph(inputs);

async function buildPhoneCallGraph() {
  const grakn = new Grakn("localhost:48555");
  const session = grakn.session("phone_calls");

  for (input of inputs) {
    console.log("Loading from [" + input.dataPath + "] into Grakn ...");
    await loadDataIntoGrakn(input, session);
  }

  session.close();
}

async function loadDataIntoGrakn(input, session) {
  const items = await parseDataToObjects(input);

  for (item of items) {
    let tx;
    tx = await session.transaction(Grakn.txType.WRITE);

    const graqlInsertQuery = input.template(item);
    console.log("Executing Graql Query: " + graqlInsertQuery);
    tx.query(graqlInsertQuery);
    tx.commit();
  }

  console.log(
    `\nInserted ${items.length} items from [${input.dataPath}] into Grakn.\n`
  );
}

function companyTemplate(company) {
  return `insert $company isa company, has name "${company.name}";`;
}

function personTemplate(person) {
  const { first_name, last_name, phone_number, city, age } = person;
  // insert person
  let graqlInsertQuery = `insert $person isa person, has phone-number "${phone_number}"`;
  const isNotCustomer = typeof first_name === "undefined";
  if (isNotCustomer) {
    // person is not a customer
    graqlInsertQuery += ", has is-customer false";
  } else {
    // person is a customer
    graqlInsertQuery += `, has is-customer true`;
    graqlInsertQuery += `, has first-name "${first_name}"`;
    graqlInsertQuery += `, has last-name "${last_name}"`;
    graqlInsertQuery += `, has city "${city}"`;
    graqlInsertQuery += `, has age ${age}`;
  }

  graqlInsertQuery += ";";
  return graqlInsertQuery;
}

function contractTemplate(contract) {
  const { company_name, person_id } = contract;
  // match company
  let graqlInsertQuery = `match $company isa company, has name "${company_name}"; `;
  // match person
  graqlInsertQuery += `$customer isa person, has phone-number "${person_id}"; `;
  // insert contract
  graqlInsertQuery +=
    "insert (provider: $company, customer: $customer) isa contract;";
  return graqlInsertQuery;
}

function callTemplate(call) {
  const { caller_id, callee_id, started_at, duration } = call;
  // match caller
  let graqlInsertQuery = `match $caller isa person, has phone-number "${caller_id}"; `;
  // match callee
  graqlInsertQuery += `$callee isa person, has phone-number "${callee_id}"; `;
  // insert call
  graqlInsertQuery += "insert $call(caller: $caller, callee: $callee) isa call; " +
    `$call has started-at ${started_at}; $call has duration ${duration};`;
  return graqlInsertQuery;
}

function parseDataToObjects(input) {
  const items = [];
  return new Promise((resolve, reject) => {
    const pipeline = new xmlStream(
      fs.createReadStream(input.dataPath + ".xml")
    );

    pipeline.on(`endElement: ${input.selector}`, function(result) {
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

## Time to Load

Run `npm run migrate.js`

Sit back, relax and watch the logs while the data starts pouring into Grakn.

### … So Far With the Migration

We started off by setting up our project and positioning the data files.

Next, we went on to set up the migration mechanism, one that was independent of the data format.

Then, we went ahead and wrote a template function for each concept. A template’s sole purpose was to construct a Graql insert query for each data item.

After that, we learned how files with different data formats can be parsed into Javascript objects.

Lastly, we ran `npm run migrate.js` which fired the `buildPhoneCallGraph` function with the given `inputs`. This loaded the data into our Grakn knowledge graph.

## Next

Now that we have some actual data in our knowledge graph, we can go ahead and [query for insights](/docs/examples/phone-calls-queries?lang=javascript).
