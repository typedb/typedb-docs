#tag::analyze[]
with driver.transaction(DB_NAME, TransactionType.READ) as tx:
    # 1. Send the analyze request
    promise = tx.analyze("""
        match { $x isa user; } or { $x isa company; };
        fetch { "email": [$x.email] };
    """)

    # 2. Resolve the promise if you want to access the result or receive an error as an exception
    analyzed = promise.resolve()
#end::analyze[]
