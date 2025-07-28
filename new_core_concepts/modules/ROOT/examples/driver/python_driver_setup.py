#tag::import[]
from typedb.driver import *
#end::import[]

#tag::constants[]
DB_NAME = "my_database"
address = "localhost:1729"
credentials = Credentials("admin", "password")
options = DriverOptions(is_tls_enabled=True, tls_root_ca_path=None)
#end::constants[]

#tag::database_create[]
with TypeDB.driver(address, credentials, options) as driver:
    # 2. Initialize database with a schema  during application startup
    try:
        # may error if the database already exists
        driver.databases.create(DB_NAME)
    finally:
#end::database_create[]
        pass
