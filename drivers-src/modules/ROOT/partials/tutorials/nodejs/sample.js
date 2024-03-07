// tag::code[]
// tag::import[]
const { TypeDB } = require("typedb-driver/TypeDB");
const { SessionType } = require("typedb-driver/api/connection/TypeDBSession");
const { TransactionType } = require("typedb-driver/api/connection/TypeDBTransaction");
const { TypeDBOptions } = require("typedb-driver/api/connection/TypeDBOptions");
const { readFile } = require('fs/promises')
const prompt = require('prompt-sync')();
// end::import[]
// tag::constants[]
const DB_NAME = "sample_app_db";
const SERVER_ADDR = "127.0.0.1:1729";
let dbReset = false;
let typedbEdition = "core"; // "cloud"
const CLOUD_USERNAME = "admin";
const CLOUD_PASSWORD = "password";
// end::constants[]
// tag::main[]
async function main() {
    try {
        const driver = await connectToTypedb(typedbEdition, SERVER_ADDR);
        let setup = await dbSetup(driver, DB_NAME, dbReset);
        if (setup) {
            await queries(driver, DB_NAME);
        } else {
            console.log("Terminating...");
            process.exit(1);
        }
    } catch (error) {
        console.error(error);
    }
    process.exit();
};
// end::main[]
// tag::connection[]
async function connectToTypedb(edition, addr, username = CLOUD_USERNAME, password = CLOUD_PASSWORD) {
    if (edition == "core") {
        return await TypeDB.coreDriver(addr);
    }
    if (edition == "cloud") {
        return await TypeDB.cloudDriver(addr, new TypeDBCredential(username, password));
    }
}
// end::connection[]
// tag::queries[]
async function queries(driver, dbName) {
    console.log("\nRequest 1 of 6: Fetch all users as JSON objects with full names and emails");
    let users = await fetchAllUsers(driver, dbName);

    let new_name = "Jack Keeper";
    let new_email = "jk@vaticle.com";
    console.log(`\nRequest 2 of 6: Add a new user with the full-name ${new_name} and email ${new_email}`);
    await insertNewUser(driver, dbName, new_name, new_email);

    let name = "Kevin Morrison";
    console.log(`\nRequest 3 of 6: Find all files that the user ${name} has access to view (no inference)`);
    let noFiles = await getFilesByUser(driver, dbName, name);

    console.log(`\nRequest 4 of 6: Find all files that the user ${name} has access to view (with inference)`);
    let files = await getFilesByUser(driver, dbName, name, inference=true);

    old_path = "lzfkn.java";
    new_path = "lzfkn2.java";
    console.log(`\nRequest 5 of 6: Update the path of a file from ${old_path} to ${new_path}`);
    let updated_files = await updateFilepath(driver, dbName, old_path, new_path);

    path = "lzfkn2.java";
    console.log(`\nRequest 6 of 6: Delete the file with path ${path}`);
    let deleted = await delete_file(driver, dbName, path);
}
// end::queries[]
// tag::fetch[]
async function fetchAllUsers(driver, dbName) {
    let dataSession = await driver.session(dbName, SessionType.DATA);
    let users;
    try {
        tx = await dataSession.transaction(TransactionType.READ);
        try {
            users = await tx.query.fetch("match $u isa user; fetch $u: full-name, email;").collect();
            for (let i = 0; i < users.length; i++) {
                console.log("User #" + (i + 1).toString() + ": " + users[i]["u"]["full-name"][0]["value"]);
            }
        }
        catch (error) { console.error(error); }
        finally { if (tx.isOpen()) {await tx.close()}; };
    }
    catch (error) { console.error(error); }
    finally { await dataSession?.close(); };
    return users;
}
// end::fetch[]
// tag::insert[]
async function insertNewUser(driver, dbName, name, email) {
    let result;
    let dataSession = await driver.session(dbName, SessionType.DATA);
    try {
        tx = await dataSession.transaction(TransactionType.WRITE);
        try {
            let response = await tx.query.insert(`insert $p isa person, has full-name $fn, has email $e; $fn == '${name}'; $e == '${email}';`);
            let answers = await response.collect();
            result = await Promise.all(
                answers.map(answer =>
                    [answer.get("fn").value,
                    answer.get("e").value]
                )
            );
            for(let i = 0; i < result.length; i++) {
                console.log("User inserted: " + result[i][0] + ", has E-mail: " + result[i][1]);
            };
            await tx.commit();
        }
        catch (error) { console.error(error); }
        finally { if (tx.isOpen()) {await tx.close()}; };
    }
    catch (error) { console.error(error); }
    finally { await dataSession?.close(); };
    return result;
}
// end::insert[]
// tag::get[]
async function getFilesByUser(driver, dbName, name, inference=false) {
    let options = new TypeDBOptions();
    options.infer = inference;
    let dataSession = await driver.session(dbName, SessionType.DATA);
    let users;
    try {
        tx = await dataSession.transaction(TransactionType.READ, options);
        try {
            users = await tx.query.get(`match $u isa user, has full-name '${name}'; get;`).collect();
            if (users.length > 1) {
                console.log("Error: Found more than one user with that name.");
                return null;
            } else if (users.length == 1) {
                let response = tx.query.get(`match
                                            $fn == '${name}';
                                            $u isa user, has full-name $fn;
                                            $p($u, $pa) isa permission;
                                            $o isa object, has path $fp;
                                            $pa($o, $va) isa access;
                                            $va isa action, has name 'view_file';
                                            get $fp; sort $fp asc;
                                            `);
                answers = await response.collect();
                result = await Promise.all(
                    answers.map(answer =>
                        [answer.get("fp").value]
                    )
                );
                for (let i = 0; i < result.length; i++) {
                    console.log("File #" + (i + 1).toString() + ": " + result[i]);
                }
                if (answers.length == 0) {
                    console.log("No files found. Try enabling inference.");
                return answers
                }
            } else {
                console.log("Error: No users found with that name.");
                return null;
            }
        }
        catch (error) { console.error(error); }
        finally { if (tx.isOpen()) {await tx.close()}; };
    }
    catch (error) { console.error(error); }
    finally { await dataSession?.close(); };
    return users;
}
// end::get[]
// tag::update[]
async function updateFilepath(driver, dbName, oldPath, newPath) {
    let dataSession = await driver.session(dbName, SessionType.DATA);
    try {
        tx = await dataSession.transaction(TransactionType.WRITE);
        try {
            let response = await tx.query.update(`
                                                match
                                                $f isa file, has path $old_path;
                                                $old_path = '${oldPath}';
                                                delete
                                                $f has $old_path;
                                                insert
                                                $f has path $new_path;
                                                $new_path = '${newPath}';
                                                `).collect();
            if (response.length > 0) {
                await tx.commit();
                console.log(`Total number of paths updated: ${response.length}.`);
                return response;
            } else {
                console.log("No matched paths: nothing to update.");
                return null;
            }
        }
        catch (error) { console.error(error); }
        finally { if (tx.isOpen()) {await tx.close()}; };
    }
    catch (error) { console.error(error); }
    finally { await dataSession?.close(); };
}
// end::update[]
// tag::delete[]
async function delete_file(driver, dbName, path) {
    let dataSession = await driver.session(dbName, SessionType.DATA);
    try {
        tx = await dataSession.transaction(TransactionType.WRITE);
        try {
            let response = await tx.query.get(`match
                                                $f isa file, has path '${path}';
                                                get;`).collect();
            if (response.length == 1) {
                await tx.query.delete(`
                                    match
                                    $f isa file, has path '${path}';
                                    delete
                                    $f isa file;
                                    `);
                await tx.commit();
                console.log("The file has been deleted.");
                return true;
            } else if (response.length > 1) {
                console.log("Matched more than one file with the same path.");
                console.log("No files were deleted.");
                await tx.close();
                return false;
            } else {
                console.log(response.length)
                console.log("No files matched in the database.");
                console.log("No files were deleted.");
                await tx.close();
                return false;
            }
        }
        catch (error) { console.error(error); }
        finally { if (tx.isOpen()) {await tx.close()}; };
    }
    catch (error) { console.error(error); }
    finally { await dataSession?.close(); };
}
// end::delete[]
// tag::db-setup[]
async function dbSetup(driver, dbName, dbReset=false) {
    console.log(`Setting up the database: ${dbName}`);
    let isNew = await tryCreateDatabase(driver, dbName, dbReset);
    if (!driver.databases.contains(dbName)) {
        console.log("Database creation failed. Terminating...");
        return false;
    }
    if (isNew) {
        try {
            let session = await driver.session(dbName, SessionType.SCHEMA);
            await dbSchemaSetup(session);
            await session.close();
            session = await driver.session(dbName, SessionType.DATA);
            await dbDatasetSetup(session);
            await session.close();
        } catch (error) { console.error(error); };
    }
    try {
        let session = await driver.session(dbName, SessionType.DATA);
        let result = await testInitialDatabase(session)
        await session.close();
        return result
    } catch (error) { console.error(error); };
}
// end::db-setup[]
// tag::db-schema-setup[]
async function dbSchemaSetup(schemaSession) {
    process.stdout.write("Defining schema...");
    try {
        tx = await schemaSession.transaction(TransactionType.WRITE);
        try {
            const define_query = await readFile("iam-schema.tql", 'utf8');
            await tx.query.define(define_query);
            await tx.commit();
            console.log("OK");
            return true;
        }
        catch (e) {
            callback(e);
            return false;
        }
    }
    catch (e) {
        callback(e);
        return false;
    }
    finally { if (tx.isOpen()) {await tx.close()}; }
}
// end::db-schema-setup[]
// tag::db-dataset-setup[]
async function dbDatasetSetup(dataSession) {
    process.stdout.write("Loading data...");
    try {
        tx = await dataSession.transaction(TransactionType.WRITE);
        try {
            const insert_query = await readFile("iam-data-single-query.tql", 'utf8');
            await tx.query.insert(insert_query);
            await tx.commit();
            console.log("OK");
        }
        catch (e) { callback(e); }
    }
    catch (e) { callback(e); }
    finally { if (tx.isOpen()) {await tx.close()}; }
}
// end::db-dataset-setup[]
// tag::test-db[]
async function testInitialDatabase(dataSession) {
    process.stdout.write("Testing the database...");
    try {
        tx = await dataSession.transaction(TransactionType.READ);
        try {
            const test_query = "match $u isa user; get $u; count;";
            let response = await tx.query.getAggregate(test_query);
            let result = await response.asValue().asLong();
            if (result == 3) {
                console.log("Passed");
                return true;
            } else {
                console.log("Failed with the result: " + result.toString() + " Expected result: 3");
                return false;
            }
        }
        catch (e) { callback(e); }
    }
    catch (e) { callback(e); }
    finally { if (tx.isOpen()) {await tx.close()}; }
}
// end::test-db[]
// tag::create_new_db[]
async function tryCreateDatabase(driver, dbName, reset=false) {
    try {
        if (await driver.databases.contains(dbName)) {
            if (reset) {
                process.stdout.write("Replacing an existing database...");
                await (await driver.databases.get(dbName)).delete();
                await driver.databases.create(dbName);
                console.log("OK");
                return true;
            } else { // reset = false
                const input = prompt("Found a pre-existing database. Do you want to replace it? (Y/N) ");
                if (input.toLowerCase() == "y") {
                    return await tryCreateDatabase(driver, dbName, true);
                } else {
                    console.log("Reusing an existing database.");
                    return false;
                }
            }
        } else { // No such database on the server
            process.stdout.write("Creating a new database...");
            await driver.databases.create(dbName);
            console.log("");
            return true;
        }
    }
    catch (e) {
        callback(e);
        return false;
    }
}
// end::create_new_db[]
main();
