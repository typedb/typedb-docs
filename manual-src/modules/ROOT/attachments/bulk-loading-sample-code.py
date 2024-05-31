# tag::imports[]
import os
from collections.abc import Iterator
from multiprocessing import Queue, Manager, Pool
from typedb.api.connection.credential import TypeDBCredential
from typedb.api.connection.session import TypeDBSession, SessionType
from typedb.api.connection.transaction import TransactionType
from typedb.driver import TypeDB
# end::imports[]


# tag::def_queries[]
def query_iterator(file_paths: list[str]) -> Iterator[str]:
    for path in file_paths:
        with open(path, "r") as file:
            for line in file:
                yield line
# end::def_queries[]


# tag::def_batches[]
def batch_iterator(file_paths: list[str], batch_size: int) -> Iterator[list[str]]:
    next_batch: list[str] = list()

    for query in query_iterator(file_paths):
        next_batch.append(query)

        if len(next_batch) >= batch_size:
            yield next_batch
            next_batch: list[str] = list()

    if len(next_batch) > 0:
        yield next_batch
# end::def_batches[]


# tag::def_load_batch[]
def load_batch(session: TypeDBSession, batch: list[str]) -> None:
    with session.transaction(TransactionType.WRITE) as transaction:
        for query in batch:
            transaction.query.insert(query)

        transaction.commit()
# end::def_load_batch[]


# tag::def_load_data[]
def load_data(addresses: str | list[str], username: str, password: str) -> None:
    database = "bookstore"
    data_files = ["contributors.tql", "publishers.tql", "books.tql"]
    batch_size = 100
    credential = TypeDBCredential(username, password, tls_enabled=True)

    with TypeDB.cloud_driver(addresses, credential) as driver:
        with driver.session(database, SessionType.DATA) as session:
            for batch in batch_iterator(data_files, batch_size):
                load_batch(session, batch)
# end::def_load_data[]


# tag::def_batch_loader[]
def batch_loader(
    queue: Queue,
    addresses: str | list[str],
    username: str,
    password: str,
    database: str
) -> None:
    credential = TypeDBCredential(username, password, tls_enabled=True)

    with TypeDB.cloud_driver(addresses, credential) as driver:
        with driver.session(database, SessionType.DATA) as session:
            while True:
                batch: list[str] | None = queue.get()

                if batch is None:
                    break
                else:
                    with session.transaction(TransactionType.WRITE) as transaction:
                        for query in batch:
                            transaction.query.insert(query)

                        transaction.commit()
# end::def_batch_loader[]


# tag::def_load_data_async[]
def load_data_async(addresses: str | list[str], username: str, password: str) -> None:
    database = "bookstore"
    data_files = ["contributors.tql", "publishers.tql", "books.tql"]
    batch_size = 100

    for data_file in data_files:
        with Manager() as manager:
            pool_size = os.cpu_count()
            pool = Pool(pool_size)
            queue = manager.Queue(4 * pool_size)

            kwargs = {
                "queue": queue,
                "addresses": addresses,
                "username": username,
                "password": password,
                "database": database,
            }

            for _ in range(pool_size):
                pool.apply_async(batch_loader, kwds=kwargs)

            for batch in batch_iterator([data_file], batch_size):
                queue.put(batch)

            for _ in range(pool_size):
                queue.put(None)  # Sentinel value

            pool.close()
            pool.join()
# end::def_load_data_async[]
