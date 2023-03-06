---
pageTitle: Reading data
keywords: typeql, query, match, pattern, read
longTailKeywords: typeql match, match get, typeql read, typedb read
Summary: Reading data in TypeDB.
---

# Reading data

To get data (and/or schema types) from a database, run queries which consist of match and/or get clauses in a `read` 
transaction.

To try the following examples use [TypeDB Studio](../../02-clients/01-studio.md) or other TypeDB 
[Clients](../../02-clients/00-clients.md).

## Get query

A get query is used to extract data instances or types (schema concepts) out of a database by describing the desired 
result in the preceding match clause. Use modifiers such as `limit`, `sort` and `offset` to retrieve an optionally 
sorted subset of the matched instances.

The get query triggers a search in a database based on what has been described in the match clause. 

### Syntax

Get queries are written in TypeQL with the following syntax:

```bash
match pattern [(, pattern)...] 
[get <variable> [(, <variable>)...];] 
[sort <variable> [asc|desc];] 
[offset <value>;] 
[limit <value>;] 
[group <variable>;] 
[count;] [sum|max|min|mean|median|std <variable>;]
```

Patterns consist of variables and properties for data instances. For more information see the 
[Query pattern anatomy](03-match.md#query-pattern-anatomy) section.

<div class="note">
[Note]
Get clause works like a filter for results. Get query without a get clause will have all variables mentioned in match 
patterns returned.
</div>

Aggregation functions must be at the end of the query and do not require a GET clause.

### Variables

A `get` clause is used to specify which variables to include in the results. If omitted, every variable is included.

```typeql
match 
  $p isa person, has name "Kevin Morrison", has email $e;
get $e;
```

The example above matches person (`$p`) with a `full-name` attribute value of `Kevin Morrison`, and `email` attribute 
(`$e`). The `get` clause then filters the results to receive only the `email` (`$e`) attributes.

```typeql
match
  $pe ($x, $y) isa permission;
  $x isa person, has full-name $x-n;
  $x-n contains "Kevin";
  $y (accessed-object: $o, valid-action: $act) isa access;
  $act has action-name $act-n;
  $o has path $o-fp;
get $x-n, $act-n, $o-fp;
```

The example above uses a `match` clause to do the following:

1. Find `permission` relation (`$pe`) of `$x` and `$y` variables.
2. Finds `$x` as `person` entities that have `full-name` attribute with value of `$x-n`. 
3. `$x-n` should contain string `Kevin`.
4. Finds `access` relation of `$o` as accessed-object and `$act` as valid-action.
5. `$act` should have `action-name` attribute with value of `$act-n`.
6. `$o` should have `path` attribute with value of `$o-fp`.

The `get` clause then filters the result from the `match` clause to get only the `person`’s `full-name` (`$x-n`), 
`action`’s `action-name` (`$act-n`) and `path` of an `object` (`$o-fp`). Every returned result should contain all 
three variables.

### Modifiers

#### Limit the results

Use the `limit` keyword followed by the maximum number of results to limit the number of results returned.

```typeql
match $p isa person; 
get $p;
limit 1;
```

This query returns only one single (and random) instance of type `person`. Consider using `limit` with 
[sorting aggregation](#sort-the-answers) to receive less random and more predictable results.

#### Sort the Answers

Use the `sort` keyword followed by a variable, to sort the answers by the variable. A second argument is optional 
and determines the sorting order: `asc` (ascending) or `desc` (descending). By default it’s ascending.

```typeql
match $p isa person, has full-name $n; 
get $n; 
sort $n asc;
```

This query returns all `full-name` attributes of all `person` entities, sorted by their `full-name` in ascending order.

To sort by multiple variables use the same syntax and add additional variables and optional sorting order arguments 
with a comma separator. 

For example:

```typeql
match $p isa person, has full-name $n, has email $e; 
get $n, $e; 
sort $n asc, $e desc;
```

The example above will return all `full-name` and `email` attributes of all `person` entities, sorted by their 
`full-name` in ascending order first and then by `email` in descending order.

#### Offset the Answers

Use the `offset` keyword followed by the number to offset the answers by. This is commonly used with the `limit` 
keyword to return a desired range of the answers. Don’t forget to [sort](#sort-the-answers) the results to guarantee 
they will stay in the same order while you move through them.

```typeql
match $p isa person, has full-name $n; 
get $n; 
sort $n asc; 
offset 6; limit 10;
```

This sorts the `full-name` attributes of all `person` entities in ascending order, skips the first six and returns up 
to the next ten. 

For those developing applications with [TypeDB drivers](../../02-clients/00-clients.md#typedb-drivers), please see the 
instructions and examples for a specific language/framework: [Java](../../02-clients/03-java.md), 
[Node.js](../../02-clients/05-nodejs.md), [Python](../../02-clients/04-python.md).

## Group

We use the `group` function, optionally followed by another aggregate function, to group the answers by the 
specified matched variable.

```typeql
match
  $pe ($x, $y) isa permission;
  $x isa person, has full-name $x-n;
  $y (accessed-object: $o, valid-action: $act) isa access;
  $act has action-name $act-n;
  $o has path $o-fp;
get $x-n, $act-n, $o-fp; 
sort $o-fp asc;
limit 3;
group $o-fp;
```

This query returns the `full-name` attributes of all `person` entities, the `path` attributes of the `object` entities 
in any `access` relations that are part of the `permission` relation with the `person` entities and the `action-name` 
attribute of the `action` entity in those `access` relations. The results are then sorted by the `path` attribute in 
ascending order, limited by only first 3 results and grouped by `path` variable values.

The following or similar result can be obtained by running the query above without inference on the TypeDB server with 
the IAM schema and dataset from the [Quickstart guide](../01-start/03-quickstart.md).

```typeql
"LICENSE" isa path => {
    {
        $act-n "modify_file" isa action-name;
        $x-n "Pearle Goodman" isa full-name;
        $o-fp "LICENSE" isa path;
    }    {
        $act-n "modify_file" isa action-name;
        $x-n "Kevin Morrison" isa full-name;
        $o-fp "LICENSE" isa path;
    }
}
"README.md" isa path => {
    {
        $act-n "modify_file" isa action-name;
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

## Aggregation

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

```typeql 
match $f isa file, has size-kb $s; get $s;
```

If you query the example above, only attribute `$s` will be returned with its value. But all the duplicated values of 
`$s` will be omitted. Because what we are querying is all attribute instances. And when two different entities have 
the same attribute (with the same value) it's still only one attribute.

So it’s just like to query only unique values. For example, if there are three files with the same value of `size-kb` 
attribute = 10, we will get only one of this value.

if we want to prevent that we should return not only attributes, but also the entities that own the attributes in the 
`get` clause. For example:

```typeql 
match $f isa file, has size-kb $s; get $f, $s;
```

This will return pairs of `$f` and `$s`, including all duplicated values of `$s` (every `file` instance with its 
attribute of `size-kb`. Including all of the same values owned by different files. For example, all three values of 10 
will be returned this way).
</div>

### Count

Use the count keyword to get the number of the specified matched variable.

```typeql 
match
  $o isa object, has path $fp;
get $o, $fp; count;
```

<div class="note">
[Note]
The `count` function is applied to every result returned. If more than one variable mentioned in get, than count 
will show the number of unique results. This is also the case, when no `get` clause added, which actually means that 
all matched variables are included.
</div>

```typeql 
match
  $pe ($x, $y) isa permission;
  $x isa person, has full-name $x-n;
  $y (accessed-object: $o, valid-action: $act) isa access;
  $act has action-name $act-n;
  $o has path $o-fp;
get $x-n, $act-n, $o-fp; group $o-fp; count;
```

This query returns the total count of person instances that has full-name, any access to an object with path and with 
a valid action for every group (grouped by the path of the object).

<div class="note">
[Note]
The `group` clause should go before the aggregation function.
</div>

### Sum

Use the `sum` keyword to get the sum of the specified `long` or `double` values of matched variable.

```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; 
sum $s;
```

### Maximum

Use the `max` keyword to get the maximum value among the specified `long` or `double` values of matched variable.

```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; max $s;
```

### Minimum

Use the `min` keyword to get the minimum value among the specified `long` or `double` values of matched variable.

```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; min $s;
```

### Mean

Use the `mean` keyword to get the average value of the specified `long` or `double` values of matched variable.

```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; mean $s;
```

### Median

Use the `median` keyword to get the median value among the specified `long` or `double` values of matched variable.

```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; median $s;
```

### Standard deviation

Use the `std` keyword to get the standard deviation value among the specified `long` or `double` values of matched 
variable. Usually used with the average value, returned by the mean keyword.

```typeql 
match
  $f isa file, has size-kb $s;
get $f, $s; std $s;
```
