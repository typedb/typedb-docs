from grakn.client import GraknClient
import unittest


class SocialNetworkTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('files/social-network/schema.gql', 'r') as schema:
            define_query = schema.read()

            with GraknClient(uri="localhost:1729") as client:
                with client.session("social_network") as session:
                    with session.transaction().write() as transaction:
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

    def test_social_network_create_new_client_a(self):
        import social_network_create_new_client_a

    def test_social_network_create_new_client_b(self):
        import social_network_create_new_client_b


    @classmethod
    def tearDownClass(cls):
        with GraknClient(uri="localhost:1729") as client:
            client.databases().delete("social_network")
            print("Deleted the social_network database")


if __name__ == '__main__':
    unittest.main()
