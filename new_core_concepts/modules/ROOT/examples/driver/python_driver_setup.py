#tag::import_and_constants[]
#tag::import[]
from typedb.driver import *
#end::import[]

#tag::constants[]
#tag::constants_db_name[]
DB_NAME = "my_database"
#end::constants_db_name[]
#tag::constants_address[]
address = "localhost:1729"
#end::constants_address[]
#tag::constants_credentials[]
credentials = Credentials("admin", "password")
#end::constants_credentials[]
#tag::constants_options[]
options = DriverOptions(is_tls_enabled=True, tls_root_ca_path=None)
#end::constants_options[]
#end::constants[]
#end::import_and_constants[]

#tag::driver_create[]
with TypeDB.driver(address, credentials, options) as driver:
#end::driver_create[]
#tag::database_create[]
    try:
        # may error if the database already exists
        driver.databases.create(DB_NAME)
    finally:
#end::database_create[]
        pass
