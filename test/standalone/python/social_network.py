import grakn
import unittest

class TestStandaloneSocialNetwork(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('files/social-network/schema.gql', 'r') as schema:
            define_query = schema.read()

            client = grakn.Grakn(uri="localhost:48555")
            with client.session(keyspace="social_network") as session:
                with session.transaction(grakn.TxType.WRITE) as transaction:
                    transaction.query(define_query)
                    transaction.commit()

    def test_social_network_query(self):
        import social_network_query


if __name__ == '__main__':
    unittest.main()