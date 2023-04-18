---
pageTitle: Schema
keywords: typeql, schema, type hierarchy, reserved keywords
longTailKeywords: typeql schema, typeql type hierarchy, typeql data model, typeql reserved keyword
Summary: Introduction to the TypeDB Schema.
---

# Schema

TypeDB schema is like a blueprint of a database.

TypeDB schema defines all user-defined types and rules used in a database.

All user-defined types must subtype the entity, relation, or attribute base type or another user-defined type.

As a result, TypeDB schemas look like ER diagrams. They resemble logical data models,
removing the need to create a separate physical data model and allowing developers to
create schemas that mirror their object model simplifying both design and development.

![Types hierarchy](../../images/schema/thing-era-role-rule.png)

TypeDB schemas are written with TypeQL which is both Data Definition Language and Data Manipulation Language (used 
for schema and data queries). You can see a complete set of TypeQL syntax and grammar rules in ANTLR v.4 specification 
file: [TypeQL.g4](https://github.com/vaticle/typeql/blob/master/grammar/TypeQL.g4).

## Types

Types define the data model, its constraints, and the relationships within it. In addition, the types within a schema 
reflect the vocabulary used to describe the business domain it represents.

Creating a type means subtyping a base type or a user-defined type. The base types are:

|      Type      |              Instance of Type               |
|:--------------:|:-------------------------------------------:|
|  Entity type   |    Entity <br/>(Instance of Entity type)    |
| Relation type  |  Relation <br/>(Instance of Relation type)  |
| Attribute type | Attribute <br/>(Instance of Attribute type) |

There is a strict hierarchy of types with all types being descendants (children, grandchildren, great-grandchildren, 
etc.) of one of the base types. Every type can have only one parent. There is also an internal type `role` that is 
used in relations. Instances of types (i.e., the data) are known as `entities`, `relations`, and `attributes`, 
depending on which branch of types they are belong to.

### Thing type

There is a base type called `thing` type that can be used to address all types (both base and user-defined).

<div class="note">
[Warning]
The `thing` base type will be deprecated in TypeDB version 3.0.
</div>

### Entity types

Entity types define objects within our business domain (e.g., an organization, file, or user). 

An instance of entity type (e.g., instance of `company` type) can exist independently of any 
other instance of any type (e.g., a different instance of `company` type, an instance of `person` type).

<div class="note">
[Note]
In comparison — a relation is meaningless without its role players, and
an attribute is meaningless without being owned by any other instance.
</div>

### Relation types

Relation types represent the relationships of other types in business domain model and define roles participants 
can **play** in a relations. 

Participants (or role players) can be `entities`, `relations`, or `attributes`. A `relation` type must specify at least 
one role. For example, `group-membership` is a `relation` type that defines `user-group` and `group-member` roles. 
The `user-group` role is to be played by a `user-group` entity whereas the `group-member` role is to be played by 
a `subject` type and all its subtypes entities.

Roles allow a schema to enforce logical constraints on types of role players. For example, a 
`group-membership` relation cannot associate a `user` type entity with a `file` type entity.

<div class="note">
[Note]
Roles can be queried like any other types even though roles do not have a direct type definition. Only as a part of 
some relation.
</div>

### Attribute types

Attribute types represent the properties of other types with a value. Mostly `entity` and `relation` types (e.g., 
the name of a business unit or a user). In TypeDB, any type can **own** an attribute type. However, different types 
can own the same attribute type — and different instances can share ownership of the same attribute instance.

For example, multiple users can own the same instance of an attribute type with the value of `Alex`.

<div class="note">
[Warning]
The feature of attribute type owning another attribute types will be deprecated in TypeDB version 3.0.
</div>

### Inheritance

A type can subtype another type. As a result, the subtype inherits all the attributes owned and roles played by its 
supertype. However, while a type can only have a single supertype, types can be subtypes of other subtypes, 
resulting in a type hierarchy. For example, `business unit` subtypes `user group`, which subtypes `subject`, 
which subtypes `entity` base type.

<div class="note">
[Note]
While roles are not generally considered to be types, they can be inherited and even overriden as a part of relation 
inheritance.
</div>

## Rules

Reasoning engine uses rules as a set of logic to infer new data. A rule consists of a condition and a conclusion. 
Condition is a pattern to look for in data and conclusion is data to be virtually inserted for every result matched 
with a pattern from condition. Rules are used by read queries for 
[Inferring new data](06-infer.md).

<div class="note">
[Important]
Rules can’t change persisted data in a database. Instead, all the reasoning is done within a dataset of a query. 
Only the result of queries is influenced by the inference. During a single transaction, newly inferred facts will be 
retained and reused (with corresponding performance gains). New transactions will re-compute inferred facts again.
</div>

The rules syntax uses `when` and `then` keywords as in `if`/`then` statement that produce virtual relations or 
attributes when the conditions are met. Read more on how to create rules in a schema in the
[Define rules](#define-rules) section. See the example of rules syntax below.

<!-- test-ignore -->
```typeql
define

rule rule-label:
when {
    ## the conditions
} then {
    ## the conclusion
};
```

<div class="note">
[Important]
Inference can only be used in a read transaction. Learn how to use inference on the [Inferring data](06-infer.md) page.
</div>

<div class="note">
[Note]
The approach TypeDB uses is a [backward-chaining](https://en.wikipedia.org/wiki/Backward_chaining) execution on top 
of [Horn-clause](https://en.wikipedia.org/wiki/Horn_clause) logic. 

Negation functionality follows the set-difference semantics. It corresponds to negation-as-failure model under the 
following conditions:

- we have stratified negation,
- the results are grounded,
- we ensure all variables occurring both inside and outside the negation are bound by the time the negation is 
  evaluated.

Infinite recursion and non-termination are prevented with a tabling mechanism.
</div>

## Define schema

TypeQL statements must begin with the `define` keyword in order to modify a schema (e.g., create **types** or 
**rules**). 

In order to use a new TypeDB database we need to define its schema first. Use TypeDB `define` queries in a `schema` 
session with `write` transaction to do so. The TypeQL statements of these queries must begin with the `define` 
keyword in order to define a schema (create types or rules). 

However, when running multiple statements within a TQL file, the `define` keyword only has to be included 
once at the very beginning.

<div class="note">
[Important]
In order to define a schema, a `schema` [session](01-connections.md#sessions) must be opened and a `write` 
[transaction](01-connections.md#transactions) started. The changes must be **committed** or they will NOT be permanent.
</div>

There is no limitation in the order of types to define. You can define schema types in any order as long as 
the schema as a whole is valid. TypeDB Clients validate your schema definition requests before sending them to a TypeDB 
server. You will not be able to commit changes if the schema definition query isn’t valid.

### Create a new database

The examples below can and should be run in a separate empty database. It is recommended to create a new database 
and to run the examples in the order they are shown. For more information on creating an empty database, see the 
[Quickstart guide](../01-start/03-quickstart.md#create-a-database).

<div class="note">
[Important]
Define queries are idempotent. Running the same define query a second time shall not produce any changes to the 
database schema. Running a modified version of an already executed schema definition query can add concepts to the 
schema but mostly can’t modify existing ones. TypeQL schema statements do NOT replace existing type definitions 
but rather add the missing parts.

Two notable exceptions are: **rules** (defining a new rule with existing label/name will replace the existing rule) and 
**annotations**, like the `@key` keyword (can be added or removed).
</div>

### Query example

The following example defines a part of the [IAM schema](../01-start/04-iam-schema.md) that will be used throughout 
the rest of the documentation. However, some queries result in modification of the original IAM schema used in the 
Quickstart guide. These occasional modifications are needed to demonstrate what TypeQL is capable of.

<!-- test-ignore -->
```typeql
define

credential sub attribute, value string;
full-name sub attribute, value string;
id sub attribute, abstract, value string;
email sub id, value string;
membership sub relation, abstract, relates parent, relates member;
group-membership sub membership, relates parent-group as parent, relates group-member as member;
subject sub entity, abstract, owns credential, plays group-membership:group-member;
user sub subject, abstract;
person sub user, owns full-name, owns email;
```

The above example can be run in [TypeDB Studio](../../02-clients/01-studio.md). See the 
[Quickstart guide](../01-start/03-quickstart.md) for full descriptions of the following steps:

1. Make sure TypeDB server is up.
2. Start TypeDB Studio.
3. Connect TypeDB Studio to the server.
4. Create or select a new database.
5. Open a Project folder.
6. Copy and paste the query code above into a new tab of the Text-editor.
7. Ensure the [**Session type**] switch is set to “**Schema**”.
8. Ensure the [**Transaction type**] switch is set to “**Write**”.
9. Click the green “play” button to start the transaction.
10. Click the “checkmark” button to commit the changes.

After a successful commit, all the types can be seen in the Types panel in the bottom left part of the Studio window. 
In addition, the following query can be run in a new tab in **Schema** / **Read** mode to see the schema visualized 
as a graph (as shown below).

<!-- test-ignore -->
```typeql
match $s sub thing;
```

![Example 1](../../images/schema/example-1.png)

<div class="note">
[Warning]
The `thing` base type will be deprecated in TypeDB version 3.0. 
To produce the same result as the above example, use the following query:

<!-- test-ignore -->
```typeql
match $s sub $t; { $t type entity; } or { $t type relation; } or { $t type attribute; };
```
</div>

In the following sections, you can find more detailed information on different schema definition queries and 
possibilities.

### Define entity types

#### Overview

Entity types are defined independently of other types, but may subtype other entity types.

Optionally, entity types can:

* be abstract.
* own attribute types.
* play roles defined in relation types.

#### Syntax

Entity types are defined in TypeQL with the following pattern:

<!-- test-ignore -->
```typeql
<label> sub (entity | <entity type label>) [(, abstract)]
[(, owns <attribute type label)...]
[(, plays <relation type label>:<role>)...];
```

#### Examples

##### Basic

The following `define` query creates a new entity type, `object`, by subtyping the `entity` base type.

<!-- test-ignore -->
```typeql
define object sub entity;
```

##### Abstract

Optionally, entity types can be defined as `abstract`. An abstract entity type can’t be instantiated and must be 
subtyped in order to create entities. It exists only so other entity types can inherit the attribute types it owns 
and the roles it plays.

<!-- test-ignore -->
```typeql
define object sub entity, abstract;
```

##### Owns an attribute

To define a new entity type that owns one or more attribute types, use the `owns` keyword followed by the label of the 
attribute type. The attribute types are appended to the entity type definition with commas. Note, attribute types must 
be defined before or concurrently (in the same transaction) with its owner(s). We can add owners later, but we can't 
own non-existent attribute type.

<!-- test-ignore -->
```typeql
define

object-type sub attribute, value string;
object sub entity, abstract, owns object-type;
```

###### Cardinality

By default, an entity can have multiple attributes of the same type: zero, one, or many.

By having multiple attributes of the same type we're effectively creating a 
[multivalued attribute](04-write.md#multivalued-attributes) (i.e. having an attribute type instantiated with multiple 
values).

Use the `@key` keyword to limit the cardinality to exactly **one** and add **uniqueness** constraint. 
See example in [Key attribute](#define-attribute-types) section.

##### Plays a role

To add roles that entities of a specific entity type can play, use the `plays` keyword.

<!-- test-ignore -->
```typeql
define

access sub relation, relates accessed-object;
object sub entity, abstract, plays access:accessed-object;
```

##### Subtypes another entity

<div class="note">
[Note]
All types that are subtyping `entity` base type directly or through other subtypes are called entity types. 
Instances of these types are called entities. The same approach can be applied to attributes and relations.
</div>

An entity type can subtype another entity type by using the same `sub` keyword, but replacing the `entity` keyword 
after it with a label of another entity type to subtype.

<!-- test-ignore -->
```typeql
define

path sub attribute, value string;

object sub entity, abstract, owns object-type, plays access:accessed-object;
resource sub object, abstract;
file sub resource, owns path;
```

In the above example, the `resource` and `file` entity types are subtypes of the `object`, which itself is a subtype 
of the `entity` base type. They inherit the `object-type` attribute type ownership from it as well as its 
`access:accessed-object` role. However, while the `resource` subtype is abstract, the `file` subtype is not. Hence, we 
can create `file` entities, but not `resource` entities.

Further, the `path` attribute type will only be owned by the `file` entity type and any other entity types which 
subtype it or directly define ownership.

##### Overrides inherited attribute ownership

To override an inherited ownership use `owns` keyword with the new attribute type label, followed by the `as` keyword 
and the inherited attribute type label. For example:

<!-- test-ignore -->
```typeql
define file sub resource, owns file-type as object-type;
```

The new attribute type that overrides inherited type is defined in the schema as subtype of the inherited 
attribute type. Hence, the inherited attribute type is abstract and has the same value type as the new attribute type.
The example above in a schema would look like that:

<!-- test-ignore -->
```typeql
define

path sub attribute, value string;

object-type sub attribute, abstract, value string;
file-type sub object-type, value string;

object sub entity, abstract, owns object-type;
resource sub object, abstract;
file sub resource, owns path, owns file-type as object-type;
```

In the above example, the `file` entity type owns the `path` and `file-type` attribute types, with the `file-type` 
attribute type overriding the inherited `object-type` attribute type.

### Define attribute types

#### Overview

Attribute types are defined independently of other types, but may subtype a user-defined abstract attribute type. 
Any type can have an ownership over any attribute type.

<div class="note">
[Warning]
Attributes owning attributes feature will be deprecated in TypeDB version 3.0.
</div>

<div class="note">
[Warning]
Attributes playing role in a relation feature will be deprecated in TypeDB version 3.0.
</div>

Optionally, attribute types can:

* be abstract.
* own other attribute types (this will be deprecated).
* play roles in relations (this will be deprecated).

#### Syntax

Attribute types are defined in TypeQL with the following pattern:

<!-- test-ignore -->
```typeql
<label> sub (attribute | <abstract attribute type label>) [(, abstract)], value <value type> [, regex "<expression>"]

[(, owns <attribute type label)...]

[(, plays <relation type label>:<role>)...];
```

The following **value types** are supported:

* `long` – a 64-bit signed integer.
* `double` – a double-precision floating point number, including a decimal point.
* `string` – enclosed in double " or single ' quotes
* `boolean` – true or false
* `datetime` – a date or date-time in the following formats:
    * `yyyy-mm-dd`
    * `yyyy-mm-ddThh:mm`
    * `yyyy-mm-ddThh:mm:ss`
    * `yyyy-mm-ddThh:mm:ss.f`
    * `yyyy-mm-ddThh:mm:ss.ff`
    * `yyyy-mm-ddThh:mm:ss.fff`

#### Examples

##### Basic

<!-- test-ignore -->
```typeql
define

name sub attribute, value string;
email sub attribute, value string;
ownership-type sub attribute, value string;
review-date sub attribute, value datetime;
validity sub attribute, value boolean;
```

##### Subtypes another attribute type

An attribute type can subtype another attribute type if its **abstract**. This is useful when the possible values of 
an attribute type can be categorized, and applications can benefit from querying entities and relations not only by 
a value of an attribute but also by a label of attribute type.

<div class="note">
[Important]
An attribute type can only subtype an abstract attribute type. However, the subtype of an attribute type can itself be 
abstract. Further, an attribute subtype must have the same **value type** as its parent attribute type. Note, the 
**value type** of an attribute subtype can be omitted in its definition. It will be inherited from its parent attribute 
type.
</div>

<!-- test-ignore -->
```typeql
define

id sub attribute, abstract, value string;
email sub id, value string;
name sub id, value string;
path sub id, value string;
number sub id, value string;
```

The above example creates an attribute type, `id`. However, because different entities can be identified by different 
information, the `id` type is subtyped by `email`, `name`, `path`, and `number` types – making it possible to query 
users by `email`, business-units by `name`, files by `path` and records by `number`.

##### Key attribute

Optionally, to ensure that owned attributes value is unique among instances of the same type, use the `@key` keyword 
at the end of the ownership definition. This prevents two instances of the same type from owning the same attribute 
instance (with the same value).

Additionally, that limits cardinality of the attribute ownership to exactly **one**. Hence, the instance of the type 
with key ownership will have exactly one (no more and no less) key attribute instance.

<!-- test-ignore -->
```typeql
define

object-type sub attribute, value string;
object sub entity, abstract, owns object-type @key;
```

##### Regular expressions

The values of an attribute type can be restricted using Java regular expressions. For example, to constrain it to a 
set of options.

<!-- test-ignore -->
```typeql
define visibility sub attribute, value string, regex "^(public|private|closed)$";
```

The above example defines an attribute type: `visibility`. It is intended for user groups, and specifies a regex to 
restrict its values to `public`, `private` and `closed`.

##### Owns other attribute types

While it is more common for entity and relation types to own attributes, attribute types can also own (other) 
attribute types.

<div class="note">
[Warning]
Attributes owning attributes feature will be deprecated in TypeDB version 3.0.
</div>

<!-- test-ignore -->
```typeql
define

symlink sub attribute, value string;
filepath sub attribute, value string, owns symlink;
```

The above example creates an attribute type `filepath`, intended for files. It is assumed there can be multiple copies 
of a `file`, each with its own `filepath` — and symlinks can be created that point to these filepaths. Thus, the 
`filepath` attribute type (and NOT the `file` entity type) owns the `symlink` attribute type.

##### Plays a role

While it is more common for the roles in relations to be played by entities or other relations, they can also be played 
by attributes.

<!-- test-ignore -->
```typeql
define credential sub attribute, value string, plays change-request:requested-change;
```

The above example creates the `credential` attribute type, and specifies it can play the role of `requested-change` in 
the `change-request` relation type. While `change-requests` were intended to manage access changes, they can now be 
used to manage `credential` changes as well.

### Define relation types

#### Overview

Relation types are defined independently of other types but may subtype other relation types. Their definition can 
include ownership of attribute types, roles other types play within them, and roles they can play in other relation 
types:

* Owned attribute types are added with the `owns` keyword followed by the attribute type label.
* Its own roles are added with the `relates` keyword followed by the role label. At least one role must be defined for 
  any relation.
* Roles it can play in other relations are added with the `plays` keyword followed by the relation type label and role.

#### Syntax

Relation types are defined in TypeQL with the following pattern:

<!-- test-ignore -->
```typeql
<label> sub (relation | <relation type label>) [(, abstract)]
[(, owns <attribute type label)...]
(, relates <role label>)
[(, relates <role label>)...]
[(, plays <relation type label>:<role>)...];
```

#### Examples

##### Basic

The following statement creates an `access` relation that defines two roles:

* `accessed-object` – played by instances of the `object` entity type or its subtypes (e.g. `file`).
* `valid-action` – played by instances of the `action` entity type.

<!-- test-ignore -->
```typeql
define access sub relation, relates accessed-object, relates valid-action;
```

##### Plays a role

In addition to defining its own roles played by other types, a relation type can play roles in other relation types.

<!-- test-ignore -->
```typeql
define

access sub relation,
relates accessed-object, relates valid-action, 
plays permission:permitted-access, plays change-request:requested-change;
```

In the above example, `access` relation type can play the `permitted-access` role in `permission` relation type and 
the `requested-change` role in `change-request` relation type. Besides, an `access` relation type relates an 
`accessed-object` role (e.g., file) and a `valid-action` role (e.g., read). Thus a `permission` relation type relates 
the `access` (i.e., read + file) and a `subject` (e.g., `person` with `full-name` attribute `Kevin Morrison`).

##### Defines multiple roles

A relation can define multiple roles (from one to many).

<!-- test-ignore -->
```typeql
define

change-request sub relation, 
relates requested-change, 
relates requested-subject, 
relates requesting-subject;
```

##### Owns an attribute

A relation type can own zero, one or many attribute types.

<!-- test-ignore -->
```typeql
define

segregation-policy sub relation, 
relates segregated-action, 
plays segregation-violation:violated-policy, 
owns policy-name;
```

##### Abstract

Optionally, relation types can be defined as `abstract` so they must be subtyped in order to create relations. An 
abstract relation type exists only so other relation types can inherit the attribute types it owns and the roles it 
defines and/or plays.

<!-- test-ignore -->
```typeql
define

violation sub relation, abstract,
owns name;
```

##### Subtypes another relation

A relation type can subtype another relation type by replacing the `relation` keyword with the label of another 
relation type. Subtype will inherit all owned attribute types and all roles related or played by the parent type.

<!-- test-ignore -->
```typeql
define

membership sub relation, relates parent, relates member;
collection-membership sub membership;
```

In the example above, the `collection-membership` relation type inherits the `parent` and `member` roles defined in 
its parent type: `membership`.

The labels of the inherited roles can be overridden to distinguish between the roles inherited by a relation subtype 
vs. the roles defined by its parent type.

<!-- test-ignore -->
```typeql
define

membership sub relation, relates parent, relates member;

collection-membership sub membership, relates collection as parent;
```

In the example above, the `collection-membership` relation type subtypes the `membership` relation type, and overrides 
the inherited `parent` role as `collection`. The inherited `member` role inherited as it is.

<div class="note">
[Note]
The two examples above can be run back to back. The second one will update the `collection-membership` type to 
override one of its inherited roles.
</div>

##### Complex example

<!-- test-ignore -->
```typeql
define

ownership sub relation,
    relates owned,
    relates owner;

group-ownership sub ownership,
    relates group as owned,
    owns ownership-type;

object-ownership sub ownership,
    relates object as owned,
    owns ownership-type;

access sub relation,
    relates object,
    relates action,
    plays change-request:change;

change-request sub relation,
    relates requester,
    relates requestee,
    relates change;
```

The example above defines one attribute type and five relation types:

* `ownership` — subtypes the `relation` base type, and relates `owned`, and `owner` roles.
* `group-ownership` — subtypes `ownership` relation type, relates `group` as `owned`, and `owner` (inherited).
* `object-ownership` — subtypes `ownership` relation, relates `object` as `owned`, and `owner` (inherited).
* `access` — subtypes the `relation` base type, relates `object` (e.g., file) and `action` (e.g., 
  read), plays the role of `change` in `change-request` relation type.
* `change-request` — subtypes the `relation` base type, relates `requester`, `requestee` and
  `change`.

### Define rules

#### Overview

Rules are defined independently of any types. Any types used in a rule must be defined in a schema.

They are executed only as a part of get queries when the [inference](06-infer.md) option is **enabled**. The results of 
rules execution exist only within the transaction they run in. They are not persisted, and any data inferred in the 
transaction ceases to exist when the transaction is closed. Read more on rules in the [Rules](#rules) section.

#### Syntax

Rules are defined in TypeQL with the following syntax:

<!-- test-ignore -->
```typeql
rule <label>:
when {
    <pattern>  [(<pattern>)...]
} then {
    <pattern>
};
```

The `rule`, `when`, and `then` keywords are specific to rule definitions.

<div class="note">
[Important]
Unlike other `define` statements for schema definitions, the rule syntax uses patterns consisting of variables and 
constraints for **data** instances. For more information see the [Pattern syntax](03-match.md#pattern-syntax) section.
</div>

#### Rule Validation

The `when` clause (conclusion) of a rule can be a multi statement pattern and can include disjunctions and negations, 
whereas the `then` clause (condition) should describe a single relation or constraint of ownership of an attribute 
(due to [Horn-clause logic](https://en.wikipedia.org/wiki/Horn_clause)).

When using a disjunction in a rule, the disjunctive parts must be bound by variables outside of the `or` statement. 
These variables are the only ones permitted that can be used in the `then` clause.

The `then` clause of a rule can’t use variables that aren’t defined in the `when` clause.

The `then` clause of a rule must not insert any instance which occurs negated in its `when` clause , or in the `when` 
clause of any rule it may trigger. Attempting to define such a rule will throw an error.

Rules will not create duplicates of instances which are already in the database or have already been inferred. 
There is no need to check if it already exists in a rule.

There are exactly **three** distinct **conclusions** permitted:

1. A new relation.
2. Ownership of an attribute defined by its value.
3. Ownership of an attribute defined by a variable.

The `then` clause must be insertable according to the schema (e.g. you cannot give an attribute to an instance that is 
not allowed to own that attribute type).

#### Examples

##### Basic

<!-- test-ignore -->
```typeql
define 

rule test:
    when {
        $p isa person;
    } then {
        $p has full-name "Dude";
    };
```

The example above demonstrates a simple rule. All `person` entities matched by a read query with the inference option 
**enabled** will have a `full-name` attribute with the value `Dude`, even if they have an existing `full-name` 
attributes with different values.

##### Transitive rule

<!-- test-ignore -->
```typeql
define 

rule transitive-reachability:
    when {
        (from: $x, to: $y) isa rel;
        (from: $y, to: $z) isa rel;
    } then {
        (from: $x, to: $z) isa rel;
    };
```

The example above allows for the transitivity of relations. We can interpret this rule as joining two relations 
together. It creates a relation `x` to `z`, given that there are relations of `x` to `y` and `y` to `z`.

##### Advanced transitivity usage

When inferring relations, it is possible to variabilize any part of the `then` clause of the rule. For example, if we 
want a rule to infer many types of relations, we could propose a rule such as:

<!-- test-ignore -->
```typeql
define 

rule all-relation-types-are-transitive:
    when {
        ($role1: $x, $role2: $y) isa! $relation;
        ($role1: $y, $role2: $z) isa! $relation;
    } then {
        ($role1: $x, $role2: $z) isa $relation;
    };
```

##### Complex rule

<!-- test-ignore -->
```typeql
define 

rule add-view-permission:
    when {
        $modify isa action, has action-name "modify_file";
        $view isa action, has action-name "view_file";
        $ac_modify (accessed-object: $obj, valid-action: $modify) isa access;
        $ac_view (accessed-object: $obj, valid-action: $view) isa access;
        (permitted-subject: $subj, permitted-access: $ac_modify) isa permission;
    } then {
        (permitted-subject: $subj, permitted-access: $ac_view) isa permission;
    };
```

The example above illustrates a more complex rule, using the IAM schema.

In short, the permission to access some file with action that has `action-name` of `view_file` can be inferred by the 
rule from the permission to `modify_file` the same file.

A full explanation of how this rule works is given in the [Example](06-infer.md#example) section of Inferring data page.

## Modify existing schema

### Add types and rules

You can add types and rules to an existing schema by running the same [define](#define-schema) statement as usual.

The define statements are idempotent. By sending the same define query twice or more times the very same resulting 
schema must be achieved as if we send it only once. So types and/or rules will not be duplicated.

A separate define statement for a new type or rule can be sent as a define query. Alternatively, the statement can be 
added to the existing schema define statement and sent together. In this case only new types or rules will be added. 
If you change name (label) of the existing type or rule in the existing schema and then send it as define query then 
the changed type or rule will be processed as a new one.

### Renaming types

To rename (change its label) a type use the [TypeDB Studio](../../02-clients/01-studio.md) or 
[TypeDB API](08-api.md) Rename method for a Type class object.

### Deleting types & rules

Use the `undefine` keyword to remove the definition of a type or its association with other types from the schema.

<div class="note">
[Important]
Don't forget to `commit` after executing an `undefine` statement. Otherwise, any changes is NOT committed to a database.
</div>

#### Undefine a type

To delete a user-defined type from a schema use the keyword `undefine` with the label of a type to delete and `sub` 
keyword, followed by the supertype (direct or not) of the deleted type.

<!-- test-ignore -->
```typeql
undefine subject sub entity;
```

<div class="note">
[Warning]
Types with existing subtypes or instances can’t be undefined. Undefine any subtypes and delete any data instances 
of a type to be able to undefine it.
</div>

#### Undefine an attribute's association

We can undefine the association that a type has with an attribute.

<!-- test-ignore -->
```typeql
undefine subject owns credential;
```

The query above removes ownership of the attribute type `object-type` from the entity type `object`. So that instances 
of `object` type will not have an ability to have ownership over instances of `object-type` anymore.

<div class="note">
[Important]
It's important to note that if we add the `sub` keyword to the `label` at the beginning: 
`undefine [label] sub [type], owns [attributes' label];` it undefines the `label` type itself, 
rather than just its association with the attribute type.

For example, `undefine subject sub entity, owns credential;` will delete the `subject` entity type from the schema. 
The ownership of the `credential` attribute type by the `subject` entity type will also be removed, but the 
`credential` attribute type will continue to exist. To undefine it from a schema use 
`undefine credential sub attribute;`.
</div>

#### Undefine a relation

Undefining a relation type inherently undefines all of its roles. Therefore, when a relation type is undefined any types 
that were playing roles in that relation type will no longer play those roles. Given a `change-request` relation type 
we can undefine it as shown below.

<!-- test-ignore -->
```typeql
undefine

change-request sub relation;
```

#### Undefine a supertype

When a type to be undefined is a supertype to something else, we must first undefine all its subtypes before 
undefining the supertype itself. You can use the same transaction to delete both the supertype and all its subtypes.

<!-- test-ignore -->
```typeql
undefine

object sub entity;
resource sub object;
```

#### Undefine a rule

Rules like any other schema members can be undefined. Consequently, to delete a rule use the `undefine rule` keywords 
and refer to the rule by its label. For example:

<!-- test-ignore -->
```typeql
undefine rule add-view-permission;
```
