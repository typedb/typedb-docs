---
sidebarTitle: Negation
pageTitle: Pattern Negation
permalink: /docs/query/pattern-negation
---

## Queries with negation

Oftentimes we encounter situations where we would like to form queries with the use of negation.
Examples of such queries include:

a) List all people that were unemployed in the last 6 months

b) Show me text-only timelines (no videos or images) 

c) All single people who have posted a photo in a forum

The intuitive meaning of a negated pattern is that of a complement. However relation complement is not a clearly defined term as it requires 
the definition of a domain of values with respect to which the complement is computed. Even in this case we end up with an infinite relation which leaves 
the projection or join operations unapplicable. As a result, we understand pattern negation in terms of computation of set differences. The set-difference semantics
are different to the perhaps familiar semantics of _Negation-as-Failure_ of Prolog and in this chapter we will attempt to provide a clear explanation of the meaning
of pattern negation in Graql.

Let us consider the relation of unemployment which can be trivially understood as the absence of employment. We define negation blocks by enclosing patterns with
curly braces and preceding them with a `not` keyword:

```
not {
    ...
};
```

Therefore, to retrieve people the that are unemployed we want to express:

```
Person($x), ¬Employment($x, employer: $y)
```

i.e. we look for the following Graql pattern:

<div class="tabs dark">

[tab:Graql]
```graql
{
    $x isa person;
    not {
        (employee: $x, employer: $y) isa employment;
    };
};
```
[tab:end]

[tab:Java]
```java
Pattern pattern = Graql.and(
        Graql.var("x").isa("person"), 
        Graql.not(
            Graql.var().isa("employment")
                .rel("employee", Graql.var("x"))
                .rel("employer", Graql.var("y"))
            )
        );
```
[tab:end]
</div>

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
$x isa person;
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
The rule interpretation above is for understanding purposes only. As a user the only thing we need to type is our query pattern:

```graql
{
    $x isa person;
    not {
        (employee: $x, employer: $y) isa employment;
    };
};
```

The variables in the negation block are local to the negation block. Consequently, executing the query:

<div class="tabs dark">

[tab:Graql]
```graql
match
$x isa person;
not {
    (employee: $x, employer: $y) isa employment;
};
get;
```
[tab:end]

[tab:Java]
```java
GraqlGet query = Graql.match(
    Graql.and(
        Graql.var("x").isa("person"), 
        Graql.not(
            Graql.var().isa("employment")
                .rel("employee", Graql.var("x"))
                .rel("employer", Graql.var("y"))
        )
    )
).get();
```
[tab:end]
</div>

will yield a list of concepts assigned to the `$x` variable.

Should we decide that our unemployment pattern is a common one, we might decide to express it via a rule. In the case when the 
set of bound variables has only one element, it is more convenient to define it in terms of a type. 
Defining the unemployment in terms of a rule and the freshly introduced negation block we can then write: 

```graql
define
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

<div class="tabs dark">

[tab:Graql]
```graql
{
    $x isa person;
    $x isa unemployed;
};
```
[tab:end]

[tab:Java]
```java
Pattern pattern = Graql.and(
    Graql.var("x").isa("person"), 
    Graql.var("x").isa("unemployed")
);
```
[tab:end]

Negation blocks are not tied to relations. We are free to define our patterns inside the negation blocks as long as they are conjunctive. For example we can use negation
blocks to perform exclusions, e.g. the query pattern to list all non-English speaking employees can read:

<div class="tabs dark">

[tab:Graql]
```graql
{
    (employee: $x) isa employment;
    (speaker: $x, spoken: $y) isa speaking-of-language;
    not { $y == "English";};
};
```
[tab:end]

[tab:Java]
```java
Pattern pattern = Graql.and(
    Graql.var().isa("employment").rel("employee", Graql.var("x")),
    Graql.var().isa("speaking-of-language")
        .rel("speaker", Graql.var("x"))
        .rel("spoken", Graql.var("y")),
    Graql.not(Graql.var("y").val("English"))
);
```
[tab:end]

We shall now see how we can form more complex patterns with negation. Let's say we want to find people that are orphans:

```
Person($x), ¬Parentship($x, father: $y), ¬Parentship($x, mother: $y)
```

To express that in Graql, we require two negation blocks:

```graql
{
    $x isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
}; 
```

which is equivalent to saying:

```
$x isa person;
not { $x isa person-with-a-father;};
not { $x isa person-with-a-mother;};
```

Now let's look at how we arrive at the answers if we execute this as a match query. To do this we will go through
the set difference computation procedure. Let's define a set `P` to be the set of all people, i.e. a set that is the answer set to a query:

```graql
match $x isa person; get;
```
 
a set `F` as the set of people having a father, i. e. a set that is the answer set of a query: 

```
match $x isa person-with-a-father;get;
```
and finally a set `M` as the set of people having a mother which can be defined in terms of a query:

```
match $x isa person-with-a-mother;get;
```

We can illustrate the relationships between the sets with a suitable Venn diagram:

![Calculating the P \ F \ M set difference](/docs/images/query/PFM.png)

Consequently, our set of answers of our match pattern is defined as `A = P \ F \ M`. As a result, from the set of all people we subtract those who have a father and those who have a mother.
Please note that the scope of variables in a negation block is local to the negation block. As a result the above pattern does not look for people that do not have a mother and a father that is the same person.

Now let's say we have three people, Alice (A), Bob (B) and Charlie (C). Consequently our set `P` reads:

```
P = {Alice, Bob, Charlie}
```

Additionally let's say we know that the following two `parentship` relations hold:

```
Parentship(child: Alice, father: Bob)
Parentship(child: Bob, mother: Charlie)
```

i.e. Bob is the father of Alice and Charlie is the mother of Bob.

This results in our sets `F` and `M` being defined as:

```
F = {Alice}
M = {Bob}
```

Consequently, the final result of the match query:

```graql
match
$x isa person;
not { ($x, father: $y) isa parentship;};
not { ($x, mother: $y) isa parentship;};
get; 
```

will only have the Charlie concept as the result obtained by computing the set difference:

```
A = P \ F \ M = {Charlie}
```

Now let's complicate things a little and see what happens if we bind the `$y` variable for parents, i. e. if we consider a query pattern:

```graql
{
    $x isa person;
    $y isa person;
    not { ($x, father: $y) isa parentship;};
    not { ($x, mother: $y) isa parentship;};
};
```

Upon inspection, we can see that in this case our three sets are different. Let's define them as `P'`, `M'` amd `F'`.
The first difference is that an element of each set is a pair (2-tuple). Our set of people `P` corresponds to the answer set of a match query:

```graql
match
$x isa person;
$y isa person;
get;
```

As a result, we have (abbreviating the names for clarity):

```
P' = { 
        (A, A), (A, B), (A, C),
        (B, A), (B, B), (B, C),
        (C, A), (C, B), (C, C)
}
```

Now the set `F'` is a set of pairs `{($x, $y)}` such that the concepts in the pair are connected via `parentship` relation with the concept assigned to `$y` variable playing the role of a father. 
Similarly the set `M'` is a set of pairs `{($x, $y)}` such that the concepts in the pair are connected via `parentship` relation with the concept assigned to `$y` variable playing the role of a mother. 
Consequently we have:

```
F' = {(A, B)}
M' = {(B, C)}
```

Now, executing our query pattern as an ordinary match-get query:

```graql
match
$x isa person;
$y isa person;
not { ($x, father: $y) isa parentship;};
not { ($x, mother: $y) isa parentship;};
get;
```

we yield the following concept pairs mapped to `$x` and `$y` variables:

```
A'' = P' \ F' \ M' = 
{ 
        (A, A), (A, C),
        (B, A), (B, B), 
        (C, A), (C, B), (C, C)
}
```

However! If we now do a projection onto the `$x` variable to compare the results with our previous query variant where 
the `$y` variable is unbounded, i.e. if we execute:

```graql
match
$x isa person;
not { ($x, father: $y) isa parentship;};
not { ($x, mother: $y) isa parentship;};
get $x;
```

we will get the following concepts in return:

```
A' = P' \ F' \ M' | x = {A, B, C}
```
which is clearly different to the anticipated result of `A = {C}` - our answer set is not a set of orphans, instead 
it is a projection from a set of people pairs where pairs playing in `parentship` relation excluded. 
As a result, extra care should be taken and thought given when formulating queries with negation blocks.

One might be tempted to put the two negation blocks into one. Let's look at the outcome of that. If we define:


```graql
{
    $x isa person;
    not { 
        ($x, father: $y) isa parentship;
        ($x, mother: $z) isa parentship;
    };
};
```
noting that this time we need to pick a fresh variable for mother as we are in the same negation block. The meaning of this pattern is the following. From all people,
remove the people that have both a mother and a father. As a result our answer set will contain people that have at most one parent.

We can go further than that. Negation blocks in queries can be nested. Consequently, if we wanted to find people whose father is unemployed we can write something
like this:

```graql
{
    $x isa person;
    not { 
        ($x, father: $y) isa parentship;
        not { ($y) isa employment; };
    };
};
```

Please note, nesting of negation blocks is only allowed in queries, but not in rules.

## Negation blocks: DOs and DONTs

Please note, the following restrictions apply to negation blocks:
- for each negation block in a query, at least one variable in the negation block must be bound to a statement outside of the negation block
This ensures that set difference operations are performed on sets that are not disjoint.
- variables in negation blocks are local to the block they are defined in
- only conjunctive statements are allowed within negation blocks


## Negation in rules
As we have already mentioned, we can use negation blocks within rules.
 
However, when inserting negation blocks in rules, currently the following restrictions apply:
- all restrictions applying to queries with negation blocks
- each rule can only have a single negation block
- nested negation blocks are not supported
- recursion with negation blocks is not supported 

We will illustrate the use of negation with rules with a graphical example.

Let us define a network of nodes with possible edges between nodes:

```graql
define

traversable sub entity,
    plays from,
    plays to;

node sub traversable;

edge sub relation, relates from, relates to;
```

Then we can define two nodes as being reachable if there exists a edge between them:

```graql
define

reachable sub relation, relates from, relates to;
reachabilityA sub rule,
when {
    (from: $x, to: $y) isa edge;
},
then {
    (from: $x, to: $y) isa reachable;
};

reachabilityB sub rule,
when {
    (from: $x, to: $z) isa edge;
    (from: $z, to: $y) isa reachable;
},
then {
    (from: $x, to: $y) isa reachable;
};
```

Consequently, with the use of negation we can define edges that are indirect:

```graql
define

indirect-edge sub relation, relates from, relates to;
indirect-edge-rule sub rule,
when {
    (from: $x, to: $y) isa reachable;
    not {(from: $x, to: $y) isa edge;};
},
then {
    (from: $x, to: $y) isa indirect-edge;
};
```

We can mark the unreachable nodes by defining the following rule:

```graql
define

unreachable sub relation, relates from, relates to;
unreachability-rule sub rule,
when {
    $x isa node;
    $y isa node;
    not {(from: $x, to: $y) isa reachable;};
},
then {
    (from: $x, to: $y) isa unreachable;
};
```

Please note the explicit addition of the `node` types in the body of the rule. This is to to ensure the boundedness condition
is satisfied as well as to maintain the expected meaning of the `unreachable` relation.

## Monotonicity of reasoning with negation

In this subsection we address an important property of reasoning - the monotonicity property.
We say that reasoning is monotonic if previously derived facts remain true upon addition of new knowledge. 
Without employing pattern negation in rules, Graql reasoning is monotonic. When pattern negation is used in rules however, this property no longer holds.
Preserving monotonicity is not strictly necessary or required, however it is important to be aware of the consequences of non-monotonic reasoning 
and how it possibly affects querying. We can illustrate this with a popular example:

Let's start with our knowledge to be the following:

- birds fly unless they are abnormal
- penguins are abnormal birds
- penguins are birds

This can be summarised as:

```
flies(X) :-  bird(X), ¬abnormal(X)
abnormal(X) :- penguin(X)
bird(X) :- penguin(X)
```

We can capture this information in Graql terms. Defining our little schema first:

```graql
define

bird sub entity;
penguin sub bird;
flies sub entity;
abnormal sub entity;

```

Accompanying it with relevant rules:

```graql
define

flying-rule sub rule,
when{
    $x isa bird;
    not {$x isa abnormal;};
},
then{
    $x isa flies;
};

abnormal-rule sub rule,
when{
    $x isa penguin;
},
then{
    $x isa abnormal;
};
```
Let's now say that we there is a bird which we will call Tweety:

<!-- test-ignore -->
```graql
insert $x isa bird;
```

In consequence of the above knowledge, we can establish that Tweety flies, i.e. if we query:

<!-- test-ignore -->
```graql
match $x isa flies; get;
```

our single Tweety bird concept will be returned. Let us now look what will happen if we add an extra bit of information.
We will specialise Tweety to be a penguin:

<!-- test-ignore -->
```graql
match $x isa bird; delete;
insert $x isa penguin;
```

If we now repeat our flying query:
 
<!-- test-ignore -->
```graql
match $x isa flies; get;
```
 
we will receive no answers. Consequently our previously derived fact of Tweety being able to fly no longer holds.

This illustrates the fact that when using pattern negation in rules, we lose the guarantee of all our previous inferences being true upon addition of new 
information be it new data or rules.
