---
pageTitle: Inferring data
keywords: typedb, query, inference, reasoning, rules, deduction, logic
longTailKeywords: typedb inference, typedb reasoning, reasoning engine
Summary: TypeDB inference queries.
---

# Inferring data

## Rules

TypeDB is capable of reasoning over data via rules [defined](02-schema.md#define-rules) in the schema. They can be used 
to infer new data, based on the existence of patterns in data of a TypeDB database. Rules can dramatically shorten 
complex queries, perform explainable knowledge discovery, and implement business logic at the database level.

## Inference

<div class="note">
[Important]
Reasoning, or inference, is performed at a query time in a `read` transaction. The results are transaction-bound and 
are not persisted.
</div>

<!-- #todo Double-check and possibly rewrite the next part--->

When executing a `get` query with infer transaction option [enabled](#how-to-use-inference) (`True`), the TypeDB 
server inspects and triggers rules that may lead to new answers to the query and then performs the query execution 
to return data that answers the query taking into account inference results. This approach is known as 
[backward-chaining](https://en.wikipedia.org/wiki/Backward_chaining) (starting from the query, then finding applicable 
rules and generating new relevant data). Reasoning can proceed from one rule to other rules, including recursively, 
leading to complex behaviors emerging from a few simple rules.

## Limitations

Inference works by rules defined in a schema of a database. Hence, what possible to infer is limited by what can be 
defined in a rule. See the [rule validation](02-schema.md#rule-validation) section for more information on what can 
and can’t be defined in a rule.

<div class="note">
[Important]
Only `read` transactions can enable inferences from rules.
</div>

Inferred facts are transaction-bound: during a single transaction, newly inferred data will be retained and reused 
(with corresponding performance gains). As soon as the transaction is closed all the inferred data is lost. New 
transactions will not be able to reuse previously inferred data and their queries will re-compute inferred facts 
again.

## Inference optimization

These are general tips for making queries with reasoning execute faster:


1. Adding a limit to the query. Without a limit, the reasoning engine is forced to explore all possible ways to answer 
   the query exhaustively. If you only need 1 answer, adding `limit 1;` to the match query can significantly improve 
   query times.
2. Using the same transaction for multiple reasoning queries. Because inferred data is cleared between transactions, 
   running the same or similar queries within one transaction can reuse previously inferred data. Combined with a limit 
   on the query, it might be possible to avoid having to do any new reasoning at all.
3. For complex queries, it can also be beneficial to add more CPU cores, as the reasoning engine is able to explore 
   more paths in the database concurrently.

## How to use inference

Inference is enabled as a read transaction option.

### TypeDB Studio

To send a request with inference enabled in [TypeDB Studio](#client/studio) follow these steps:

1. Ensure the [**Session type**] (schema / data) switch is set to “**data**” (next to the database dropdown).
2. Ensure the [**Transaction type**] (write / read) switch is set to “**read**”.
3. Ensure the [**infer**] button (next to the transaction type switch) is pushed (shown in **green** text).
4. Click the `+` icon at the top of the **Text-editor** panel.
5. Copy the TypeQL query into the **Text-editor** panel.
6. Click the green “play” button.

### TypeDB Console

Set the `infer` option to `true` when you start the read transaction. For example:

<!-- test-ignore -->
```
transaction typedb data read --infer true
```

### TypeDB Drivers

Set the `infer` option to `True` when you start the read transaction. For example:

<!-- #todo Consider adding other languages--->

<!-- test-ignore -->
```python
typedb_options = TypeDBOptions.core()  # Initialising a new set of options
typedb_options.infer = True  # Enabling inference in this new set of options
with session.transaction(TransactionType.READ, typedb_options) as transaction:
```

## Example

In the IAM database there are multiple rules, but we will use the one described at the 
[IAM schema explanation](../01-start/04-iam-schema.md) page. 

<!-- test-ignore -->
```typeql
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

By default, the IAM dataset used in the [Quickstart guide](../01-start/03-quickstart.md) sets permissions only for the 
`modify_file` action. 

But the IAM schema has the rule called `add-view-permission` (see above) to infer permission to `view_file` access 
from the `modify_file` permission for the same file. The `view_file` action access permission does not exist in the 
database, but it can be inferred by the rule.

To do so, let’s use the following query:

<!-- test-ignore -->
```typeql
match
    $p isa person, has full-name "Kevin Morrison";
    $o isa object, has path $o-path;
    $a isa action, has action-name "view_file";
    $ac(accessed-object: $o, valid-action: $a) isa access;
    $pe(permitted-subject: $p, permitted-access: $ac) isa permission;
get $o-path;
```

The above query should return `path` values for most files if the inference option is **enabled**. Without the 
inference enabled the query should not return any results (for the default IAM dataset contains no permissions for 
access with `view_file` action).

### Query explanation

The example is a `get` query with `match` clause and optional `get` clause that does the following:

1. Finds `person` entity (`$p`) with an attribute `full-name` equal to the `Kevin Morrison` string value.
2. Finds all `object` entities (`$o`) with a `path` attribute (`$o-path`).
3. Finds `action` entity (`$a`) with `action-name` of `view-file`.
4. Finds `access` relation (`$ac`) that relates `$o` (as `accessed-object`) to `$a` (as `valid-action`).
5. Finds all `permission` relations that relate `$p` (as `permitted-subject`) to `$ac` (as `permitted-access`).
6. Filters the results to receive only the `$o-path` variable that complies with all the statements above.

In short, it returns `path` attributes for every `object` that `person` with a `full-name` of `Kevin Morrison` has 
permission to access with `action` with the `action-name` of `view_file`. 

## Explain query

There is specific type of query to use with the inferred results if we want them explained by a TypeDB server.

When we get a result of a `get` query that was performed with both inference and explain options **enabled** we 
can use an **explain** query to request additional information on how the exact instances of data were inferred.

To do that use `explainables` method on the `get` query result (`ConceptMap`). It returns a stream of `explainable` 
objects. Send an `explainable` object with an **explain** query to get a stream of `explanations`.

Every `explanation` include information about what rule was used to obtain this inferred result, 
condition of the rule, conclusion of the rule and variable mapping.

### Python example

The following code (provided with a TypeDB server with IAM database from 
[Quickstart guide](../01-start/03-quickstart.md)) can infer `view_file` permission for multiple files for a single 
user and explain every inferred result. Basically, we repeat the previous example and then request explanation of 
relation `$pe`.

<!-- test-ignore -->
```python
from typedb.client import TypeDB, SessionType, TransactionType, TypeDBOptions

with TypeDB.core_client("0.0.0.0:1729") as client:  # Connect to TypeDB server
    with client.session("iam", SessionType.DATA) as session:  
        print("\nRequest #1: Explain query — Files that Kevin Morrison has view access to (with explanation)")
        typedb_options = TypeDBOptions.core()  # Initialising a new set of options
        typedb_options.infer = True  # Enabling inference in this new set of options
        typedb_options.explain = True
        with session.transaction(TransactionType.READ, typedb_options) as transaction:  
            typeql_read_query = "match $p isa person, has full-name $p-fname; $o isa object, has path $o-path;" \
                                "$a isa action, has action-name 'view_file'; $ac(accessed-object: $o, valid-action: $a) isa access;" \
                                "$pe(permitted-subject: $p, permitted-access: $ac) isa permission; $p-fname = 'Kevin Morrison';" \
                                "get $o-path; sort $o-path asc;"
            iterator = transaction.query().match(typeql_read_query)
            i = 0
            for item in iterator:  # Iterating through results
                i += 1
                explainable_relations = item.explainables().relations()
                e = 0
                for explainable in explainable_relations:
                    e += 1
                    explain_iterator = transaction.query().explain(explainable_relations[explainable])
                    ex = 0
                    for explanation in explain_iterator:
                        ex += 1
                        
                        print("\nRead result #:", i, ", File path:", item.get("o-path").as_attribute().get_value())
                        print("Explainable #:", e, ", Explained variable:", explainable)
                        print("Explainable object:", explainable_relations[explainable])
                        print("Explainable part of query:", explainable_relations[explainable].conjunction())
                        print("Explanation #:", ex)
                        
                        print("\nRule: ", explanation.rule().get_label())
                        print("Condition: ", explanation.condition())
                        print("Conclusion: ", explanation.conclusion())
                        print("Variables used in explanation: ", explanation.variable_mapping())
                        print("----------------------------------------------------------")
```

The script above runs the query from the [example](#example) in the previous section. The inference option provides 
the result of 10 files (by default in the IAM database from the [Quickstart guide](../01-start/03-quickstart.md)). 
And `explain` option enables the `explainables` to be received and used in the **explain** queries (one explain query 
for each result that needs to be explained).

#### Output

The result should be similar to the following:

<!-- test-ignore -->
```
Read result #: 10 , File path: zlckt.ts
Explainable #: 1 , Explained variable: pe
Explainable object: &lt;typedb.concept.answer.concept_map._ConceptMap.Explainable object at 0x105cb34f0>
Explainable part of query: { $pe (permitted-subject:$p, permitted-access:$ac); $pe isa permission; }
Explanation #: 1

Rule:  add-view-permission

Condition:  [_1/_StringAttribute[action-name:0x836f800328000b6d6f646966795f66696c65]][_2/_StringAttribute[action-name:0x836f8003280009766965775f66696c65]][_3/_Relation[permission:0x847080038000000000000001]][ac_modify/_Relation[access:0x8470800a8000000000000003]][ac_view/_Relation[access:0x8470800a8000000000000011]][modify/_Entity[operation:0x826e800c8000000000000001]][obj/_Entity[file:0x826e80098000000000000004]][subj/_Entity[person:0x826e80018000000000000001]][view/_Entity[operation:0x826e800c8000000000000000]]

Conclusion:  [_/_Relation[permission:0x847080037fffffffffffffff]][_permission/_RelationType[label: permission]][_permission:permitted-access/_RoleType[label: permission:permitted-access]][_permission:permitted-subject/_RoleType[label: permission:permitted-subject]][ac_view/_Relation[access:0x8470800a8000000000000011]][subj/_Entity[person:0x826e80018000000000000001]]

Variables used in explanation:  {'p': {'subj'}, 'ac': {'ac_view'}, 'pe': {'_'}}

----------------------------------------------------------
```

#### Explanation parsing

The `explanation.rule().get_label()` method returns the name of the rule that was used for this particular inference, 
hence the result of which is being explained:

<!-- test-ignore -->
```
add-view-permission
```

The `explanation.variable_mapping()` method returns mapping of the variable names in the query with variable names in 
the rule:

<!-- test-ignore -->
```
{'p': {'subj'}, 'ac': {'ac_view'}, 'pe': {'_'}}
```

The `explanation.condition()`method returns the condition of the rule written with the exact matched instances of data.

For the rule condition defined as: 

<!-- test-ignore -->
```
$modify isa action, has action-name "modify_file";
$view isa action, has action-name "view_file";
$ac_modify (accessed-object: $obj, valid-action: $modify) isa access;
$ac_view (accessed-object: $obj, valid-action: $view) isa access;
(permitted-subject: $subj, permitted-access: $ac_modify) isa permission; \
```

We got the condition explained with particular instances from the IAM dataset:

<!-- test-ignore -->
```
[_1/_StringAttribute[action-name:0x836f800328000b6d6f646966795f66696c65]]
[_2/_StringAttribute[action-name:0x836f8003280009766965775f66696c65]]
[_3/_Relation[permission:0x847080038000000000000001]]
[ac_modify/_Relation[access:0x8470800a8000000000000003]]
[ac_view/_Relation[access:0x8470800a8000000000000011]]
[modify/_Entity[operation:0x826e800c8000000000000001]]
[obj/_Entity[file:0x826e80098000000000000004]]
[subj/_Entity[person:0x826e80018000000000000001]]
[view/_Entity[operation:0x826e800c8000000000000000]]
```

The example above contains additional line breakers for convenience. The syntax of the condition is similar to 
the following:

<!-- test-ignore -->
```
[<rule_variable_label>/<BaseType>[<Type>:<IID>]]
```

Those are exact instances of data that was matched by the rule. For example, `obj` is a `file` type entity that has 
an attribute of `path` type of value `zlckt.ts`. We didn’t got the `path` in the explanation because it wasn't 
mentioned in the rule, but was able to obtain it by the API call from the get query result: 

<!-- test-ignore -->
```
item.get("o-path").as_attribute().get_value())
```

The `explanation.conclusion()` method returns the conclusion of the rule written with the exact instances of data 
(including the inferred instance of data that exists only virtually — as a result of the inference).

For the rule condition defined as:

<!-- test-ignore -->
```
(permitted-subject: $subj, permitted-access: $ac_view) isa permission;
```

We got the conclusion explained with particular instances from the IAM dataset:

<!-- test-ignore -->
```
[_/_Relation[permission:0x847080037fffffffffffffff]]
[_permission/_RelationType[label: permission]]
[_permission:permitted-access/_RoleType[label: permission:permitted-access]] 
[_permission:permitted-subject/_RoleType[label: permission:permitted-subject]] 
[ac_view/_Relation[access:0x8470800a8000000000000011]]
[subj/_Entity[person:0x826e80018000000000000001]]
```

The example above contains additional line breakers for convenience. The syntax of the condition is similar to following:

<!-- test-ignore -->
```
[<rule_variable>/<BaseType>[<Type>:<IID>]]
```
