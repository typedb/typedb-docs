---
pageTitle: Query Pattern
keywords: typeql, schema, query, pattern, statements, match
longTailKeywords: typeql schema, typeql type hierarchy, typeql data model, typeql reserved keyword
Summary: Introduction to the TypeDB Schema.
---

# Query Pattern

In this section we explore patterns — building blocks of the majority of [TypeQL queries](../../11-query/00-overview.md).

## Queries



## Query pattern anatomy

At the core of each query sits a query pattern that describes a subset of data of our particular interest. Here we
<!--- Is the substitution of `subgraph` to `subset of data` correct??? -->
examine the structure of query patterns closer. In general, patterns can be thought of as different arrangements of
statement collections. TypeQL statements constitute the smallest building blocks of queries. Let's have a close
look at the constructs of a basic match clause.

![Statement structure](../../images/query/statement-structure.png)

- Each statement starts with a **variable** (`V`) providing a concept reference. We can reference both data and schema
  concepts via variables. A TypeQL variable is prefixed with a dollar sign `$`.

- The variable is followed by a comma-separated list of **properties** (`P1`, `P2`, `P3`) describing the concepts the
  variable refers to. Here we can see that all the concepts that variable `$p` refers to, must be of type `person`.
  The matched instances are expected to own an attribute of type `name` with the value of `"Bob"`. Additionally, we
  require the concepts to own an attribute of type `phone-number` with any value. We signal that we want to fetch the
  owned `phone-number`s as well by defining an extra `$phone` variable. Consequently, after performing a match on
  this statement, we should obtain pairs of concepts that satisfy our
  statement.

- We mark the end of the statement with a semi-colon `;`.

There is some freedom in forming and composing our statements. For example, as shown below, we could write our single statement with three properties as three combined statements.

<!-- test-ignore -->
```typeql
$p isa person;
$p has name 'Bob';
$p has phone-number $phone;
```

Consequently, we arrive at the subject of pattern composition. We already know that statements are the smallest building blocks, however, we have a number of possibilities for arranging them together. By doing so, we can express more complex pattern scenarios and their corresponding subgraphs. We allow the following ways to arrange statements together.

![Pattern structure](../../images/query/pattern-structure.png)

1. **Statement**: simplest possible arrangement - a single basic building block as [explained above](#Query pattern anatomy).
2. **Conjunction**: a set of patterns where to satisfy a match, **all** patterns must be matched. We form conjunctions by separating the partaking patterns with semi-colons `;`.
3. **Disjunction**: a set of patterns where to satisfy a match, **at least one** pattern must be matched. We form disjunctions by enclosing the partaking patterns within curly braces and interleaving them with the `or` keyword.
4. **Negation**: defines a conjunctive pattern that explicitly defines conditions **not** to be met. We form negations by defining the pattern of interest inside a `not {};` block.

To better illustrate the possibilities, we will now look at an example of an expressive pattern.

![Example pattern](../../images/query/example-pattern.png)

The pattern above describes pairs of instances of `person` who are married, went to the same `school` and are employed by the same `organisation`.
The pattern additionally specifies the employer to be either `Pharos` or `Cybersafe`, and the school to not be named `HCC`. Additionally the pattern
asks to fetch the `full-name` of each of the people in the pair.

The pattern is a conjunction of four different pattern types:
- **Conjunction 1** specifies the variables for people, school and organisation, specifies their types and asks for `full-name`s of people.
- **Disjunction** specifies that the companies of interest are either `Pharos` or `Cybersafe`.
- **Negation** specifies that we are not interested in the people who attended the school named `HCC`.
- **Conjunction 2** defines the pattern requiring the people to be in a `marriage` relationship, attend the same school via the `studentship` relationship, and
  work at the same organisation via the `employment` relationship.