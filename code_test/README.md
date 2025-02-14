# Code testing

## Writing tests

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
