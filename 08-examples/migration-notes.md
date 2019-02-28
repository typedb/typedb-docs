## Migration Process

### Constructing Input JSON

The first step in the migration process is to read the data files and insert them into a pre-defined JSON structure. This JSON object will then be used by the corresponding template function to construct the Graql insert query.

### Constructing Graql Insert Queries

Construction of the Graql insert queries is the job of template functions. A template function is one that received the Input JSON and uses the data contained within it to construct and return the Graql insert query.

#### Custom Templates vs. Generic Templates

The template functions can be either custom for each type as defined in the schema, or generic for any type. It is possible to have a collection of templates that are only one of these two types, but each approach comes with its own limitations.

Writing completely generic template functions that cover all common and specific scenarios of constructing Graql insert queries, result in:

- complex structure for the Input JSON that is hard to understand
- complex implementation of the template function that becomes difficult to troubleshoot

Writing completely custom template functions, one for each type, can become very time consuming, especially in cases that there are many types defined in the schema.

The best approach is to take advantage of both types, that is to have

- generic template functions to cover the majority of the cases, and
- custom template functions for special edge cases.

### Preparing the Execution List

The next step is to add each of the constructed Graql insert queries to a list which will later be iterated for execution. To ensure that every query can be successfully executed, the order of the queries in the list matters. Queries that are meant to insert relationships (that rely on the existence of other instances), should be placed towards the end of the list, or stored in separate lists altogether.

#### Avoiding Duplicates

Although it is possible to rely on Grakn for checking for pre-existence of a particular instance prior to inserting it, it results in the execution of extra transactions that add to the migration time. Instead, a much better approach is to validate the uniqueness of the Graql insert queries, before inserting them. The most effective method to do this is to avoid appending identical Graql insert queries to the final list. This covers the most common cases of duplicated data. There may be more complex cases that require a custom validator which acts a gateway to appending the queries to the final list.

### Execution

Lastly, the list(s) containing the Graql insert queries are passed on to a function that uses a transaction to execute bulks of the queries on the given keyspace. This step can be performed concurrently for better performance, given that the order of the queries being executed is taken into account.