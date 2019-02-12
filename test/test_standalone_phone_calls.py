import grakn
import csv

from unittest import TestCase


class LoadPhoneCalls(TestCase):

    @classmethod
    def main(cls):

        with open('files/phone-calls/schema.gql', 'r') as schema:
            define_query = schema.read()

            client = grakn.Grakn(uri="localhost:48555")
            with client.session(keyspace="phone_calls") as session:
                with session.transaction(grakn.TxType.WRITE) as transaction:
                    transaction.query(define_query)
                    transaction.commit()
