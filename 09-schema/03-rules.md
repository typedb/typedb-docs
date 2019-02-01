---
sidebarTitle: Rules
pageTitle: Rules
permalink: /docs/schema/rules
---

## What is a Rule?
Grakn is capable of reasoning over data via pre-defined rules. Graql rules look for a given pattern in the dataset and when found, create the given queryable relationship. Automated reasoning provided by rules is performed at query (run) time. Rules not only allow shortening and simplifying commonly-used queries but also enable knowledge discovery and implementation of business logic at the database level.

When you query the knowledge graph for certain information, Grakn returns a complete set of answers. These answers contain explicit matches as well as implicit ones that have been inferred by the rules included in the schema.

In this section, we learn more about how rules are constructed and how they are meant to be used.

## Define a Rule
Defining a Graql rule begins with a given label followed by `sub rule`, the `when` body as the condition, and the `then` body as the conclusion.

```graql
define

rule-label sub rule,
  when {
    ## the condition
  } then {
    ## the conclusion
  };
```

Let's look an example.

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
  } then {
    ($x, $y) isa siblings;
  };
```
[tab:end]

[tab:Java]
```java
DefineQuery query = Graql.define(
  label("people-with-same-parents-are-siblings").sub("rule").when(
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

[tab:Javascript]
```nodejs
await transaction.query("define people-with-same-parents-are-siblings sub rule, when { (mother: $m, $x) isa parentship; (mother: $m, $y) isa parentship; (father: $f, $x) isa parentship; (father: $f, $y) isa parentship; $x != $y; } then { ($x, $y) isa siblings; };");
```
[tab:end]

[tab:Python]
```python
transaction.query("define people-with-same-parents-are-siblings sub rule, when { (mother: $m, $x) isa parentship; (mother: $m, $y) isa parentship; (father: $f, $x) isa parentship; (father: $f, $y) isa parentship; $x != $y; } then { ($x, $y) isa siblings; };")
```
[tab:end]
</div>

<div class = "note">
[Note]
**For those developing with Client [Java](/docs/client-api/java)**: Executing a `define` query, is as simple as calling the [`withTx().execute()`](/docs/client-api/java#client-api-method-eager-executation-of-a-graql-query) method on the query object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Node.js](/docs/client-api/nodejs)**: Executing a `define` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/nodejs#client-api-method-lazily-execute-a-graql-query) function available on the [`transaction`](/docs/client-api/nodejs#client-api-title-transaction) object.
</div>

<div class = "note">
[Note]
**For those developing with Client [Python](/docs/client-api/python)**: Executing a `define` query, is as simple as passing the Graql(string) query to the [`query()`](/docs/client-api/python#client-api-method-lazily-execute-a-graql-query) method available on the [`transaction`](/docs/client-api/python#client-api-title-transaction) object.
</div>

The Graql rule above is telling Grakn the following:

when
: there are two different people (`$x` and `$y`) who have the same mother `$m` and the same father `$f`,

then
: those people (`$x` and `$y`) must be siblings.

If you find the Graql code above unfamiliar, don't be concerned. We soon learn about [using Graql to describe patterns](/docs/query/match-clause).

In this example, siblings data is not explicitly stored anywhere in the knowledge graph. But by having included this rule in the schema, we can always know who the siblings are and use the `siblings` relationship in our queries.

<!-- This is a basic example of how Graql rules can be useful. In a dedicated section, we learn about rules by looking at more examples of [rule-based automated reasoning](...). -->

## The Underlying Logic
Under the hood, rules are restricted to be definite Horn Clauses. In simple terms, the Graql statements placed in the `when` body form one single condition where all statements must be true for the rule to apply. The `then` body, on the other hand, is restricted to contain one single statement only.

To simplify this logic even further, you can think of the [siblings example](#define-a-rule) in form of an `if` statement like so:

```java
if (is-m-mother-of-x && is-m-mother-of-y && is-f-father-of-x && is-f-father-of-y && is-x-different-to-y) {
    are-x-and-y-siblings = true;
    // any more assignments break the rule!
}
```

<div class="note">
[Advanced Topic]
Rules as Horn Clauses can be defined either in terms of a disjunction with at most one unnegated atom or an implication with the consequent consisting of a single atom. Atoms are considered atomic first-order predicates - ones that cannot be decomposed to simpler constructs.
In our system, we define both the head and the body of rules as Graql patterns. Consequently, the rules are statements of the form:

```
q1 ∧ q2 ∧ ... ∧ qn → p
```

where `q`s and the `p` are atoms that each correspond to a single Graql statement. The “when” of the statement (antecedent) then corresponds to the rule body with the “then” (consequent) corresponding to the rule head.

The implication form of Horn clauses aligns more naturally with Graql semantics as we define the rules in terms of the “when” and “then” blocks which directly correspond to the antecedent and consequent of the implication respectively.
</div>

### What goes in the then body
The following are the types of one single statement that can be set as the conclusion of a rule in the `then` body:
- setting the type. Example: `$x isa person;`,
- assigning an explicit value to an attribute. Example: `$x has flag "incomplete";`, or
- inserting a relationship. Example: `($x, $y) isa siblings;`.

## Deleting Rules
Rules like any other concept types can be undefined. To do so, we use the [undefine keyword](/docs/schema/concepts#undefine).

## Summary
Rules are a powerful tool that reason over the explicitly stored data and produce and store implicit knowledge at run-time.

In the next section, we learn how to [perform read and write instructions over a knowledge graph](/docs/query/overview) that is represented by a schema.