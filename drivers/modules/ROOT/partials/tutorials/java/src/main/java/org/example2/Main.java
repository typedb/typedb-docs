package org.example2;
// tag::code[]
// tag::import[]

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

// end::import[]
// tag::class-main[]
public class Main {
    // tag::constants[]
    private static final String DB_NAME = "sample_app_db";
    private static final String SERVER_ADDR = "127.0.0.1:1729";

    private static final String USERNAME = "admin";
    private static final String PASSWORD = "password";

    // end::constants[]
    // tag::main[]
    public static void main(String[] args) {
        try (Driver driver = driverConnect(SERVER_ADDR, USERNAME, PASSWORD)) {
            if (dbSetup(driver, DB_NAME, false)) {
                System.out.println("Setup complete.");
                queries(driver, DB_NAME);
            } else {
                System.out.println("Setup failed.");
            }
        } catch (TypeDBDriverException e) {
            e.printStackTrace();
        }
    }

    // end::main[]
    // tag::queries[]
    private static void queries(Driver driver, String dbName) throws TypeDBDriverException {
        System.out.println("Request 1 of 6: Fetch all users as JSON objects with emails and phone numbers");
        List<JSON> users = fetchAllUsers(driver, dbName);

        String new_user_phone = "17778889999";
        String new_user_email = "k.koolidge@typedb.com";
        String new_user_username = "k-koolidge";
        System.out.printf("Request 2 of 6: Add a new user with the email '%s' and phone '%s'\n", new_user_email, new_user_phone);
        List<ConceptRow> newUsers = insertNewUser(driver, dbName, new_user_email, new_user_phone, new_user_username);

        String kevinEmail = "kevin.morrison@typedb.com";
        System.out.printf("Request 3 of 6: Find direct relatives of a user with email %s\n", kevinEmail);
        List<ConceptRow> directRelatives = getDirectRelativesByEmail(driver, dbName, kevinEmail);

        System.out.printf("Request 4 of 6: Transitively find all relatives of a user with email %s\n", kevinEmail);
        List<ConceptRow> allRelatives = getAllRelativesByEmail(driver, dbName, kevinEmail);

        String oldKevinPhone = "110000000";
        String newKevinPhone = "110000002";
        System.out.printf("Request 5 of 6: Update the phone of a of user with email %s from %s to %s\n", kevinEmail, oldKevinPhone, newKevinPhone);
        List<ConceptRow> updatedUsers = updatePhoneByEmail(driver, dbName, kevinEmail, oldKevinPhone, newKevinPhone);

        System.out.printf("Request 6 of 6: Delete the user with email \"%s\"%n", new_user_email);
        deleteUserByEmail(driver, dbName, new_user_email);
    }

    // end::queries[]
    // tag::connection[]
    private static Driver driverConnect(String uri, String username, String password) throws TypeDBDriverException {
        // tag::driver_new[]
        Driver driver = TypeDB.driver(uri, new Credentials(username, password), new DriverOptions(false, null));
        // end::driver_new[]
        return driver;
    }
    // end::connection[]

    // tag::fetch[]
    private static List<JSON> fetchAllUsers(Driver driver, String dbName) throws TypeDBDriverException {
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.READ)) {
            String query = "match $u isa user; fetch { 'phone': $u.phone, 'email': $u.email };";
            List<JSON> answers = tx.query(query).resolve().asConceptDocuments().stream().collect(Collectors.toList());
            answers.forEach(json -> System.out.println("JSON: " + json.toString()));
            return answers;
        }
    }

    // end::fetch[]
    // tag::insert[]
    public static List<ConceptRow> insertNewUser(Driver driver, String dbName, String newEmail, String newPhone, String newUsername) throws TypeDBDriverException {
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.WRITE)) {
            String query = String.format(
                    "insert $u isa user, has $e, has $p, has $username; $e isa email '%s'; $p isa phone '%s'; $username isa username '%s';",
                    newEmail, newPhone, newUsername
            );
            List<ConceptRow> answers = tx.query(query).resolve().asConceptRows().stream().collect(Collectors.toList());
            tx.commit();
            for (ConceptRow row : answers) {
                String phone = row.get("p").get().tryGetString().get();
                String email = row.get("e").get().tryGetString().get();
                System.out.println("Added new user. Phone: " + phone + ", E-mail: " + email);
            }
            return answers;
        }
    }

    // end::insert[]
    // tag::match[]
    public static List<ConceptRow> getDirectRelativesByEmail(Driver driver, String dbName, String email) throws TypeDBDriverException {
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.READ)) {
            List<ConceptRow> users = tx.query(String.format("match $u isa user, has email '%s';", email)).resolve().asConceptRows()
                    .stream().collect(Collectors.toList());
            if (users.size() != 1) {
                System.out.printf("Error: Found %d users with email %s, expected 1", users.size(), email);
                return null;
            } else {
                String relativesQuery = String.format(
                        "match " +
                                "$e == '%s';" +
                                "$u isa user, has email $e;" +
                                "$family isa family ($u, $relative);" +
                                "$relative has username $username;" +
                                "not { $u is $relative; };" +
                                "select $username;" +
                                "sort $username asc;",
                        email
                );
                List<ConceptRow> rows = tx.query(relativesQuery).resolve().asConceptRows().stream().collect(Collectors.toList());
                rows.forEach(row -> System.out.println("Relative: " + row.get("username").get().tryGetString().get()));
                return rows;
            }
        }
    }

    // end::match[]
    // tag::match-function[]
    public static List<ConceptRow> getAllRelativesByEmail(Driver driver, String dbName, String email) throws TypeDBDriverException {
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.READ)) {
            List<ConceptRow> users = tx.query(String.format("match $u isa user, has email '%s';", email)).resolve().asConceptRows()
                    .stream().collect(Collectors.toList());
            if (users.size() != 1) {
                System.out.printf("Error: Found %d users with email %s, expected 1", users.size(), email);
                return null;
            } else {
                String relativesQuery = String.format(
                        "match " +
                                "$u isa user, has email $e;" +
                                "$e == '%s';" +
                                "let $relative in all_relatives($u);" +
                                "not { $u is $relative; };" +
                                "$relative has username $username;" +
                                "select $username;" +
                                "sort $username asc;",
                        email
                );
                List<ConceptRow> rows = tx.query(relativesQuery).resolve().asConceptRows().stream().collect(Collectors.toList());
                rows.forEach(row -> System.out.println("Relative: " + row.get("username").get().tryGetString().get()));
                return rows;
            }
        }
    }

    // end::match-function[]
    // tag::update[]
    public static List<ConceptRow> updatePhoneByEmail(Driver driver, String dbName, String email, String oldPhone, String newPhone) throws TypeDBDriverException {
        List<ConceptRow> rows = new ArrayList<>();
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.WRITE)) {
            String query = String.format(
                    "match $u isa user, has email '%s', has phone $phone; $phone == '%s';" +
                            "update $u has phone '%s';",
                    email, oldPhone, newPhone);
            rows = tx.query(query).resolve().asConceptRows().stream().collect(Collectors.toList());
            tx.commit();
            System.out.printf("Total number of phones updated: %d%n", rows.size());
        }
        return rows;
    }

    // end::update[]
    // tag::delete[]
    public static void deleteUserByEmail(Driver driver, String dbName, String email) throws TypeDBDriverException {
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.WRITE)) {
            String query = String.format("match $u isa user, has email '%s'; delete $u;", email);
            List<ConceptRow> rows = tx.query(query).resolve().asConceptRows().stream().collect(Collectors.toList());
            tx.commit();
            System.out.printf("Deleted %d users", rows.size());
        }
    }

    // end::delete[]
    // tag::db-setup[]
    private static boolean dbSetup(Driver driver, String dbName, boolean dbReset) throws TypeDBDriverException {
        System.out.println("Setting up the database: " + dbName);
        if (driver.databases().contains(dbName)) {
            if (dbReset) {
                if (!replaceDatabase(driver, dbName)) {
                    return false;
                }
            } else {
                System.out.println("Found a pre-existing database. Do you want to replace it? (Y/N) ");
                String answer;
                try {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
                    answer = reader.readLine();
                } catch (IOException e) {
                    throw new RuntimeException("Failed to read user input.", e);
                }
                if (answer.equalsIgnoreCase("y")) {
                    if (!replaceDatabase(driver, dbName)) {
                        return false;
                    }
                } else {
                    System.out.println("Reusing an existing database.");
                }
            }
        } else { // No such database found on the server
            if (!createDatabase(driver, dbName)) {
                System.out.println("Failed to create a new database. Terminating...");
                return false;
            }
        }
        if (driver.databases().contains(dbName)) {
            return validateData(driver, dbName);
        } else {
            System.out.println("Database not found. Terminating...");
            return false;
        }
    }

    // end::db-setup[]
    // tag::create_new_db[]
    private static boolean createDatabase(Driver driver, String dbName) throws TypeDBDriverException {
        System.out.print("Creating a new database...");
        driver.databases().create(dbName);
        System.out.println("OK");
        dbSchemaSetup(driver, dbName);
        dbDatasetSetup(driver, dbName);
        return true;
    }

    // end::create_new_db[]
    // tag::replace_db[]
    private static boolean replaceDatabase(Driver driver, String dbName) throws TypeDBDriverException {
        System.out.print("Deleting an existing database...");
        driver.databases().get(dbName).delete();  // Delete the database if it exists already
        System.out.println("OK");
        if (createDatabase(driver, dbName)) {
            return true;
        } else {
            System.out.println("Failed to create a new database. Terminating...");
            return false;
        }
    }

    // end::replace_db[]
    // tag::db-schema-setup[]
    private static void dbSchemaSetup(Driver driver, String dbName) throws TypeDBDriverException {
        String schemaFile = "schema.tql";
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.SCHEMA)) {
            String defineQuery = new String(Files.readAllBytes(Paths.get(schemaFile)));
            System.out.print("Defining schema...");
            tx.query(defineQuery).resolve();
            tx.commit();
            System.out.println("OK");
        } catch (IOException e) {
            throw new RuntimeException("Failed to read the schema file.", e);
        }
    }

    // end::db-schema-setup[]
    // tag::db-dataset-setup[]
    private static void dbDatasetSetup(Driver driver, String dbName) throws TypeDBDriverException {
        String dataFile = "data_small_single_query.tql";
        try (Transaction tx = driver.transaction(dbName, Transaction.Type.WRITE)) {
            String insertQuery = new String(Files.readAllBytes(Paths.get(dataFile)));
            System.out.print("Loading data...");
            tx.query(insertQuery).resolve();
            tx.commit();
            System.out.println("OK");
        } catch (IOException e) {
            throw new RuntimeException("Failed to read the data file.", e);
        }
    }

    // end::db-dataset-setup[]
    // tag::validate-db[]
    private static boolean validateData(Driver driver, String dbName) throws TypeDBDriverException {
        try (Transaction transaction = driver.transaction(dbName, Transaction.Type.READ)) {
            String countQuery = "match $u isa user; reduce $count = count;";
            System.out.print("Validating the dataset...");
            long count = transaction.query(countQuery).resolve().asConceptRows().next().get("count").get().tryGetInteger().get();
            if (count == 3) {
                System.out.println("Passed");
                return true;
            } else {
                System.out.printf("Validation failed, unexpected number of users: %d. Terminating...\n", count);
                return false;
            }
        }
    }
    // end::validate-db[]
}
// end::class-main[]
// end::code[]
