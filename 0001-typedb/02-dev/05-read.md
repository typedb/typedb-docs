---
pageTitle: Reading data
keywords: typeql, query, match, pattern, read
longTailKeywords: typeql match, match get, typeql read, typedb read
Summary: Reading data from a TypeDB database.
---

# Reading data

There is only one query type to retrieve data instances and types from a database: get query.

To try the following examples use [TypeDB Studio](../../02-clients/01-studio.md) or other TypeDB 
[Clients](../../02-clients/00-clients.md).

For those developing applications with [TypeDB drivers](../../02-clients/00-clients.md#typedb-drivers), please see the 
instructions and examples of how to send a query for a specific language/framework: 
[Java](../../02-clients/03-java.md), 
[Node.js](../../02-clients/05-nodejs.md), 
[Python](../../02-clients/04-python.md).

## Get query

A get query triggers a search in a database based on what has been described in the `match` clause. It is 
used to extract concepts (data instances or types) out of a database. The result of a get query can be quite different, 
depending on the query itself ([modifiers](#modifiers), [aggregation](#aggregation), [grouping](#group)) 
and transaction options ([inference](06-infer.md#inferring-data)). For more information see the 
[Response interpretation](07-response.md) page.

### Syntax

Get queries are written in TypeQL with the following syntax:

```bash
match <pattern>
[get <variable> [(, <variable>)...];] 
[sort <variable> [asc|desc];] 
[offset <value>;] 
[limit <value>;] 
[group <variable>;] 
[count;] [sum|max|min|mean|median|std <variable>;]
```

<div class="note">
[Note]
A pattern consists of variables and constraints for concepts. For more information see the 
[Pattern syntax](03-match.md#pattern-syntax) section.
</div>

<div class="note">
[Important]
A `get` clause works like a filter for variables in matched answers. Get query without a `get` clause will have all 
variables mentioned in `match` clause pattern to be returned as concepts in every answer.
</div>

Aggregation functions, as well as modifiers, and grouping must be at the end of the query and do not require a `get` 
clause.

### Variables

A `get` clause is used to specify which variables to include in the results. If omitted, every variable is included.

<!-- test-ignore -->
```typeql
match 
  $p isa person, has name "Kevin Morrison", has email $e;
get $e;
```

The example above matches person (`$p`) with a `full-name` attribute value of `Kevin Morrison`, and `email` attribute 
(`$e`). The `get` clause then filters the results to receive only the `email` (`$e`) attributes.

<!-- test-ignore -->
```typeql
match
  $pe ($x, $y) isa permission;
  $x isa person, has full-name $x-n;
  $x-n contains "Kevin";
  $y (object: $o, action: $act) isa access;
  $act has name $act-n;
  $o has path $o-fp;
get $x-n, $act-n, $o-fp;
```

The example above uses a `match` clause to do the following:

1. Finds `permission` relation (`$pe`) of `$x` and `$y` variables.
2. Finds `$x` as `person` entities that have `full-name` attribute with value of `$x-n`. 
3. `$x-n` should contain string `Kevin`.
4. Finds `access` relation of `$o` as object and `$act` as action.
5. `$act` should have `name` attribute with value of `$act-n`.
6. `$o` should have `path` attribute with value of `$o-fp`.

The `get` clause then filters the answers from the `match` clause to get only the `person`’s `full-name` (`$x-n`), 
`action`’s `name` (`$act-n`) and `path` of an `object` (`$o-fp`). Every returned result should contain all 
three concepts.

### Number of answers

The number of answers returned depends on the get query (mostly `match` clause pattern) and database data/schema.

For example, if we have **3** `person` entities and **10** `file` entities in a database with the IAM schema and  
send the following get query:

<!-- test-ignore -->
```typeql
match
  $x isa person;
  $f isa file;
get $x, $f; 
```

How many results are we expecting to retrieve from a database?

<div class="note">
[Note]
Spoiler: **13** is the wrong answer here.
</div>

As the example above doesn't have any [modifiers](#modifiers), [aggregation](#aggregation), or [grouping](#group) 
the number of results will depend on the number of matched solutions for pattern in the `match` clause. So the 
TypeDB query processor will explore all possible solutions: every solution consisting of exactly one `person` entity 
and one `file` entity. There are only `3 * 10 = 30` possible combinations of person and file entities, so we will 
get 30 answers.

See the [Patterns overview](03-match.md#patterns-overview) section of the Matching patterns page for more information.

### Modifiers

#### Limit the results

Use the `limit` keyword followed by a positive integer to limit the number of results (answers) returned.

<!-- test-ignore -->
```typeql
match $p isa person; 
get $p;
limit 1;
```

This query returns only one single (and random) instance of type `person`. Consider using `limit` with 
[sorting aggregation](#sort-the-answers) to receive less random and more predictable results.

#### Sort the Answers

Use the `sort` keyword followed by a variable, to sort the answers using a variable mentioned in the first argument. A 
second argument is optional and determines the sorting order: `asc` (ascending, be default) or `desc` (descending).

<!-- test-ignore -->
```typeql
match $p isa person, has full-name $n; 
get $n; 
sort $n asc;
```

This query returns all `full-name` attributes of all `person` entities, sorted by the value of `full-name` in ascending 
order.

To sort by multiple variables use the same syntax and add additional variables and optional sorting order arguments 
with a comma separator. 

For example:

<!-- test-ignore -->
```typeql
match $p isa person, has full-name $n, has email $e; 
get $n, $e; 
sort $n asc, $e desc;
```

The example above will return all `full-name` and `email` attributes of all `person` entities, sorted by their 
`full-name` in ascending order first and then by `email` in descending order.

#### Offset the Answers

Use the `offset` keyword followed by the number to offset the answers by. This is commonly used with the `limit` 
keyword to return a desired range of the answers. Don’t forget to [sort](#sort-the-answers) the results to ensure 
predictable and deterministic results.

<!-- test-ignore -->
```typeql
match $p isa person, has full-name $n; 
get $n; 
sort $n asc; 
offset 6; limit 10;
```

This sorts the `full-name` attributes of all `person` entities in ascending order, skips the first six and returns up 
to the next ten. 

### Group

We use the `group` function, optionally followed by another aggregate function, to group the answers by the 
specified matched variable.

<!-- test-ignore -->
```typeql
match
  $pe ($x, $y) isa permission;
  $x isa person, has full-name $x-n;
  $y (object: $o, action: $act) isa access;
  $act has name $act-n;
  $o has path $o-fp;
get $x-n, $act-n, $o-fp; 
sort $o-fp asc;
limit 3;
group $o-fp;
```

This query returns the `full-name` attributes of all `person` entities, the `path` attributes of the `object` entities 
in any `access` relations that are part of the `permission` relation with the `person` entities and the `name` 
attribute of the `action` entity in those `access` relations. The results are then sorted by the `path` attribute in 
ascending order, limited by only first 3 results and grouped by `path` variable values.

The following or similar result can be obtained by running the query above without inference on the TypeDB server with 
the IAM schema and dataset from the [Quickstart guide](../01-start/03-quickstart.md).

<!-- test-ignore -->
```typeql
"LICENSE" isa path => {
    {
        $act-n "modify_file" isa name;
        $x-n "Pearle Goodman" isa full-name;
        $o-fp "LICENSE" isa path;
    }    {
        $act-n "modify_file" isa name;
        $x-n "Kevin Morrison" isa full-name;
        $o-fp "LICENSE" isa path;
    }
}
"README.md" isa path => {
    {
        $act-n "modify_file" isa name;
        $x-n "Pearle Goodman" isa full-name;
        $o-fp "README.md" isa path;
    }
}
```

<div class="note">
[Note]
There can be a difference in the `full-name` value for the `README.md` file since we used `sort` by the `path` and not 
the `full-name`.
</div>

### Aggregation

Aggregation performs a calculation on a set of values, and returns a single value. 

TypeDB supports the following types of aggregation:

- count
- sum
- max
- mean
- median

To perform aggregation in TypeDB, we first write a [match clause](03-match.md) to describe the set of data, then follow 
that by get to retrieve a distinct set of answers based on the specified variables, and lastly an aggregate 
function to perform on the variable of interest.

<div class="note">
[Note]
Aggregation uses data returned by the query to perform the calculation. 

For example:

<!-- test-ignore -->
```typeql 
match $f isa file, has size-kb $s; get $s;
```

If we query the example above, only attribute `$s` will be returned with its value. But all the duplicated values of 
`$s` will be omitted. Because what we are querying is all attribute instances. And when two different entities have 
the same attribute (with the same value) it's still only one attribute.

So it’s just like to query only unique values. For example, if there are three files with the same value of `size-kb` 
attribute = 10, we will get only one of this value.

if we want to prevent that we should return not only attributes, but also the entities that own the attributes in the 
`get` clause. For example:

<!-- test-ignore -->
```typeql 
match $f isa file, has size-kb $s; get $f, $s;
```

This will return pairs of `$f` and `$s`, including all duplicated values of `$s` (every `file` instance with its 
attribute of `size-kb`. Including all of the same values owned by different files. For example, all three values of 10 
will be returned this way).
</div>

#### Count

Use the count keyword to get the number of the specified matched variable.

<!-- test-ignore -->
```typeql 
match
  $o isa object, has path $fp;
get $o, $fp; count;
```

<div class="note">
[Note]
The `count` function is applied to every result returned. If more than one variable mentioned in get, then `count` 
will show the number of unique combinations of results. This is also the case when no `get` clause is added, which 
actually means that all matched variables are included.
</div>

<!-- test-ignore -->
```typeql 
match
  $pe ($x, $y) isa permission;
  $x isa person, has full-name $x-n;
  $y (object: $o, action: $act) isa access;
  $act has name $act-n;
  $o has path $o-fp;
get $x-n, $act-n, $o-fp; group $o-fp; count;
```

This query returns the total count of `person` instances that have `full-name` as well as any `access` to an `object` 
with `path` and with a `valid action` for every group (grouped by the `path` of the `object`).

<div class="note">
[Note]
The `group` clause should go before the aggregation function.
</div>

#### Sum

Use the `sum` keyword to get the sum of the specified `long` or `double` values of matched variable.

<!-- test-ignore -->
```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; 
sum $s;
```

<div class="note">
[Warning]
Omitting the variable `$f` in the `get` clause` of the above query will result in missing all duplicated values of `$s`
from the aggregation. For more information see the [matching patterns](03-match.md#patterns-overview) page.
</div>

#### Maximum

Use the `max` keyword to get the maximum value among the specified `long` or `double` values of matched variable.

<!-- test-ignore -->
```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; max $s;
```

#### Minimum

Use the `min` keyword to get the minimum value among the specified `long` or `double` values of matched variable.

<!-- test-ignore -->
```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; min $s;
```

#### Mean

Use the `mean` keyword to get the average value of the specified `long` or `double` values of matched variable.

<!-- test-ignore -->
```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; mean $s;
```

#### Median

Use the `median` keyword to get the median value among the specified `long` or `double` values of matched variable.

<!-- test-ignore -->
```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; median $s;
```

#### Standard deviation

Use the `std` keyword to get the standard deviation value among the specified `long` or `double` values of matched 
variable. Usually used with the average value, returned by the mean keyword.

<!-- test-ignore -->
```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; std $s;
```
