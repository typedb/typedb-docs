import grakn
import unittest


class TestStandaloneSocialNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('files/social-network/schema.gql', 'r') as schema:
            define_query = schema.read()

            client = grakn.Grakn(uri="localhost:48555")
            with client.session("social_network") as session:
                with session.transaction(grakn.TxType.WRITE) as transaction:
                    transaction.query(define_query)
                    transaction.commit()
                    print("Loaded the social_network schema")

    def test_social_network_quickstart_query(self):
        import social_network_quickstart_query

    def test_social_network_python_client_a(self):
        import social_network_python_client_a

    def test_social_network_python_client_b(self):
        import social_network_python_client_b

    def test_social_network_python_client_c(self):
        import social_network_python_client_c

    def test_social_network_python_client_d(self):
        import social_network_python_client_d

    @classmethod
    def tearDownClass(cls):
        client = grakn.Grakn(uri="localhost:48555")
        client.keyspaces().delete("social_network")
        print("Deleted the social_network keyspace")


if __name__ == '__main__':
    unittest.main()
