---
pageTitle: Rules
keywords: graql, rule, reasoning, automated reasoning
longTailKeywords: grakn reasoning, grakn automated reasoning, grakn rules
Summary: Automated reasoning with Rules in Grakn.
---

## What is a Rule?
Grakn is capable of reasoning over data via pre-defined rules. Graql rules look for a given pattern in the dataset and when found, create the given queryable relation. Automated reasoning provided by rules is performed at query (run) time. Rules not only allow shortening and simplifying commonly-used queries but also enable knowledge discovery and implementation of business logic at the database level.

The rule-based reasoning allows automated capture and evolution of patterns within the knowledge graph. Graql reasoning is performed at query time and is guaranteed to be complete. Thanks to the reasoning facility, common patterns in the knowledge graph can be defined and associated with existing schema elements. The association happens by means of rules. This not only allows us to compress and simplify typical queries, but offers the ability to derive new non-trivial information by combining defined patterns. Once a given query is executed, Graql will not only query the knowledge graph for exact matches but will also inspect the defined rules to check whether additional information can be found (inferred) by combining the patterns defined in the rules. The completeness property of Graql reasoning guarantees that, for a given content of the knowledge graph and the defined rule set, the query result shall contain all possible answers derived by combining database lookups and rule applications.

In this section we will explain the concept of Graql rules. We will explain their structure and meaning as well as go through how to use them to capture dynamic facts about our knowledge graph.

## Define a Rule
Defining a Graql rule begins with a given label followed by `sub rule`, the `when` body as the condition, and the `then` body as the conclusion.
<!-- test-ignore -->
```graql
define 

rule-label sub rule,
  when {
    ## the condition
  }, then {
    ## the conclusion
  };
```

Each hashed line corresponds to a single Graql statement. In Graql, the "when" part of the rule is required to be a conjunctive pattern, whereas the "then" should be atomic - each rule can derive a single fact only. If our use case requires a rule with a disjunction in the "when" part, please notice that, when using the disjunctive normal form, it can be decomposed into series of conjunctive rules.

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
    $x != $y;
};
```

If you find the Graql code above unfamiliar, don't be concerned. We soon learn about [using Graql to describe patterns](/docs/query/match-clause). Please note the variable inequality requirement. Without it, $x and $y can still be mapped to the same concept. Those requirements will serve as our `when` part of the rule. What remains to be done is to define the conclusion of our requirements - the fact that two people are siblings. We do it simply by writing the relevant relation pattern:

```
(sibling: $x, sibling: $y) isa siblings;
```

Combining all this information we can finally define our rule as following.

<div class="tabs dark">

[tab:Graql]
```graql
define

people-with-same-parents-are-siblings sub rule,
when {
    (mother: $m, $x) isa parentship;
    (mother: $m, $y) isa parentship;
    (father: $f, $x) isa parentship;
    (father: $f, $y) isa parentship;
    $x != $y;
}, then {
    ($x, $y) isa siblings;
};
```
[tab:end]

[tab:Java]
```java
GraqlDefine query = Graql.define(
  type("people-with-same-parents-are-siblings").sub("rule")
    .when(
        and(
            var().rel("mother", "m").rel("x").isa("parentship"),
            var().rel("mother", "m").rel("y").isa("parentship"),
            var().rel("father", "f").rel("x").isa("parentship"),
            var().rel("father", "f").rel("y").isa("parentship"),
            var("x").neq("y")
        )
    ).then(
        var().isa("siblings").rel("x").rel("y")
    )
);
```
[tab:end]
</div>

Please note that facts defined via rules are in general not stored in the knowledge graph. In this example, siblings data is not explicitly stored anywhere in the knowledge graph. However by defining the rule in the schema, at query time the extra fact will be generated so that we can always know who the siblings are.

If you find the Graql code above unfamiliar, don't be concerned. We soon learn about [using Graql to describe patterns](../11-query/01-match-clause.md).

In this example, siblings data is not explicitly stored anywhere in the knowledge graph. But by having included this rule in the schema, we can always know who the siblings are and use the `siblings` relation in our queries.

## Retrieve a Rule
To provide a quick preview of how you can use the following Graql queries to retrieve rules:

```graql
# retrieve all rules
match $r sub rule; get;  
# retrieve the specific rule
match $r type people-with-same-parents-are-siblings; get; 
```

Remember that rules are part of the schema and can be queried the same way as other schema concepts described in [Graql Match documentation](../11-query/01-match-clause.md).

## Delete a Rule

Rules like any other schema members can be undefined. Consequently, to delete rules we refer to them by their label and use the [undefine keyword](../09-schema/01-concepts.md#undefine).
For the case of the rule defined above, to delete it we write:

<!-- test-delay -->
```graql
undefine people-with-same-parents-are-siblings sub rule;
```

<div class="note">
[Important]
Don't forget to `commit` after executing a `undefine` query. Otherwise, anything you have undefined is NOT committed to the original keyspace that is running on the Grakn server.
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
    $x != $y;
};
```

To simplify this logic even further, you can think of the [siblings example](#define-a-rule) in form of an `if` statement like so:
<!-- test-ignore -->
```java
for a given (m, f, x, y) tuple

if (parentship(m, x)
  && parentship(m, y)
  && parentship(f, x)
  && parentship(f, y)
  && x != y) {
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
