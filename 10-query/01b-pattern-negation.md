---
sidebarTitle: Negation
pageTitle: Pattern Negation
permalink: /docs/query/pattern-negation
---

## Queries with negation

Oftentimes we encounter situations where we would like to form queries with the use of negation.
An examples of such queries include:

a) List all people that were unemployed in the last 6 months?
b) show me text-only (no videos are images) timelines
c) All people that are singles that have posted a photo in a forum
d) All employees of company A that are graduates of a given school

The intuitive meaning of a negated pattern is that of a complement. However relation complement is not a clearly defined term as it requires 
the definition of a domain of values with respect to which the complement is computed. Even in this case we end up with an infinite relation which leaves 
the projection or join operations unapplicable. As a result, we understand pattern negation in terms of computation of set differences. The set-difference semantics
are different to the perhaps familiar semantics of negation by failure of Prolog and in this chapter we will attempt to provide a clear explanation of the meaning
of pattern negation in Graql.

Let us consider the relation of unemployment which can be trivially understood as the absence of employment. We define negation blocks by enclosing patterns with
curly braces and preceding them with a `not` keyword:

```
not {
    ...
};
```

Therefore to retrieve people the that are unemployed we want to express:

```
Person($x), ¬Employment($x, employer: $y)
```

i.e. we look for the pattern:

```
$x isa person
not {
    (employee: $x, employer: $y) isa employment;
};
```

Please note that the `$y` variable inside the negation block is not bound. This is of great importance when discussing the meaning of negation. 
If we were to interpret the query using the simple complement semantics we would arrive at a conclusion that unemployed people are people for which there exists 
a company that doesn't hire them - it would get evaluated to all `($x, $y)` pairs where `$x` is a person and `$y` isa a company that is not 
in an employment relation with `$x`. What we do instead is we interpret the negation block as some relation of arity equal to the number of variables that are bound
to non-negated statements. This imposes a requirment of at least one variable in the negation block being bound to a variable outside the block.
Here our only bound variable is `$x`. Consequently we can think of the query as:

```
Person($x), ¬???($x)
???($x) :- Employment($x, employer:$y)
```

In Graql terms it's equivalent to the pattern:

```
$x isa person
not { ($x) isa ???;};
```

with the question relation defined in terms of a rule:

```
negation-block sub rule,
when {
    (employee: $x, employer: $y) isa employment;
},
then {
    ($x) isa ???;
};
```

In this way, we have no problems defining the projection or join operations as these are handled by the native rule semantics. Consquently we can proceed with the set difference
semantics unambiguously. As a result, the unemployment is evaluated according to our expectation of unemployment as an absence of being part of any employment - from the
set of people we subtract the set of people being in employment relations. Please note that this example illustrates the basic mechanism of how patterns with negation are interpreted. 
The rule interpretation is for understanding purposes only. As a user the only thing we need to type is our query pattern:

```
$x isa person
not {
    (employee: $x, employer: $y) isa employment;
};
```

The variables in the negation block are local to the negation block. Consequently, executing the query:

```
match
$x isa person
not {
	(employee: $x, employer: $y) isa employment;
};
get;
```

will yield a list of concepts assigned to the `$x` variable.

Shall we decide that our unemployment pattern is a common one, we might decide to express it via rule.
Defining the unemployment it in terms of a rule and the freshly introduced negation block we can then write. In case when the set of bound variables has only one element, it is
more convenient to define it in terms of a type:

```
unemployed sub entity;
unemployment sub rule,
when {
    $x isa person;
    not{
        (employee: $x, employer: $y) isa employment;
    };
},
then {
    $x isa unemployed;
};
```

Consequently, our unemployment query pattern simply becomes:

```
$x isa person;
$x isa unemployed;
```

Negation blocks are not tied to relations. We are free to define our patterns inside the negation blocks as long as they are conjunctive. For example we can use negation
blocks to perform exclusions, e.g. the query pattern to list all non-English speaking employees can read:

```
(employee: $x) isa employment;
(speaker: $x, spoken: $y) isa speaking-of-language;
not { $y == "English";};
```

We shall now see how we can form more complex patterns with negation. Let's say we want to find people that are orphans:

```
Person($x), ¬Parentship($x, father: $y), ¬Parentship($x, mother: $y)
```

To formulate in Graql terms we require two negation blocks:

```
$x isa person
not { ($x, father: $y) isa parentship;};
not { ($x, mother: $y) isa parentship;};
```

This tells us to compute a set of answers `A = P \ F \ M`, where the set P is the set of all people, the set F is the set of all people having a father and the set M is the
set of all people having a mother. Please not that the scope of variables in a negation block is local to the negation block. As a result the above pattern does not 
look for people that do not have a mother and a father that is the same person.

One might be tempted to put the two negation blocks into one. Let's look at the outcome of that. If we define:


```
$x isa person;
not { 
	($x, father: $y) isa parentship;
	($x, mother: $z) isa parentship;
};
```
noting that this time we need to pick a fresh variable for mother as we are in the same negation block. The meaning of this pattern is the following. From all the people,
remove the people that have both a mother and a father. As a result our answer set will contain people that have at most one parent.

We can go further than that. Negation blocks in queries can be nested. Consequently, if we wanted to find people whose father is unemployed we can write something
like this:

```
$x isa person;
not { 
	($x, father: $y) isa parentship;
	not { ($y) isa employment; };
};
```

Please note, nesting of negation blocks is only allowed in queries, but not in rules.

## Negation blocks: DOs and DONTs

Please note, the following restrictions apply to negation blocks:
- for each negation block in a query, at least one variable in the negation block must be bound to a statement outside of the negation block
This ensures that set difference operations are performed on sets that are not disjoint.
- variables in negation blocks are local to the block they are defined in
- only conjunctive statements are allowed


## Negation in rules
As we have already mentioned, we can use negation blocks within rules.

However, when inserting negation blocks in rules, currently the following restrictions apply:
- all restrictions applying to queries with negation blocks
- each rule can only have a single negation block
- nested negation blocks are not supported
- recursion with negation blocks is not supported


## Monotonicity of reasoning with negation

In this subsection we will address an important property of reasoning being the monotonicity property.
We say that reasoning is monotonic if previously derived facts remain true upon addition of new knowledge. Up to this point Graql reasoning was monotonic. However with
the addition of pattern negation this property no longer holds. We can illustrate this fact in a popular example:

Let's start with our knowledge to be the following:

- birds fly unless they are abnormal
- penguins are abnormal birds
- penguins are birds
- Tweety is a bird

This can be summarised as:

```
flies(X) :-  bird(X), ¬abnormal(X)
abnormal(X) :- penguin(X)
bird(X) :- penguin(X)
```

We can capture this information in Graql terms:

Defining our little schema first:

```
bird sub entity;
penguin sub bird;
flies sub entity;
abnormal isa entity;
```

Accompanying it with relevant rules:

```
flying-rule sub rule,
when{
	$x isa bird;
	not {$x isa abnormal;};
},
then{
	$x isa flies;
}

abnormal-rule sub rule,
when{
	$x isa penguin;
},
then{
	$x isa abnormal;
}
```

In consequence of the above knowledge, we can establish that Tweety flies, i. e. if we query:

```
match $x isa flies;get;
```
the Tweety concept will be returned.

Let us now look what will happen if we add an extra bit of information - we will specialise Tweety to be a penguin. If we now repeat our flying query, we will
receive no answers. Consequently our previously derived fact no longer holds.