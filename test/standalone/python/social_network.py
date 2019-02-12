import grakn
import csv
import phone_calls_csv_migration

from unittest import TestCase


class LoadPhoneCalls(TestCase):

    def setUpClass(self):

        with open('files/phone-calls/schema.gql', 'r') as schema:
            define_query = schema.read()

            client = grakn.Grakn(uri="localhost:48555")
            with client.session(keyspace="social_network") as session:
                with session.transaction(grakn.TxType.WRITE) as transaction:
                    transaction.query(define_query)
                    transaction.commit()

    def test_csv_migration(self):
        phone_calls_csv_migration.build_phone_call_graph()