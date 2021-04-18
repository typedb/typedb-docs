---
pageTitle: Rules
keywords: graql, rule, reasoning, automated reasoning
longTailKeywords: grakn reasoning, grakn automated reasoning, grakn rules
Summary: Automated reasoning with Rules in Grakn.
---

## What is a Rule?
Grakn is capable of reasoning over data via rules defined in the schema. They can be used to automatically infer new facts, based on the existence of patterns in your data. Rules can enable you to dramatically shorten complex queries, perform explainable knowledge discovery, and implement business logic at the database level. 

Reasoning, or inference, is performed at query time and is guaranteed to be complete. When executing a `match` query, the execution engine returns data that directly answers the query, and also inspects and triggers rules that may lead to new answers to the query. This approach is known as backwards-chaining (starting from the query, then finding applicable rules and generating relevant new facts). Reasoning can proceed via one rule to other rules, including recursively, leading to complex behaviours emerging from a few simple rules.

In this section we will explain the concept of Graql rules. We will explain their structure and meaning as well as go through how to use them to capture dynamic facts about our knowledge graph.


<div class="note">
[Important]
Inferred facts are transaction-bound: during a single transaction newly inferred facts will be retained and reused (with corresponding peformance gains). New transactions will re-compute inferred facts again.
</div>


<div class="note">
[Important]
Currently, for a match query to trigger reasoning and obtain inferences from rules, you must use a _read_ transaction. We are working towards enabling reasoning in write transactions in subsequent releases.
</div>


## Define a Rule
Defining a Graql rule begins with a `rule` followed by a given label, the `when` body as the condition, and the `then` body as the conclusion.
<!-- test-ignore -->
```graql
define 

rule rule-label:
  when {
    ## the condition
  } then {
    ## the conclusion
  };
```

Each hashed line corresponds to a single Graql statement. In Graql, the "when" part of the rule is required to be a conjunctive pattern, whereas the "then" should describe a single `has` or `relation`. If your use case requires a rule with a disjunction ("or") in the `when` part, notice that several rules with the same conclusion can be easily created to achieve the same behaviour.

Let us have a look at an example. We want to express the fact that two given people are siblings. As we all know, for two people to be siblings, we need the following facts to be true:
- they share the same mother
- they share the same father
- they are not the same person

To express those facts in Graql, we can write:
<!-- test-delay -->
```graql
{
    (mother: $m, $x) isa parentship;
    (mother: $m, $y) isa parentship;
    (father: $f, $x) isa parentship;
    (father: $f, $y) isa parentship;
};
```

If you find the Graql code above unfamiliar, don't be concerned. We soon learn about [using Graql to describe patterns](/docs/query/match-clause). Those requirements will serve as the `when` part of the rule. Next, we define the conclusion of our rule - the fact that two people are siblings:

```
(sibling: $x, sibling: $y) isa siblings;
```

Combining all this information we can finally define our rule as following.

<div class="tabs dark">

[tab:Graql]
```graql
define

rule people-with-same-parents-are-siblings:
when {
    (mother: $m, $x) isa parentship;
    (mother: $m, $y) isa parentship;
    (father: $f, $x) isa parentship;
    (father: $f, $y) isa parentship;
} then {
    (sibling: $x, sibling: $y) isa siblings;
};
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  rule("people-with-same-parents-are-siblings")
    .when(
        and(
            var().rel("mother", "m").rel("x").isa("parentship"),
            var().rel("mother", "m").rel("y").isa("parentship"),
            var().rel("father", "f").rel("x").isa("parentship"),
            var().rel("father", "f").rel("y").isa("parentship")
        )
    ).then(
        var().rel("sibling", "x").rel("sibling", "y").isa("siblings")
    )
);
```
[tab:end]
</div>

Note that facts defined via rules are not stored in the knowledge graph. In this example, siblings relations are not persisted. However, by defining the rule in the schema, at query time the extra fact will be generated so that we can always know who the siblings are.


### Forms of Rule

Grakn supports inferring new, full facts in rules. There are exactly three distinct conclusions (`then`) that are permitted by this principle:

* Inferring a complete new relation, as in our above example. 

<div class="tabs dark">

[tab:Graql]
```graql
define

rule people-with-same-parents-are-siblings:
when {
    (mother: $m, $x) isa parentship;
    (mother: $m, $y) isa parentship;
    (father: $f, $x) isa parentship;
    (father: $f, $y) isa parentship;
} then {
    (sibling: $x, sibling: $y) isa siblings;
};
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  rule("people-with-same-parents-are-siblings")
    .when(
        and(
            var().rel("mother", "m").rel("x").isa("parentship"),
            var().rel("mother", "m").rel("y").isa("parentship"),
            var().rel("father", "f").rel("x").isa("parentship"),
            var().rel("father", "f").rel("y").isa("parentship")
        )
    ).then(
        var().rel("sibling", "x").rel("sibling", "y").isa("siblings")
    )
);
```
[tab:end]
</div>

* Inferring an attribute ownership of a constant attribute 

<div class="tabs dark">

[tab:Graql]
```graql
define

rule anne-is-nickname-for-annabelle:
when {
    $p isa person, has full-name "Annabelle";
} then {
    $p has nickname "Anne";
};
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  rule("anne-is-nickname-for-annabelle")
    .when(
        and(
            var("p").isa("person").has("full-name", "Annabelle")
        )
    ).then(
        var("p").has("nickname", "Anne")
    )
);
```
[tab:end]
</div>

Here, we apply a constant attribute that may or may not previously exist in the database, as a new fact that is owned by `$p`, which is any person with name "Annabelle".

* Inferring an ownership of a variable attribute

<div class="tabs dark">

[tab:Graql]
```graql
define

rule student-graduated-implies-person-graduated:
when {
    $p isa person;
    $s (student: $p) isa studentship;
    $s has graduated $is-graduated;
} then {
    $p has $is-graduated;
};
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  rule("student-graduated-implies-person-graduated")
    .when(
        and(
            var("p").isa("person"),
            var("r").rel("student", "p").isa("studentship"),
            var("r").has("graduated", var("is-graduated"))
        )
    ).then(
        var("p").has(var("is-graduated"))
    )
);
```
[tab:end]
</div>

In this example, we take a pre-existing attribute that is attached to a relation, and re-attach it to another data instance.


### Rule Validation

Besides conforming to one of the three patterns previously outlined, we also require that:

1. The `then` of the rule must be insertable according to the schema (eg. you cannot give an attribute to an instance that is not allowed to own that attribute type). Grakn will reject rules that could insert incompatible data.
2. There are no disjunctions in the `when` of the rule
3. There are no negations in the `when` of the rule (this restriction will be lifted imminently)


### Advanced Usage

When inferring relations, it is possible to variabilise any part of the `then` of the rule. For example, if we know we wanted a rule to infer many different types of relations, we could propose a rule such as:

<div class="tabs dark">

[tab:Graql]
<!-- test-ignore -->
```graql
define

rule all-relation-types-are-transitive:
when {
    ($role1: $x, $role2: $y) isa! $relation;
    ($role1: $y, $role2: $z) isa! $relation;
} then {
    ($role1: $x, $role2: $z) isa $relation;
};
```
[tab:end]

[tab:Java]
<!-- test-ignore -->
```java
GraqlDefine query = Graql.define(
  rule("all-relation-types-are-transitive")
    .when(
        and(
            var().rel(var("role1"), var("x")).rel(var("role2"), var("y")).isaX(var("relation")),
            var().rel(var("role1"), var("y")).rel(var("role2"), var("z")).isaX(var("relation"))
        )
    ).then(
        var().rel(var("role1"), var("x")).rel(var("role2"), var("z")).isa(var("relation"))
    )
);
```
[tab:end]
</div>

This rule will make every relation transitive.

## Optimisation Notes

There are two general tips for making queries with reasoning execute faster:
1. Adding a limit to the query. Without a limit, the reasoning engine is forced to explore all possible ways to answer the query exhaustively. If you only need 1 answer, adding `limit 1` to the `match` query can improve query times.
2. Using the same transaction for multiple reasoning queries. Because inferred facts are cleared between transactions, running the same or similar queries within one transaction can reuse previously found facts. Combined with a `limit` on the query, it might be possible to avoid having to do any new reasoning at all.

For complex queries, it can also be beneficial to add more CPU cores, as the reasoning engine is able to explore more paths in the database concurrently.

## Delete a Rule

Rules like any other schema members can be undefined. Consequently, to delete rules we refer to them by their label and use the [undefine keyword](../09-schema/01-concepts.md#undefine).
For the case of the rule defined above, to delete it we write:

<!-- test-delay -->
```graql
undefine rule people-with-same-parents-are-siblings;
```

<div class="note">
[Important]
Don't forget to `commit` after executing a `undefine` query. Otherwise, anything you have undefined is NOT committed to the original database that is running on the Grakn server.
When using one of the Grakn Clients, to commit changes, we call the `commit()` method on the `transaction` object that carried out the query. Via the Graql Console, we use the `commit` command.
</div>

## Functional Interpretation
Another way to look at rules is to treat them as functions. In that way, we treat each statement as a function returning either true or false. Looking again at the body of our siblings rule:
<!-- test-delay -->
```graql
{
    (mother: $m, $x) isa parentship;
    (mother: $m, $y) isa parentship;
    (father: $f, $x) isa parentship;
    (father: $f, $y) isa parentship;
};
```

To simplify this logic even further, you can think of the [siblings example](#define-a-rule) in form of an `if` statement like so:
<!-- test-ignore -->
```java
for a given (m, f, x, y) tuple

if (parentship(m, x)
  && parentship(m, y)
  && parentship(f, x)
  && parentship(f, y)) {
     siblings(x, y) will return true
}
```

<div class="note">
[Advanced]
Rules as Horn Clauses can be defined either in terms of a disjunction with at most one unnegated atom or an implication with the consequent consisting of a single atom. Atoms are considered atomic first-order predicates - ones that cannot be decomposed to simpler constructs.
In our system, we define both the head and the body of rules as Graql patterns. Consequently, the rules are statements of the form:

```
q1 ∧ q2 ∧ ... ∧ qn → p
```

where `q`s and the `p` are atoms that each correspond to a single Graql statement. The “when” of the statement (antecedent) then corresponds to the rule body with the “then” (consequent) corresponding to the rule head.

The implication form of Horn clauses aligns more naturally with Graql semantics as we define the rules in terms of the “when” and “then” blocks which directly correspond to the antecedent and consequent of the implication respectively.
</div>


## Summary
Rules are a powerful tool that allows to reason over the explicitly stored data and produce implicit knowledge at run-time.

In the next section, we learn how to [perform read and write instructions over a knowledge graph](../11-query/00-overview.md) that is represented by a schema.
