---
pageTitle: Writing data
keywords: typeql, typedb, query, insert, delete, update, write
longTailKeywords: typeql insert, typeql write data, typeql delete, typeql update
Summary: Writing data in a TypeDB database.
---

# Writing data

There are multiple query types that can modify data in a database with `write` transaction:

- insert query
- delete query
- update (or match-delete-insert query)

<div class="note">
[Note]
To modify the schema of a database, use [define](02-schema.md#define)/[undefine](02-schema.md#undefine) queries instead.
</div>

To try the following examples use [TypeDB Studio](../../02-clients/01-studio.md) or one of the other TypeDB 
[Clients](../../02-clients/00-clients.md).

For those developing applications with [TypeDB drivers](../../02-clients/00-clients.md#typedb-drivers), please see the 
instructions and examples for a specific language/framework: 
[Java](../../02-clients/03-java.md), 
[Node.js](../../02-clients/05-nodejs.md), 
[Python](../../02-clients/04-python.md).

## Insert query

An insert query, optionally preceded by a [match](03-match.md) clause, adds data (e.g., entities, relations and 
attributes) to a database.

### Syntax

Insert queries are written in TypeQL with the following syntax:

<!-- test-ignore -->
```typeql
[match <pattern>]
insert <pattern>
```

The optional `match` clause uses a pattern to find existing data which is needed to insert new data. 
For example, to insert a new relation, we need to match every entity, attribute, and/or other relation that will 
play a role in it to be able to address them in the `insert` clause. 

The `insert` clause uses patterns to specify the data to be inserted and may include existing data found by 
the `match` clause.

<div class="note">
[Note]
A pattern consists of variables and constraints for concepts. For more information see the 
[Pattern syntax](03-match.md#pattern-syntax) section.
</div>

The `insert` query is the only data query that can be without a `match` clause. In that case the pattern in the `insert` 
clause will be used exactly once per query. 

In case there is a `match` clause before an `insert` clause then the number of inserts will depend on the number of 
answers matched by `match` clause. In that case `insert` clause will be executed once per every matched answer.

<div class="note">
[Important]
If there is no matches for a `match` clause in an `insert` query then there will be no inserts. 
</div>

<div class="note">
[Note]
The `insert` clause can have multiple patterns to insert in one query. But it can’t insert types (use 
[define](02-schema.md#define) to insert new types) and can’t have the following:

- Conjunction
- Disjunction
- Negation
- `is` keyword

</div>

#### Example insert query

<!-- test-ignore -->
```typeql
insert $p isa person, has full-name "Bob";
```

The above query inserts a `person` entity with a `full-name` attribute whose value is "Bob".

<div class="note">
[Note]
If there is no attribute with this value then it will be created by this query.
</div>

#### Example match-insert query

<!-- test-ignore -->
```typeql
match 
  $p isa person, has full-name "Bob"; 
insert 
  $p has email "bob@vaticle.com";
```

The above query finds a `person` entity whose `full-name` attribute has a value of `Bob`, and makes it the owner of 
an `email` attribute with a value of `bob@vaticle.com`.

### Entities

Use the `insert` keyword followed by a pattern to insert an entity.

<!-- test-ignore -->
```typeql
insert $p isa person, has full-name "John Parkson", has email "john.parkson@gmail.com", has credential "qwerty1";
```

The above query inserts a `person` entity with following attributes: 

- `full-name` – value is `John Parkson`, 
- `email` – value is `john.parkson@gmail.com`,
- `credential` – value is `qwerty1`.

<div class="note">
[Note]
If the above query were to be run multiple times, it would create multiple `person` entities – all owning the 
same attributes. 

However, if the `person` entity type definition specified an `email` attribute with the `@key` keyword 
(which adds a [uniqueness constraint](02-schema.md#assign-an-attribute-to-an-entity-as-a-unique-identifier)), 
the query would succeed the first time and fail every time thereafter because, in this case, only one `person` entity 
can own any `email` attribute with a specific value.
</div>

### Attributes

There are three ways to insert attributes:

- Insert an attribute on its own (e.g., independent of any entities, relations, or attributes).
- Insert an attribute owned by a new entity, relation, or attribute.
- Insert an attribute owned by an existing entity, relation, or attribute.

Use the `insert` keyword followed by a pattern to insert an attribute.

<!-- test-ignore -->
```typeql
insert $s 34 isa size-kb;
```

The above query inserts a `size-kb` attribute with a value of `34`. The variable `$s` is optional.

However, it is more common to insert one or more attributes with a new entity, relation, or attribute as owner.

<!-- test-ignore -->
```typeql
insert $f isa file, has size-kb 34;
```

The above query inserts a new `file` entity owning a `size-kb` attribute with a value of `34`.

Use variables from the optional `match` clause in the `insert` clause to create a required context. 
For example, to specify an existing owner for a new attribute:

<!-- test-ignore -->
```typeql
match 
  $f isa file, has path "README.md"; 
insert 
  $f has size-kb 55;
```

In the above query, the `match` clause finds a `file` entity, or multiple entities, owning a `path` attribute with a 
value of `README.md`. Then, it makes the matching entity/entities own a `size-kb` attribute with a value of `55`.

<div class="note">
[Note]
In the last two examples, if there was an existing `size-kb` attribute with a specified value, a new attribute would 
not be created. Instead, the `file` entity would end up owning the existing one. If an existing one did not exist, a 
new attribute would be created and owned by the `file` entity.
</div>

<!---  #todo Doublecheck the term for attribute ownership cardinality! -->

#### Multivalued attributes

TypeDB supports multivalued attributes by allowing entities, relations, and attributes to own multiple attributes 
of the same attribute type. 

For example, if the `person` entity type can own an `email` attribute type, a `person` entity can own multiple (from 
0 to many) number of `email` attributes with different values.

##### Example 1

<!-- test-ignore -->
```typeql
match 
  $p isa person, has name "John Parkson"; 
insert 
  $p has email "john.parkson@vaticle.com", has email "admin@jp.com", has email "jp@gmail.com";
```

This query will assign ownership of 3 different attributes of the `email` type to the matched `person` entity 
(or entities).

See the illustration from [TypeDB Studio](../../02-clients/01-studio.md) below.

![John with 6 attributes, 4 of which are email type](../../images/studio/john-6-attributes.png)

##### Example 2

<!-- test-ignore -->
```typeql
match 
  $f isa file, has path "README.md"; 
insert 
  $f has size-kb 55, has size-kb 65, has size-kb 70, has path "README2.md";
```

In the above query, `match` clause finds a `file` entity (or entities) owning a `path` attribute with a value of 
`README.md`. Then, it inserts  ownerships of an additional `path` attribute and three additional `size-kb` attributes. 
If the `file` entity/entities owned one `path` attribute and no `size-kb` attribute before the query, it would own two 
`path` attributes and three `size-kb` attributes after it. 

See the illustration from [TypeDB Studio](../../02-clients/01-studio.md) below.

![Readme with multiple size-kb attributes](../../images/studio/readme-with-multiple-sizes.png)

### Relations

Unlike entities and attributes, the `match` clause is required when inserting relations (i.e., a match insert) 
because the roles in a relation are expected to be played by existing entities, other relations or attributes. 
Thus, the `match` clause is used to identify the players of roles in a new relation.

<!-- test-ignore -->
```typeql
match 
  $f isa file, has path "iopvu.java"; 
  $op isa operation, has name "view_file"; 
insert 
  $a (object: $f, action: $op) isa access;
```

In the above example we match our role players before inserting a relation. The number of relations being inserted 
depends on the number of matched results. In our [IAM dataset](../01-start/03-quickstart.md#insert-data) there is only 
one match by default. But if there will three results matched by the `match` clause — there are three relations 
being inserted here.

<div class="note">
[Note]
You can insert a relation with some roles missing a role player, but that represents an incomplete data state (as 
existence of a relation suggest existence of its role players) and there needs to be at least one role player in an 
inserted relation.
</div>

#### Multiple role players

<div class="note">
[Note]
In versions `1.7.0` and higher, a role in a relation can be played by multiple players in the same way an entity can 
have multiple attributes of the same type.
</div>

<!-- test-ignore -->
```typeql
match
  $p1 isa subject, has full-name "Pearle Goodman"; 
  $p2 isa subject, has full-name "Masako Holley"; 
  $o isa object, has path "zewhb.java"; 
insert 
  $obj-ownership (object-owner: $p1, object-owner: $p2, owned-object: $o) isa object-ownership;
```

The above query:

1. Finds a `person` entity (`$p1`) by its `full-name` attribute `Pearle Goodman`. 
2. Finds a `person` entity (`$p2`) by its `full-name` attribute `Masako Holley`. 
3. Finds an `object` entity (`$o`, `zewhb.java`). 
4. Inserts an `object-ownership` relation (`$obj-ownership`) which relates `$p1` (as `object-owner`) and `$p2` (as 
  `object-owner`) to `$o` (as `owned-object`).

In short, it makes `Pearle Goodman` and `Masako Holley` owners of the `zewhb.java` file.

#### Relations as role players

In addition to entities and attributes, roles of relations can be played by other relations.

<!-- test-ignore -->
```typeql
match 
  $s isa subject, has full-name "Pearle Goodman"; 
  $o isa object, has path "zewhb.java"; 
  $a isa action, has name "modify_file";
  $ac (object: $o, action: $a) isa access; 
insert 
  $p (subject: $s, access: $ac) isa permission;
```
The above query:

1. Finds a `subject` (`$s`) whose `full-name` attribute has a value of `Pearle Goodman`. 
2. Finds an `object` (`$o`) 
   whose `path` attribute has a value of `zewhb.java`.
3. Finds an `action` (`$a`) whose name attribute has a value of `modify_file`.
4. Finds an `access` relation (`$ac`) that relates the `$o` (as `access-object`) to `$a` (as `action`). 
5. Inserts a `permission` relation that relates `$s` (as `subject`) to the relation `$ac` (as 
   `access`).

In short, it creates a `permission` letting `Pearle Goodman` modify the `zewhb.java` file.

The relation of `access` type now plays role of `access` in the inserted relation of the `permission` type.

<div class="note">
[Warning]
If `match` clause returns multiple matched solutions, then the `insert` clause is executed for every one of them.

For more information see the [Matching patterns](03-match.md#patterns-overview) page.
</div>

## Delete query

A delete query is always preceded by a `match` clause and removes data from a database. It can be used to remove 
entities, relations, and attributes as well as references to them, like attribute ownerships. For example, to remove 
ownership of an attribute without deleting the attribute itself. Or, to remove the player of a role from a relation 
without deleting either the player or the relation/role.

### Syntax

Delete queries are written in TypeQL with the following syntax:

<!-- test-ignore -->
```typeql
match <pattern>
delete <pattern>
```

The `match` clause uses patterns to find existing data/references which may be removed. The `delete` clause uses a 
pattern to specify which data/references found by the `match` clause should be removed.

<div class="note">
[Note]
A pattern consists of variables and constraints for concepts. For more information see the 
[Pattern syntax](03-match.md#pattern-syntax) section.
</div>

The number of deleted concepts depends on the number of answers matched by `match` clause. `delete` clause will be 
executed once per every matched answer.

<div class="note">
[Important]
If there is no matches for a `match` clause in a `delete` query then there will be no deletes. 
</div>

<div class="note">
[Note]
The `delete` clause can have multiple patterns to delete in one query. But it can’t delete types (use 
[undefine](02-schema.md#undefine) to delete types) and can’t have the following:

- Conjunction
- Disjunction
- Negation
- `is` keyword

</div>

If multiple patterns are needed to delete data, run multiple queries in the same transaction.

### Entities

Use a match clause followed by the `delete` keyword and a pattern containing an `isa` expression to remove an entity 
from a database.

<!-- test-ignore -->
```typeql
match 
  $p isa person, has email "john.parkson@gmail.com"; 
delete 
  $p isa person;
```

In the above query, `match` clause finds a `person` entity (or entities) owning an `email` attribute with a value of 
`john.parkson@gmail.com`. Then, it removes the matched entities and all associated ownerships.

### Relations

#### Instances

Use a match clause followed by the `delete` keyword and a pattern containing an `isa` expression to remove a relation 
from a database.

<!-- test-ignore -->
```typeql
match
  $p isa subject, has full-name "Pearle Goodman";
  $a isa action, has name "modify_file";
  $ac (object: $o, action: $a) isa access; 
  $pe (subject: $p, access: $ac) isa permission;
delete 
  $pe isa permission;
```

The above query does the following:

1. Finds a `subject` entity ($p), with full-name attribute value of `Pearle Goodman`.
2. Finds an `action` entity ($a), with name attribute value of `modify_file`.
3. Finds `access` relations ($ac) relating any object (as object) to the action $a (as action).
4. Finds `permission` relations ($pe) relating the `subject` entity $p (as subject) to the `access` 
   relations $ac (as access).
5. Deletes all matched permissions $pe.

In short, it removes all of the permissions which let Pearle Goodman modify files.

#### Role players

Use a match clause followed by the `delete` keyword and a pattern to remove a player from a role in a relation.

<!--- #todo Double-check the example-->

<!-- test-ignore -->
```typeql
match
  $p isa subject, has full-name "Masako Holley"; 
  $o isa object, has path "zewhb.java"; 
  $oo (object-owner: $p, object-owned: $o) isa object-ownership; 
delete 
  $oo (object-owner: $p);
```

The above query, assuming the `full-name` attribute is unique for each `subject` entity, and the `path` attribute 
unique for each `object`:

1. Finds a `subject` entity ($p, Masako Holley)
2. Finds an `object` entity ($o, zewhb.java)
3. Finds an `object-owner` relation ($oo) relating $p (object-owner) to $o (object-owned).
4. Deletes $p as a player of the `object-owner` role in $oo

In short, it removes `Masako Holley` as an owner of the `zewhb.java` file. However, the relation itself stays and any 
other `subject` entities playing the `object-owner` role will continue to do so.

<div class="note">
[Note]
The `isa object-ownership` expression is omitted because we are not deleting the `object-ownership` relation itself, 
but rather a specific player of its `object-owner` role.
</div>

### Attributes

Attributes can be owned by entities, relations, and other attributes. A delete query can remove the attribute itself 
or remove the ownership of it (and leave the attribute).

Attributes are immutable. Rather than changing the value of an owned attribute, the ownership of it is replaced with 
the ownership of a new/different attribute.

#### Instances

Use a match clause followed by the `delete` keyword and a pattern containing an `isa` expression to remove an 
attribute from a database.

<!-- test-ignore -->
```typeql
match 
  $fn isa full-name; 
  $fn “Bob”; 
delete 
  $fn isa full-name;
```

The above example finds the `full-name` attribute whose value is `Bob`, and deletes it. As well as all ownerships of 
this attribute by any entities, relations, or other attributes.

#### Ownership

TypeDB allows multiple instances to share the same attribute, so it is more common to remove the ownership of an 
attribute rather than the attribute itself.

Use a match clause followed by the `delete` keyword and a pattern to remove the ownership of an attribute.

<!-- test-ignore -->
```typeql
match 
  $o isa object, has path $fp; 
  $fp like "(logs/.*)"; 
delete 
  $o has $fp;
```

The above query finds all `object` entities that has a `path` attribute whose value matches a regular expression 
(`logs/.*`). It then removes their ownership of any matching `path` attributes. However, the attributes 
themselves are not removed.

<div class="note">
[Important]
The `delete` clause can be altered a little to produce a very different result. Be aware of potential mistakes of 
deleting the wrong data accidentally. See the examples below.
</div>

The `isa object` expression in the query above is omitted because we are not deleting the `object` entities themselves, 
but rather their ownership of `path` attributes. 

For example, `delete $o isa object, has $fp;` clause with a `match` clause above deletes all matched objects `$o`. 
Thus, deletes all their ownerships over any attributes, not only `$fp`.

We do not include `path` into the `delete` clause as it's not needed for ownership deletion. The type of `$fp` should
be specified in the `match` clause if it's important. In this case it is specified as `path` already.

For example, `delete $o has path $fp;` clause with a `match` clause above produces an error.

Finally, we can delete the attributes themselves, thus deleting ownerships over any of them by all instances of all 
types.

For example, `delete $fp isa path;` clause with a `match` clause above deletes all matched `path` attributes, thus 
deleting all ownerships of these attributes from every owner of any type.

## Update

An update is actually a `match-delete-insert` query, and it removes and then adds data based on the `match`, `delete`, 
and `insert` patterns. 

Unlike other databases, TypeDB does not update data in place. Data is updated by 
replacing references to it. In relations, when a player is removed from a role, the player itself is not removed from 
the database. 

In addition, attributes are immutable. Rather than changing the value of an owned attribute, 
the ownership of it is replaced with the ownership of a new/different attribute.

### Syntax

Updates are written in TypeQL with the following syntax:

<!-- test-ignore -->
```typeql
match <pattern>
delete <pattern>
insert <pattern>
```

The `match` clause uses patterns to find existing data/references to be changed. The `delete` clause uses a pattern 
to specify which data/references found by the `match` clause should be removed. The `insert` clause uses a pattern 
to specify the data/references which will replace it.

<div class="note">
[Note]
A pattern consists of variables and constraints for concepts. For more information see the 
[Pattern syntax](03-match.md#pattern-syntax) section.
</div>

The number of deleted and inserted concepts depends on the number of answers matched by `match` clause. `delete` 
clause as well as `insert` clause will be executed once per every matched answer.

<div class="note">
[Important]
If there is no matches for a `match` clause in a update (`match-delete-insert`) query then there will be no deletes 
and no inserts. 
</div>

<div class="note">
[Note]
The `delete` clause can have multiple patterns to delete in one query. But it can’t delete types (use 
[undefine](02-schema.md#undefine) to delete types) and can’t have the following:

- Conjunction
- Disjunction
- Negation
- `is` keyword
- 
</div>

<div class="note">
[Note]
The `insert` clause can have multiple patterns to insert in one query. But it can’t insert types (use 
[define](02-schema.md#define) to insert new types) and can’t have the following:

- Conjunction
- Disjunction
- Negation
- `is` keyword
- 
</div> 

If multiple patterns are needed to update data, run multiple queries in the same transaction.

### Updating attribute values

#### Replacing ownership

In many cases, the desired effect is to change the value of an owned attribute. We can’t change the value of an 
attribute as attributes are immutable, but we can change the owned attribute. To update an attribute owned by an 
entity, its ownership must first be removed. Then, the entity can be assigned ownership of an attribute with a 
different value. It can be an existing attribute or a new one.

<!-- test-ignore -->
```typeql
match 
  $p isa person, has full-name "Masako Holley", has email $email; 
delete 
  $p has $email;
insert 
  $p has email "m.holley@vaticle.com";
```

The above query, does the following:

1. Finds all `person` entities (`$p`) that have a `full-name` attribute with a value of `Masako Holley`.
2. Deletes `$p`’s ownership of its current `email` attribute.
3. Makes `$p` the owner of an `email` attribute with a value of `m.holley@vaticle.com`.

If there is an existing `email` attribute with a value of `m.holley@vaticle.com`, the matching `person` entities will 
now own it. Otherwise, a new one will be created and owned by the matching `person` entities.

<div class="note">
[Note]
An `email` attribute with the previous value of `masako.holley@vaticle.com` will still exist, but it will no longer 
be owned by the matching `person` entities.
</div> 

#### Replacing attributes

There may be times when the desired effect is to change the value of multiple owned attributes, all of the same type. 
This is done by removing them, inserting the ownership of a new/different attribute.

<!-- test-ignore -->
```typeql
match
  $p isa person, has full-name $n;
  $n contains "inappropriate word";
delete 
  $n isa full-name;
insert 
  $p has full-name "deleted";
```

The above query:

1. Finds all `person` entities (`$p`) with at least one owned `full-name` attribute (`$n`).
2. Filters `$n` (and consequently `$p`) to only those that contain the string `inappropriate word`.
3. Removes these `full-name` attributes that contain the string from the database. 
4. Makes `$p` (all entities of person that had `full-names` that contained the string) the owners of a `full-name` 
   attribute with a value of `deleted`.

If a similar query has been run before, there may be an existing attribute with a value of `deleted` which the matching 
`person` entities will now own. If not, a new `full-name` attribute will be inserted and the matching `person` entities 
will own it.

<div class="note">
[Note]
After running the above query, there will be a single full-name` attribute with a value of `deleted` which is owned by 
the matching entities, and any `full-name` attributes which had contained the string `inappropriate word` will no longer 
exist.
</div> 

#### Updating a relation’s role player

To replace a role player, we combine the steps for extending the relation, with steps for deleting a role player:

<!-- test-ignore -->
```typeql
match
  $p isa person, has full-name "Pearle Goodman";
  $a_write isa action, has name "modify_file";
  $a_read isa action, has name "view_file";
  $ac_write (object: $o, action: $a_write) isa access; 
  $ac_read (object: $o, action: $a_read) isa access; 
  $pe (subject: $p, access: $ac_write) isa permission;
delete 
  $pe (access: $ac_write);
insert 
  $pe (access: $ac_read);
```

The above query does the following: 

1. Finds a `person` entity (`$p`) with a `full-name` of `Pearle Goodman`.
2. Finds an `action` entity (`$a_write`) with `name` of `modify_file`).
3. Finds an `action` entity (`$a_read`)  with `name` of `read_file`).
4. Finds all `access` relations (`$ac_write`) that relate any `object` (as `object`) to `$a_write` (as `action`).
5. Finds all `access` relations (`$ac_read`) that relate any `object` (as `object`) to `$a_read` (as `action`).
6. Finds all permissions (`$pe`) that relate `$p` (as `subject`) to `$ac_write` (as `access`).
7. Removes all write accesses (`$ac_write`) as a player of the `access` role in matching permission relations
   (`$pe`).
8. Adds all read accesses (`$ac_read`) as a player of the `access` role in matching permission relations (`$pe`).

In short, all of Pearle Goodman’s permissions with write access will become permissions with read access.

<div class="note">
[Note]
After running the above query, all of the matched `access` relations `$ac_write` with `$a_write` as `action` 
still exist, but no longer play a role in the matched `permission` relations.
</div> 
