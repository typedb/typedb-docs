# Code testing

## Writing tests

### For TypeQL

Here's a sample .adoc file illustrating the syntax for writing valid testable code.

```adoc
== Page Title
:test-tql: (linear | custom)
// When custom order is chosen you can specify an entrypoint:
[:test-tql-entry: <LABEL>] 

//!program[lang=tql, type=<TYPE>, [fail_at=<FAILURE>,] [count=<NUM>,] [name=<LABEL>,] [jump=<LABEL>,]]

Some text. Each 'code block' will be tested as a single query.

////
<Invisible query a.k.a. code block>
////

More text. Here's a simple visible block

//!++
[,typql]
----
<Visible query a.k.a. code block>
----
//!--

Yet more text. Invisible and visible code can be combined in the same block!

//!++
////
<Invisible part of query>
////
[,typql]
----
<Visiable part of query>
----
//!--

Words. words. words.

<more-code-blocks-as-needed>

Once we are done with our transaction:

//!run

Further transactions to follow:

<more-programs>
```
where
* `<TYPE>` can be `read, write, schema` 
* `<FAILURE>` can be `runtime, commit`
* `<NUM>` is an integer representing expected answer count
* `<LABEL>` is a label for the program (used for entrypoints and jumping around)
* A single program will be executed as a **single transaction** (with each code block being an individual query)

### For other languages

Same as for TypeQL, but with less configuration options for now:
```adoc
== Page Title
:test-rust: yes

Some Text

//!program[lang=rust]
...
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

The folder name (`code_test`) is the python module's name, so renaming the folder requires renaming `import` statements as well.
