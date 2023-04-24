---
pageTitle: Migrating CSV, JSON and XML Data with Client Python
keywords: typedb, examples, migration, python
longTailKeywords: typedb python migration
Summary: Learn how to use Client Python to migrate CSV, JSON and XML data into a TypeDB Knowledge Graph.
---

## Goal

In this tutorial, our aim is to migrate some actual data to the `phone_calls` knowledge graph that we [defined previously](../08-examples/01-phone-calls-schema.md) using [Client Python](../02-clients/python/01-python-overview.md).

## A Quick Look at the Schema

Before we get started with migration, let’s have a quick reminder of how the schema for the `phone_calls` knowledge graph looks like.

![The Visualised Schema](../images/examples/phone_calls_schema.png)

## An Overview

Let’s go through a summary of how the migration takes place.

1.  we need a way to talk to our TypeDB [database](../06-management/01-database.md). To do this, we use [Client Python](../02-clients/python/01-python-overview.md).
2.  we go through each data file, extracting each data item and parsing it to a Python dictionary.
3.  we pass each data item (in the form of a Python dictionary) to its corresponding template function, which in turn gives us the constructed TypeQL query for inserting that item into TypeDB.
4.  we execute each of those queries to load the data into our target database — `phone_calls`.

Before moving on, make sure you have **Python3** and **Pip3** installed and the [**TypeDB Server**](/docs/typedb/install-and-run#start-the-typedb-server) running on your machine.

## Get Started

1.  Create a directory named `phone_calls` on your desktop.
2.  cd to the phone_calls directory via terminal.
3.  Run `pip3 install typedb-client` to install the TypeDB [Client Python](../02-clients/python/01-python-overview.md).
4.  Open the `phone_calls` directory in your favourite text editor.
5.  Create a `migrate.py` file in the root directory. This is where we’re going to write all our code.

## Include the Data Files

Pick one of the data formats below and download the files. After you download them, place the four files under the `files/phone-calls/data` directory. We need these to load their data into our `phone_calls` knowledge graph.

**CSV** | [companies](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/companies.csv) | [people](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/people.csv) | [contracts](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/contracts.csv) | [calls](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/calls.csv)

**JSON** | [companies](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/companies.json) | [people](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/people.json) | [contracts](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/contracts.json) | [calls](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/calls.json)

**XML** | [companies](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/companies.xml) | [people](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/people.xml) | [contracts](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/contracts.xml) | [calls](https://raw.githubusercontent.com/vaticle/typedb-examples/master/telecom/phone_calls/data/calls.xml)

## Set up the migration mechanism

All code that follows is to be written in `phone_calls/migrate.py`.

```python
from typedb.client import TypeDB 

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

First thing first, we import the typedb module. We use it for connecting to our `phone_calls` database.

Next, we declare the `inputs`. More on this later. For now, what we need to understand about inputs — it’s a list of dictionaries, each one containing:
- The path to the data file
- The template function that receives a dictionary and produces the TypeQL insert query. we define these template functions in a bit.

Let’s move on.

## build_phone_call_graph(inputs)

```python
from typedb.client import TypeDB, SessionType

def build_phone_call_graph(inputs):
    with TypeDB.core_client("localhost:1729") as client:
        with client.session("phone_calls", SessionType.DATA) as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into TypeDB ...")
                load_data_into_typedb(input, session)

# ...
```

This is the main and only function we need to call to start loading data into TypeDB.

What happens in this function, is as follows:

1.  A TypeDB `client` is created, connected to the server we have running locally.
2.  A `session` is created, connected to the database `phone_calls`. Note that by using `with`, we indicate that the session closes after it’s been used.
3.  For each `input` dictionary in `inputs`, we call the `load_data_into_typedb(input, session)`. This takes care of loading the data as specified in the input dictionary into our database.

## load_data_into_typedb(input, session)

```python
from typedb.client import TransactionType

def load_data_into_typedb(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:
        with session.transaction(TransactionType.WRITE) as transaction:
            typeql_insert_query = input["template"](item)
            print("Executing TypeQL Query: " + typeql_insert_query)
            transaction.query().insert(typeql_insert_query)
            transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into TypeDB.\n")

# ...
```

In order to load data from each file into TypeDB, we need to:

1.  retrieve a list containing dictionaries, each of which represents a data item. We do this by calling `parse_data_to_dictionaries(input)`
2.  for each dictionary in `items`: a) create a `transaction`, which closes once used, b) construct the `typeql_insert_query` using the corresponding template function, c) execute the query and d) commit the transaction.

<div class="note">
[Important]
To avoid running out of memory, it’s recommended that every single query gets created and committed in a single transaction.
However, for faster migration of large datasets, this can happen once for every `n` queries, where `n` is the maximum number of queries guaranteed to run on a single transaction.
</div>

Before we move on to parsing the data into dictionaries, let’s start with the template functions.

## The Template Functions

Templates are simple functions that accept a dictionary, representing a single data item. The values within this dictionary fill in the blanks of the query template. The result is a TypeQL insert query.
We need 4 of them. Let’s go through them one by one.

### company_template

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

```typeql
insert $company isa company, has name "Telecom";
```

### person_template

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

- Goes in:
```python
{ "phone_number": "+44 091 xxx" }
```

- Comes out:

```typeql
insert $person isa person, has phone-number "+44 091 xxx", has is-customer false;
```

or:

- Goes in:
```python
{ "first_name": "Jackie", "last_name": "Joe", "city": "Jimo", "age": 77, "phone_number": "+00 091 xxx"}
```

- Comes out:

```typeql
insert $person isa person, has phone-number "+00 091 xxx", has is-customer true, has first-name "Jackie", has last-name "Joe", has city "Jimo", has age 77;
```

### contract_template

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

- Goes in:
```python
{ "company_name": "Telecom", "person_id": "+00 091 xxx" }
```

- Comes out:

```typeql
match $company isa company, has name "Telecom"; $customer isa person, has phone-number "+00 091 xxx"; insert (provider: $company, customer: $customer) isa contract;
```

### call_template

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

- Goes in:
```python
{ "caller_id": "+44 091 xxx", "callee_id": "+00 091 xxx", "started_at": 2018-08-10T07:57:51, "duration": 148 }
```

- Comes out:

```typeql
match $caller isa person, has phone-number "+44 091 xxx"; $callee isa person, has phone-number "+00 091 xxx"; insert $call(caller: $caller, callee: $callee) isa call; $call has started-at 2018-08-10T07:57:51; $call has duration 148;
```

We’ve now created a template for each and all four concepts that were [previously](../08-examples/01-phone-calls-schema.md) defined in the schema.

It’s time for the implementation of `parse_data_to_dictionaries(input)`.

## DataFormat-specific Implementation

The implementation for `parse_data_to_dictionaries(input)` differs based on the format of our data files.

<div class="tabs light">

[tab:CSV]
We use Python’s built-in [`csv` library](https://docs.python.org/3/library/csv.html#dialects-and-formatting-parameters). Let’s import the module for it.

```python
from typedb.client import TypeDB
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
from typedb.client import TypeDB
import ijson

# ...
```

Moving on, we write the implementation of `parse_data_to_dictionaries(input)` for processing `.json` files.

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
We use Python’s built-in [`xml.etree.cElementTree` library](https://docs.python.org/2/library/xml.etree.elementtree.html). Let’s import the module for it.

```python
from typedb.client import TypeDB
import xml.etree.cElementTree as et

# ...
```

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
                ## convert the buffer (string) to a structured tag
                tnode = et.fromstring(buffer)
                ## parse the tag to a dictionary
                item = {}
                for element in list(tnode):
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
from typedb.client import TypeDB, SessionType, TransactionType
import csv

def build_phone_call_graph(inputs):
    with TypeDB.core_client("localhost:1729") as client:
        with client.session("phone_calls", SessionType.DATA) as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into TypeDB ...")
                load_data_into_typedb(input, session)

def load_data_into_typedb(input, session):
    items = parse_data_to_dictionaries(input)

    with session.transaction(TransactionType.WRITE) as transaction:
        for item in items:
            typeql_insert_query = input["template"](item)
            print("Executing TypeQL Query: " + typeql_insert_query)
            transaction.query().insert(typeql_insert_query)
        transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into TypeDB.\n")

def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'

def person_template(person):
    # insert person
    typeql_insert_query = 'insert $person isa person, has phone-number "' + person["phone_number"] + '"'
    if person["first_name"] == "":
        # person is not a customer
        typeql_insert_query += ", has is-customer false"
    else:
        # person is a customer
        typeql_insert_query += ", has is-customer true"
        typeql_insert_query += ', has first-name "' + person["first_name"] + '"'
        typeql_insert_query += ', has last-name "' + person["last_name"] + '"'
        typeql_insert_query += ', has city "' + person["city"] + '"'
        typeql_insert_query += ", has age " + str(person["age"])
    typeql_insert_query += ";"
    return typeql_insert_query

def contract_template(contract):
    # match company
    typeql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    typeql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    typeql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return typeql_insert_query

def call_template(call):
    # match caller
    typeql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    typeql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    typeql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return typeql_insert_query

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
from typedb.client import TypeDB, SessionType, TransactionType
import ijson

def build_phone_call_graph(inputs):
    with TypeDB.core_client("localhost:1729") as client:
        with client.session("phone_calls", SessionType.DATA) as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into TypeDB ...")
                load_data_into_typedb(input, session)

def load_data_into_typedb(input, session):
    items = parse_data_to_dictionaries(input)

    with session.transaction(TransactionType.WRITE) as transaction:
        for item in items:
            typeql_insert_query = input["template"](item)
            print("Executing TypeQL Query: " + typeql_insert_query)
            transaction.query().insert(typeql_insert_query)
        transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into TypeDB.\n")

def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'

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

def contract_template(contract):
    # match company
    typeql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    typeql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    typeql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return typeql_insert_query

def call_template(call):
    # match caller
    typeql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    typeql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    typeql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return typeql_insert_query

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
from typedb.client import TypeDB, SessionType, TransactionType
import xml.etree.cElementTree as et

def build_phone_call_graph(inputs):
    with TypeDB.core_client("localhost:1729") as client:
        with client.session("phone_calls", SessionType.DATA) as session:
            for input in inputs:
                print("Loading from [" + input["data_path"] + "] into TypeDB ...")
                load_data_into_typedb(input, session)

def load_data_into_typedb(input, session):
    items = parse_data_to_dictionaries(input)

    with session.transaction(TransactionType.WRITE) as transaction:
        for item in items:
            typeql_insert_query = input["template"](item)
            print("Executing TypeQL Query: " + typeql_insert_query)
            transaction.query().insert(typeql_insert_query)
        transaction.commit()

    print("\nInserted " + str(len(items)) + " items from [ " + input["data_path"] + "] into TypeDB.\n")

def company_template(company):
    return 'insert $company isa company, has name "' + company["name"] + '";'

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

def contract_template(contract):
    # match company
    typeql_insert_query = 'match $company isa company, has name "' + contract["company_name"] + '";'
    # match person
    typeql_insert_query += ' $customer isa person, has phone-number "' + contract["person_id"] + '";'
    # insert contract
    typeql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return typeql_insert_query

def call_template(call):
    # match caller
    typeql_insert_query = 'match $caller isa person, has phone-number "' + call["caller_id"] + '";'
    # match callee
    typeql_insert_query += ' $callee isa person, has phone-number "' + call["callee_id"] + '";'
    # insert call
    typeql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return typeql_insert_query

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
                ## parse the tag to a dictionary and append to items
                item = {}
                for element in list(tnode):
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

Sit back, relax and watch the logs while the data starts pouring into TypeDB.

### ... So Far With the Migration

We started off by setting up our project and positioning the data files.

Next, we went on to set up the migration mechanism, one that was independent of the data format.

Then, we went ahead and wrote the template functions whose only job was to construct a TypeQL insert query based on the data passed to them.

After that, we learned how files with different data formats can be parsed into Python dictionaries.

Lastly, we ran `python3 migrate.py` which fired the `build_phone_call_graph` function with the given `inputs`. This loaded the data into our TypeDB knowledge graph.

## Next

Now that we have some actual data in our knowledge graph, we can go ahead and [query for insights](../08-examples/05-phone-calls-queries.md?tab=python).
