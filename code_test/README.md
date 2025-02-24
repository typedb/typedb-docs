# Code testing

## Writing tests

### For TypeQL

Here's a sample .adoc file illustrating the syntax for writing valid testable code.

```adoc
= Page Title
:test-typeql: (linear | custom)
[:test-typeql-entry: <LABEL>] 

Intro.

== First section

Text. 

[,typeql]
----
#!test[<TYPE>[, reset] [, rollback] [, fail_at=<FAILURE>] [, count=<NUM>] [, jump=<LABEL>] [, name=<LABEL>]]
#{{
<HIDDEN-QUERY>
#}}
#{{
<HIDDEN-QUERY>
#}}
#!test[<TYPE>, ...]
#{{
<HIDDEN-QUERY>
#}}
<VISIBLE-QUERY>
#!test[<TYPE>, ...]
<VISIBLE-QUERY>
#!---
<VISIBLE-QUERY>
----

More text.
```

where
* Tests represent individual transactions (we commit/close at the end of each test)
* `<TYPE>` can be `read, write, schema` 
* `reset` resets the database before running the test
* `rollback` rolls backs the transaction instead of committing it
* `fail_at=<FAILURE>` can be `runtime, commit`
* `count=<NUM>` is an integer representing expected answer count
* `name=<LABEL>` names the test
* `jump=<LABEL>` is a label for the test (used for entrypoints and jumping around)
* A single test will be executed as a **single transaction** (with each code block being an individual query)

### For other languages

Same as for TypeQL, but with less configuration options for now:
```adoc
== Page Title
:test-rust: yes

Some Text

[,rust]
----
//!test[lang=rust]
//{{
<HIDDEN-CODE-SEGMENT>
//}}
<VISIBLE-CODE-SEGMENT>
----

More text.
```

NOTE: Entrypoints and jumping around isn't supported for languages other than TypeQL

### Examples

See examples in `./tests/` for how to write testable examples in `.adoc` files.

## Running tests

### Multi-file run

```bash
python -m code_test.main <lang>     
```

### Single file run

```bash
python -m code_test.main <lang> <file-name>    
```

## Development

### Type checking

Type check with `mypy code_test/main.py` (need to install `mypy`)

### Modules

The folder name (`code_test`) is the python module's name, so renaming the folder requires renaming `import` statements in the code as well (IntelliJ's refactoring might be able to handle it).
