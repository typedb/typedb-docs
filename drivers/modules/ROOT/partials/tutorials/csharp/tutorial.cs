// tag::code[]
// tag::import[]
using TypeDB.Driver;
using TypeDB.Driver.Api;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
// end::import[]

class TutorialProgram
{
// tag::constants[]
    const string DB_NAME = "sample_app_db";
    const string SERVER_ADDR = "127.0.0.1:1729";
    enum Edition { Core, Cloud }
    const Edition TYPEDB_EDITION = Edition.Core;
    const string CLOUD_USERNAME = "admin";
    const string CLOUD_PASSWORD = "password";
    // end::constants[]
    // tag::db-schema-setup[]
    static void DbSchemaSetup(ITypeDBSession session, string schemaFile = "iam-schema.tql") {
        string defineQuery;
        try
        {
            defineQuery = File.ReadAllText(schemaFile);
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                Console.WriteLine("Defining schema...");
                tx.Query.Define(defineQuery).Resolve();
                tx.Commit();
                Console.WriteLine("OK");
            }
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine("Error: File not found.");
            Environment.Exit(1);
        }
        catch (Exception e)
        {
            Console.WriteLine($"An error occurred: {e.Message}");
            Environment.Exit(1);
        }
    }
    // end::db-schema-setup[]
    // tag::db-dataset-setup[]
    static void DbDatasetSetup(ITypeDBSession session, string dataFile = "iam-data-single-query.tql") {
        string insertQuery = File.ReadAllText(dataFile);
        using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
            Console.WriteLine("Loading data...");
            IEnumerable<IConceptMap> response = tx.Query.Insert(insertQuery);
            int count = response.Count();
            tx.Commit();
            Console.WriteLine("OK");
        }
    }
    // end::db-dataset-setup[]
    // tag::create_new_db[]
    static bool CreateDatabase(ITypeDBDriver driver, string dbName) {
        Console.WriteLine("Creating a new database...");
        driver.Databases.Create(dbName);
        Console.WriteLine("OK");
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Schema)) {
            DbSchemaSetup(session);
        }
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            DbDatasetSetup(session);
        }
        return true;
    }
    // end::create_new_db[]
    // tag::replace_db[]
    static bool ReplaceDatabase(ITypeDBDriver driver, string dbName) {
        Console.WriteLine("Deleting an existing database...");
        driver.Databases.Get(dbName).Delete();
        Console.WriteLine("OK");
        return CreateDatabase(driver, dbName);
    }
    // end::replace_db[]
    // tag::test-db[]
    static bool DbCheck(ITypeDBSession session) {
        using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read)) {
            Console.WriteLine("Testing the database...");
            string testQuery = "match $u isa user; get $u; count;";
            long result = tx.Query.GetAggregate(testQuery).Resolve()!.AsLong();
            if (result == 3) {
                Console.WriteLine("Passed");
                return true;
            } else {
                Console.WriteLine($"Failed with the result: {result}\nExpected result: 3.");
                return false;
            }
        }
    }
    // end::test-db[]
    // tag::db-setup[]
    static bool DbSetup(ITypeDBDriver driver, string dbName, bool dbReset = false) {
        Console.WriteLine($"Setting up the database: {dbName}");
        if (driver.Databases.Contains(dbName)) {
            if (dbReset) {
                ReplaceDatabase(driver, dbName);
            } else {
                Console.Write("Found a pre-existing database. Do you want to replace it? (Y/N) ");
                ConsoleKeyInfo keyInfo = Console.ReadKey();
                Console.WriteLine();
                if (keyInfo.Key == ConsoleKey.Y)
                    {
                        ReplaceDatabase(driver, dbName);
                    }
                    else
                    {
                        Console.WriteLine("Reusing an existing database.");
                    }
            }
        } else {
            CreateDatabase(driver, dbName);
        }
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            return DbCheck(session);
        }
    }
    // end::db-setup[]
    // tag::fetch[]
    static List<JObject> FetchAllUsers(ITypeDBDriver driver, string dbName) {
        List<JObject> users = new();
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read)) {
                IEnumerable<JObject> queryResult = tx.Query.Fetch("match $u isa user; fetch $u: full-name, email;");
                int c = 1;
                foreach (JObject user in queryResult) {
                    users.Add(user);
                    Console.WriteLine($"User #{c++} ");
                    Console.WriteLine(JsonConvert.SerializeObject(user, Formatting.Indented));
                    Console.WriteLine();
                }
            }
        }
        return users;
    }
    // end::fetch[]
    // tag::insert[]
    static IEnumerable<IConceptMap> InsertNewUser(ITypeDBDriver driver, string dbName, string name, string email) {
        List<IConceptMap> response = new List<IConceptMap>();
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string query = $"insert $p isa person, has full-name '{name}', has email '{email}';";
                IEnumerable<IConceptMap> result = tx.Query.Insert(query);
                foreach (IConceptMap conceptMap in result) {
                    string retrievedName = conceptMap.Get("_0").AsAttribute().Value.AsString();
                    string retrievedEmail = conceptMap.Get("_1").AsAttribute().Value.AsString();
                    Console.WriteLine($"Added new user. Name: {retrievedName}, E-mail: {retrievedEmail}");
                }
                tx.Commit();
            }
        }
        return response;
    }
    // end::insert[]
    // tag::get[]
    static List<string> GetFilesByUser(ITypeDBDriver driver, string dbName, string name, bool inference = false) {
        TypeDBOptions options = new();
        options.Infer(inference);
        List<string> files = new List<string>();
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Read, options)) {
                string query = $"match $u isa user, has full-name '{name}'; get;";
                IEnumerable<IConceptMap> users = tx.Query.Get(query);
                int userCount = users.Count();
                if (userCount > 1) {
                    Console.WriteLine("Error: Found more than one user with that name.");
                } else if (userCount == 1) {
                    string fetchQuery = $@"
                        match
                        $fn == '{name}';
                        $u isa user, has full-name $fn;
                        $p($u, $pa) isa permission;
                        $o isa object, has path $fp;
                        $pa($o, $va) isa access;
                        $va isa action, has name 'view_file';
                        get $fp; sort $fp asc;";
                    IEnumerable<IConceptMap> response = tx.Query.Get(fetchQuery);
                    int resultCounter = 0;
                    foreach (IConceptMap cm in response) {
                        resultCounter++;
                        files.Add(cm.Get("fp").AsAttribute().Value.AsString());
                        Console.WriteLine($"File #{resultCounter}: {cm.Get("fp").AsAttribute().Value.AsString()}");
                    }
                    if (resultCounter == 0) {
                        Console.WriteLine("No files found. Try enabling inference.");
                    }
                } else {
                    Console.WriteLine("Error: No users found with that name.");
                }
            }
        }
        return files;
    }
    // end::get[]
    // tag::update[]
    static int UpdateFilePath(ITypeDBDriver driver, string dbName, string oldPath, string newPath) {
        int count = 0;
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string updateQuery = $@"
                    match
                    $f isa file, has path $old;
                    $old == '{oldPath}';
                    delete
                    $f has $old;
                    insert
                    $f has path '{newPath}';";
                List<IConceptMap> response = tx.Query.Update(updateQuery).ToList();
                count = response.Count();
                if (count > 0) {
                    tx.Commit();
                    Console.WriteLine($"Total number of paths updated: {count}.");
                } else {
                    Console.WriteLine("No matched paths: nothing to update.");
                }
            }
        }
        return count;
    }
    // end::update[]
    // tag::delete[]
    static bool DeleteFile(ITypeDBDriver driver, string dbName, string path) {
        using (ITypeDBSession session = driver.Session(dbName, SessionType.Data)) {
            using (ITypeDBTransaction tx = session.Transaction(TransactionType.Write)) {
                string matchQuery = $"match $f isa file, has path '{path}'; get;";
                IEnumerable<IConceptMap> response = tx.Query.Get(matchQuery);
                int count = response.Count();
                if (count == 1) {
                    tx.Query.Delete($"match $f isa file, has path '{path}'; delete $f isa file;").Resolve();
                    tx.Commit();
                    Console.WriteLine("The file has been deleted.");
                    return true;
                } else if (count > 1) {
                    Console.WriteLine("Matched more than one file with the same path.");
                    Console.WriteLine("No files were deleted.");
                    return false;
                } else {
                    Console.WriteLine("No files matched in the database.");
                    Console.WriteLine("No files were deleted.");
                    return false;
                }
            }
        }
    }
    // end::delete[]
    // tag::queries[]
    static void Queries(ITypeDBDriver driver, string dbName) {
        Console.WriteLine("\nRequest 1 of 6: Fetch all users as JSON objects with full names and emails");
        List<JObject> users = FetchAllUsers(driver, dbName);

        string newName = "Jack Keeper";
        string newEmail = "jk@typedb.com";
        Console.WriteLine("\nRequest 2 of 6: Add a new user with the full-name " + newName + " and email " + newEmail);
        InsertNewUser(driver, dbName, newName, newEmail);

        string name = "Kevin Morrison";
        Console.WriteLine("\nRequest 3 of 6: Find all files that the user " + name + " has access to view (no inference)");
        List<string> noFiles = GetFilesByUser(driver, dbName, name);

        Console.WriteLine("\nRequest 4 of 6: Find all files that the user " + name + " has access to view (with inference)");
        List<string> files = GetFilesByUser(driver, dbName, name, true);

        string oldPath = "lzfkn.java";
        string newPath = "lzfkn2.java";
        Console.WriteLine("\nRequest 5 of 6: Update the path of a file from " + oldPath + " to " + newPath);
        int updatedFiles = UpdateFilePath(driver, dbName, oldPath, newPath);

        string filePath = "lzfkn2.java";
        Console.WriteLine("\nRequest 6 of 6: Delete the file with path " + filePath);
        bool deleted = DeleteFile(driver, dbName, filePath);
    }
    // end::queries[]
    // tag::connection[]
    static ITypeDBDriver ConnectToTypeDB(Edition typedbEdition, string addr, string username = CLOUD_USERNAME, string password = CLOUD_PASSWORD, bool encryption = true) {
        switch (typedbEdition) {
            case Edition.Core:
                return TypeDB.Driver.Drivers.CoreDriver(addr);
            case Edition.Cloud:
                return TypeDB.Driver.Drivers.CloudDriver(addr, new TypeDBCredential(username, password, encryption));
            default:
                throw new InvalidOperationException("Invalid TypeDB edition specified.");
        }
    }
    // end::connection[]
    // tag::main[]
    static void Main(string[] args) {
        using (ITypeDBDriver driver = ConnectToTypeDB(TYPEDB_EDITION, SERVER_ADDR)) {
            if (driver.IsOpen()) {
                if (DbSetup(driver, DB_NAME)) {
                    Queries(driver, DB_NAME);
                    Environment.Exit(0);
                } else {
                    Console.Error.WriteLine("Failed to set up the database. Terminating...");
                    Environment.Exit(1);
                }
            } else {
                Console.Error.WriteLine("Failed to connect to TypeDB server. Terminating...");
                Environment.Exit(1);
            }
        }
    }
    // end::main[]
}
// end::code[]
