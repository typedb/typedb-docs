import grakn
import unittest

class TestStandalonePhoneCalls(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('files/phone-calls/schema.gql', 'r') as schema:
            define_query = schema.read()

            client = grakn.Grakn(uri="localhost:48555")
            with client.session(keyspace="phone_calls") as session:
                with session.transaction(grakn.TxType.WRITE) as transaction:
                    transaction.query(define_query)
                    transaction.commit()

    def test_a_phone_calls_first_query(self):
        import phone_calls_first_query

    def test_b_phone_calls_second_query(self):
        import phone_calls_second_query

    def test_c_phone_calls_third_query(self):
        import phone_calls_third_query

    def test_d_phone_calls_forth_query(self):
        import phone_calls_forth_query

    def test_e_phone_calls_fifth_query(self):
        import phone_calls_fifth_query

    def test_f_phone_calls_csv_migration(self):
        import phone_calls_csv_migration

    def test_g_phone_calls_json_migration(self):
        import phone_calls_json_migration

    def test_h_phone_calls_xml_migration(self):
        import phone_calls_xml_migration

    @classmethod
    def tearDown(cls):
        client = grakn.Grakn(uri="localhost:48555")
        with client.session(keyspace="phone_calls") as session:
            with session.transaction(grakn.TxType.WRITE) as transaction:
                transaction.query("match $x isa relationship; delete $x;")
                transaction.query("match $x isa entity; delete $x;")
                transaction.query("match $x isa attribute; delete $x;")
                transaction.commit()

if __name__ == '__main__':
    unittest.main()
