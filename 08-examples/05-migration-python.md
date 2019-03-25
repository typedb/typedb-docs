---
pageTitle: Migrating CSV, JSON and XML Data with Client Python
keywords: grakn, examples, migration, python
longTailKeywords: grakn python migration
Summary: Learn how to use Client Python to migrate CSV, JSON and XML data into a Grakn Knowledge Graph.
permalink: /docs/examples/phone-calls-migration-python
---

## Goal

In this tutorial, our aim is to migrate some actual data to the `phone_calls` knowledge graph that we [defined previously](/docs/examples/phone-calls-schema) using [Client Python](/docs/client-api/python).

## A Quick Look at the Schema

Before we get started with migration, let’s have a quick reminder of how the schema for the `phone_calls` knowledge graph looks like.

![The Visualised Schema](/docs/images/examples/phone_calls_schema.png)

## An Overview

Let’s go through a summary of how the migration takes place.

1.  we need a way to talk to our Grakn [keyspace](/docs/management/keyspace). To do this, we use [Client Python](/docs/client-api/python).
2.  we go through each data file, extracting each data item and parsing it to a Python dictionary.
3.  we pass each data item (in the form of a Python dictionary) to its corresponding template function, which in turn gives us the constructed Graql query for inserting that item into Grakn.
4.  we execute each of those queries to load the data into our target keyspace — `phone_calls`.

Before moving on, make sure you have **Python3** and **Pip3** installed and the [**Grakn Server**](/docs/running-grakn/install-and-run#start-the-grakn-server) running on your machine.

## Get Started

1.  Create a directory named `phone_calls` on your desktop.
2.  cd to the phone_calls directory via terminal.
3.  Run `pip3 install grakn` to install the Grakn [Client Python](/docs/client-api/python).
4.  Open the `phone_calls` directory in your favourite text editor.
5.  Create a `migrate.py` file in the root directory. This is where we’re going to write all our code.

## Include the Data Files

Pick one of the data formats below and download the files. After you download them, place the four files under the `files/phone-calls/data` directory. We need these to load their data into our `phone_calls` knowledge graph.

**CSV** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/companies.csv) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/nodejs/migration/csv/data/people.csv) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/contracts.csv) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/calls.csv)

**JSON** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/companies.json) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/people.json) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/contracts.json) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/calls.json)

**XML** | [companies](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/companies.xml) | [people](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/people.xml) | [contracts](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/contracts.xml) | [calls](https://raw.githubusercontent.com/graknlabs/examples/master/datasets/phone-calls/calls.xml)

## Set up the migration mechanism

All code that follows is to be written in `phone_calls/migrate.py`.

```python
from grakn.client import GraknClient

inputs = [
    {
        "data_path": "files/phone-calls/data/companies",
        "template": company_template
    },
    {
        "data_path": "files/phone-calls/data/people",
        "template": person_template
    },
    {
        "data_path": "files/phone-calls/data/contracts",
        "template": contract_template
    },
    {
        "data_path": "files/phone-calls/data/calls",
        "template": call_template
    }
]

build_phone_call_graph(inputs)
```

First thing first, we import the grakn module. We use it for connecting to our `phone_calls` keyspace.

Next, we declare the `inputs`. More on this later. For now, what we need to understand about inputs — it’s a list of dictionaries, each one containing:
- The path to the data file
- The template function that receives a dictionary and produces the Graql insert query. we define these template functions in a bit.

Let’s move on.

## build_phone_call_graph(inputs)

```python
from grakn.client import GraknClient

def build_phone_call_graph(inputs):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "phone_calls") as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into Grakn ...")
                load_data_into_grakn(input, session)

# ...
```

This is the main and only function we need to call to start loading data into Grakn.

What happens in this function, is as follows:

1.  A Grakn `client` is created, connected to the server we have running locally.
2.  A `session` is created, connected to the keyspace `phone_calls`. Note that by using `with`, we indicate that the session closes after it’s been used.
3.  For each `input` dictionary in `inputs`, we call the `load_data_into_grakn(input, session)`. This takes care of loading the data as specified in the input dictionary into our keyspace.

## load_data_into_grakn(input, session)

```python
def load_data_into_grakn(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:
        with session.transaction().write() as transaction:
            graql_insert_query = input["template"](item)
            print("Executing Graql Query: " + graql_insert_query)
            transaction.query(graql_insert_query)
            transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into Grakn.\n")

# ...
```

In order to load data from each file into Grakn, we need to:

1.  retrieve a list containing dictionaries, each of which represents a data item. We do this by calling `parse_data_to_dictionaries(input)`
2.  for each dictionary in `items`: a) create a `transaction`, which closes once used, b) construct the `graql_insert_query` using the corresponding template function, c) execute the query and d)commit the transaction.

<div class="note">
[Important]
To avoid running out of memory, it’s recommended that every single query gets created and committed in a single transaction.
However, for faster migration of large datasets, this can happen once for every `n` queries, where `n` is the maximum number of queries guaranteed to run on a single transaction.
</div>

Before we move on to parsing the data into dictionaries, let’s start with the template functions.

## The Template Functions

Templates are simple functions that accept a dictionary, representing a single data item. The values within this dictionary fill in the blanks of the query template. The result is a Graql insert query.
We need 4 of them. Let’s go through them one by one.

### companyTemplate

```python
def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'
```

Example:

- Goes in:
```python
{ "name": "Telecom" }
```

- Comes out:
```python
insert $company isa company, has name "Telecom";
```

### personTemplate

```python
def person_template(person):
    # insert person
    graql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if "first_name" in person:
        # person is a customer
        graql_insert_query += ", has is-customer true"
        graql_insert_query += ', has first-name "' + person["first_name"] + '"'
        graql_insert_query += ', has last-name "' + person["last_name"] + '"'
        graql_insert_query += ', has city "' + person["city"] + '"'
        graql_insert_query += ", has age " + str(person["age"])
    else:
        # person is not a customer
        graql_insert_query += ", has is-customer false"
    graql_insert_query += ";"
    return graql_insert_query
```

Example:

- Goes in:
```python
{ "phone_number": "+44 091 xxx" }
```

- Comes out:
```python
insert $person isa person has phone-number "+44 091 xxx";
```

or:

- Goes in:
```python
{ "firs_name": "Jackie", "last_name": "Joe", "city": "Jimo", "age": 77, "phone_number": "+00 091 xxx"}
```

- Comes out:
```python
insert $person has phone-number "+44 091 xxx", has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

### contractTemplate

```python
def person_template(person):
    # insert person
    graql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if "first_name" in person:
        # person is a customer
        graql_insert_query += ", has is-customer true"
        graql_insert_query += ', has first-name "' + person["first_name"] + '"'
        graql_insert_query += ', has last-name "' + person["last_name"] + '"'
        graql_insert_query += ', has city "' + person["city"] + '"'
        graql_insert_query += ", has age " + str(person["age"])
    else:
        # person is not a customer
        graql_insert_query += ", has is-customer false"
    graql_insert_query += ";"
    return graql_insert_query
```

Example:

- Goes in:
```python
{ "company_name": "Telecom", "person_id": "+00 091 xxx" }
```

- Comes out:
```python
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

### callTemplate

```python
def call_template(call):
    # match caller
    graql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    graql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    graql_insert_query += " insert $call(caller: $caller, callee: $callee) isa call; $call has started-at " + call["started_at"] + "; $call has duration " + str(call["duration"]) + ";"
    return graql_insert_query
```

Example:

- Goes in:
```python
{ "caller_id": "+44 091 xxx", "callee_id": "+00 091 xxx", "started_at": 2018-08-10T07:57:51, "duration": 148 }
```

- Comes out:
```python
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

We’ve now created a template for each and all four concepts that were [previously](./defining-the-schema) defined in the schema.

It’s time for the implementation of `parse_data_to_dictionaries(input)`.

## DataFormat-specific Implementation

The implementation for `parse_data_to_dictionaries(input)` differs based on the format of our data files.

<div class="tabs light">

[tab:CSV]
We use Python’s built-in [`csv` library](https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters). Let’s import the module for it.

```python
from grakn.client import GraknClient
import csv

#...
```

Moving on, we write the implementation of `parse_data_to_dictionaries(input)` for parsing `.csv` files. Note that we use [DictReader](https://docs.python.org/3/library/csv.html#csv.DictReader) to map the information in each row to a dictionary.

```python
def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"] + ".csv") as data:
        for row in csv.DictReader(data, skipinitialspace = True):
            item = { key: value for key, value in row.items() }
            items.append(item)
    return items
```

Besides this function, we need to make one more change.

Given the nature of CSV files, the dictionary produced has all the columns of the `.csv` file as its keys, even when the value is not there, it’ll be taken as a blank string.

For this reason, we need to change one line in our `person_template` function.

`if "first_name" in person` becomes `if person["first_name"] == ""`.
[tab:end]

[tab:JSON]
We use [ijson](https://pypi.org/project/ijson/), an iterative JSON parser with a standard Python iterator interface.

Via the terminal, while in the `phone_calls` directory, run `pip3 install ijson` and import the module for it.

```python
from grakn.client import GraknClient
import ijson

# ...
```

Moving on, we write the implementation of `parse_data_to_dictionaries(input)` for processing `.json` files.

We use Python’s built-in [`xml.etree.cElementTree` library](https://docs.python.org/2/library/xml.etree.elementtree.html). Let’s import the module for it.

```python
def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"] + ".json") as data:
        for item in ijson.items(data, "item"):
            items.append(item)
    return items
```
[tab:end]

[tab:XML]
For parsing XML data, we need to know the target tag name. This needs to be specified for each data file in our `inputs` deceleration.

```python
# ...

inputs = [
    {
        "data_path": "files/phone-calls/data/companies",
        "template": company_template,
        "selector": "company"
    },
    {
        "data_path": "files/phone-calls/data/people",
        "template": person_template,
        "selector": "person"
    },
    {
        "data_path": "files/phone-calls/data/contracts",
        "template": contract_template,
        "selector": "contract"
    },
    {
        "data_path": "files/phone-calls/data/calls",
        "template": call_template,
        "selector": "call"
    }
]

# ...
```

And now for the implementation of `parse_data_to_dictionaries(input)` for parsing `.xml` files.

The implementation below, although, not the most generic, performs well with very large `.xml` files. Note that many libraries that do xml to dictionary parsing, pull in the entire `.xml` file into memory first. There is nothing wrong with that approach when you’re dealing with small files, but when it comes to large files, that’s just a no go.

```python
def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"] + ".xml", "rb") as inputfile:
        ## we are in the file
        keep_adding_lines = False
        for line in inputfile:
            if "<" + input["selector"] + ">" in str(line):
                ## now: at the start of a new target tag
                buffer = line
                keep_adding_lines = True
            elif "</" + input["selector"]  + ">" in str(line):
                ## now: the tag is complete
                buffer += line
                keep_adding_lines = False
                ## convert the buffer (string) to a strurctured tag
                tnode = et.fromstring(buffer)
                ## parse the tag to a dictionary
                item = {}
                for element in tnode.getchildren():
                    item[element.tag] = element.text
                ## append the item to the list
                items.append(item)
                ## delete the buffer to free the memory
                del buffer
            elif keep_adding_lines:
                ## now: inside the target tag
                buffer += line
    return items
```
[tab:end]

</div>

## Putting It All Together

Here is how our `migrate.py` looks like for each data format.

<div class="tabs dark">

[tab:CSV]
<!-- test-example phone_calls_csv_migration.py -->
```python
from grakn.client import GraknClient
import csv

def build_phone_call_graph(inputs):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "phone_calls") as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into Grakn ...")
                load_data_into_grakn(input, session)

def load_data_into_grakn(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:
        with session.transaction().write() as transaction:
            graql_insert_query = input["template"](item)
            print("Executing Graql Query: " + graql_insert_query)
            transaction.query(graql_insert_query)
            transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into Grakn.\n")

def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'

def person_template(person):
    # insert person
    graql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if person["first_name"] == "":
        # person is not a customer
        graql_insert_query += ", has is-customer false"
    else:
        # person is a customer
        graql_insert_query += ", has is-customer true"
        graql_insert_query += ', has first-name "' + person["first_name"] + '"'
        graql_insert_query += ', has last-name "' + person["last_name"] + '"'
        graql_insert_query += ', has city "' + person["city"] + '"'
        graql_insert_query += ", has age " + str(person["age"])
    graql_insert_query += ";"
    return graql_insert_query

def contract_template(contract):
    # match company
    graql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    graql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    graql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return graql_insert_query

def call_template(call):
    # match caller
    graql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    graql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    graql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return graql_insert_query

def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"] + ".csv") as data: # 1
        for row in csv.DictReader(data, skipinitialspace = True):
            item = { key: value for key, value in row.items() }
            items.append(item) # 2
    return items

inputs = [
    {
        "data_path": "files/phone-calls/data/companies",
        "template": company_template
    },
    {
        "data_path": "files/phone-calls/data/people",
        "template": person_template
    },
    {
        "data_path": "files/phone-calls/data/contracts",
        "template": contract_template
    },
    {
        "data_path": "files/phone-calls/data/calls",
        "template": call_template
    }
]

build_phone_call_graph(inputs=inputs)
```
[tab:end]

[tab:JSON]
<!-- test-example phone_calls_json_migration.py -->
```python
from grakn.client import GraknClient
import ijson

def build_phone_call_graph(inputs):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "phone_calls") as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into Grakn ...")
                load_data_into_grakn(input, session)

def load_data_into_grakn(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:
        with session.transaction().write() as transaction:
            graql_insert_query = input["template"](item)
            print("Executing Graql Query: " + graql_insert_query)
            transaction.query(graql_insert_query)
            transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into Grakn.\n")

def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'

def person_template(person):
    # insert person
    graql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if "first_name" in person:
        # person is a customer
        graql_insert_query += ", has is-customer true"
        graql_insert_query += ', has first-name "' + person["first_name"] + '"'
        graql_insert_query += ', has last-name "' + person["last_name"] + '"'
        graql_insert_query += ', has city "' + person["city"] + '"'
        graql_insert_query += ", has age " + str(person["age"])
    else:
        # person is not a customer
        graql_insert_query += ", has is-customer false"
    graql_insert_query += ";"
    return graql_insert_query

def contract_template(contract):
    # match company
    graql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    graql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    graql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return graql_insert_query

def call_template(call):
    # match caller
    graql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    graql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    graql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return graql_insert_query

def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"] + ".json") as data:
        for item in ijson.items(data, "item"):
            items.append(item)
    return items

inputs = [
    {
        "data_path": "files/phone-calls/data/companies",
        "template": company_template
    },
    {
        "data_path": "files/phone-calls/data/people",
        "template": person_template
    },
    {
        "data_path": "files/phone-calls/data/contracts",
        "template": contract_template
    },
    {
        "data_path": "files/phone-calls/data/calls",
        "template": call_template
    }
]

build_phone_call_graph(inputs)
```
[tab:end]

[tab:XML]
<!-- test-example phone_calls_xml_migration.py -->
```python
from grakn.client import GraknClient
import xml.etree.cElementTree as et

def build_phone_call_graph(inputs):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace = "phone_calls") as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into Grakn ...")
                load_data_into_grakn(input, session)

def load_data_into_grakn(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:
        with session.transaction().write() as transaction:
            graql_insert_query = input["template"](item)
            print("Executing Graql Query: " + graql_insert_query)
            transaction.query(graql_insert_query)
            transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into Grakn.\n")

def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'

def person_template(person):
    # insert person
    graql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if "first_name" in person:
        # person is a customer
        graql_insert_query += ", has is-customer true"
        graql_insert_query += ', has first-name "' + person["first_name"] + '"'
        graql_insert_query += ', has last-name "' + person["last_name"] + '"'
        graql_insert_query += ', has city "' + person["city"] + '"'
        graql_insert_query += ", has age " + str(person["age"])
    else:
        # person is not a customer
        graql_insert_query += ", has is-customer false"
    graql_insert_query += ";"
    return graql_insert_query

def contract_template(contract):
    # match company
    graql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    graql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    graql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return graql_insert_query

def call_template(call):
    # match caller
    graql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    graql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    graql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return graql_insert_query

def parse_data_to_dictionaries(input):
    items = []
    with open(input["data_path"] + ".xml", "rb") as inputfile:
        append = False
        for line in inputfile:
            if "<" + input["selector"] + ">" in str(line):
                ## start of a new xml tag
                buffer = line
                append = True
            elif "</" + input["selector"]  + ">" in str(line):
                ## we got a complete xml tag
                buffer += line
                append = False
                tnode = et.fromstring(buffer)
                ## parse the tag to a dictionary and append to tiems
                item = {}
                for element in tnode.getchildren():
                    item[element.tag] = element.text
                items.append(item)
                ## delete the buffer to free the memory
                del buffer
            elif append:
                ## inside the current xml tag
                buffer += line
    return items

inputs = [
    {
        "data_path": "files/phone-calls/data/companies",
        "template": company_template,
        "selector": "company"
    },
    {
        "data_path": "files/phone-calls/data/people",
        "template": person_template,
        "selector": "person"
    },
    {
        "data_path": "files/phone-calls/data/contracts",
        "template": contract_template,
        "selector": "contract"
    },
    {
        "data_path": "files/phone-calls/data/calls",
        "template": call_template,
        "selector": "call"
    }
]

build_phone_call_graph(inputs)
```
[tab:end]

</div>

## Time to Load

Run `python3 migrate.py`

Sit back, relax and watch the logs while the data starts pouring into Grakn.

### ... So Far With the Migration

We started off by setting up our project and positioning the data files.

Next, we went on to set up the migration mechanism, one that was independent of the data format.

Then, we went ahead and wrote the template functions whose only job was to construct a Graql insert query based on the data passed to them.

After that, we learned how files with different data formats can be parsed into Python dictionaries.

Lastly, we ran `python3 migrate.py` which fired the `build_phone_call_graph` function with the given `inputs`. This loaded the data into our Grakn knowledge graph.

## Next

Now that we have some actual data in our knowledge graph, we can go ahead and [query for insights](/docs/examples/phone-calls-queries?tab=python).
