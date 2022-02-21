from typedb.client import *
import unittest


class PhoneCallsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('files/phone-calls/schema.tql', 'r') as schema:
            define_query = schema.read()

            with TypeDB.core_client('localhost:1729') as client:
                if "phone_calls" in client.databases().all():
                    client.databases().get("phone_calls").delete()
                client.databases().create("phone_calls")
                with client.session("phone_calls", SessionType.SCHEMA) as session:
                    with session.transaction(TransactionType.WRITE) as transaction:
                        transaction.query().define(define_query)
                        transaction.commit()
                        print("Loaded the phone_calls schema")

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


if __name__ == '__main__':
    unittest.main(verbosity=4)
