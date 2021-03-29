from grakn.client import *
import unittest


class SocialNetworkTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('files/social-network/schema.gql', 'r') as schema:
            define_query = schema.read()

            with Grakn.core_client() as client:
                if "social_network" in client.databases().all():
                    client.databases().get("social_network").delete()
                client.databases().create("social_network")
                with client.session("social_network", SessionType.SCHEMA) as session:
                    with session.transaction(TransactionType.WRITE) as transaction:
                        transaction.query().define(define_query)
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


if __name__ == '__main__':
    unittest.main(verbosity=4)
