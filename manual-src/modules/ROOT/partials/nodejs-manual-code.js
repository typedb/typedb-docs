// tag::import[]
const { TypeDB } = require("typedb-driver/TypeDB");
const { SessionType } = require("typedb-driver/api/connection/TypeDBSession");
const { TransactionType } = require("typedb-driver/api/connection/TypeDBTransaction");
const { TypeDBOptions } = require("typedb-driver/api/connection/TypeDBOptions");
// end::import[]
async function main() {
    const DB_NAME = "sample_db";

    console.log("TypeDB Manual sample code");
    // tag::driver[]
    const driver = await TypeDB.coreDriver("127.0.0.1:1729");
    // end::driver[]
    // tag::list-db[]
    let dbs = await driver.databases.all();
    for (db of dbs) {
        console.log(db.name);
    }
    // end::list-db[]
    // tag::delete-db[]
    if (await driver.databases.contains(DB_NAME)) {
        await (await driver.databases.get(DB_NAME)).delete();
    }
    // end::delete-db[]
    // tag::create-db[]
    await driver.databases.create(DB_NAME);
    // end::create-db[]
    if (driver.databases.contains(DB_NAME)) {
        console.log("Database setup complete.");
    }
    // tag::define[]
    try {
        session = await driver.session(DB_NAME, SessionType.SCHEMA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const define_query = `
                                define
                                email sub attribute, value string;
                                name sub attribute, value string;
                                friendship sub relation, relates friend;
                                user sub entity,
                                    owns email @key,
                                    owns name,
                                    plays friendship:friend;
                                admin sub user;
                                `;
            await transaction.query.define(define_query);
            await transaction.commit();
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::define[]
    // tag::undefine[]
    try {
        session = await driver.session(DB_NAME, SessionType.SCHEMA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const undefine_query = "undefine admin sub user;";
            await transaction.query.undefine(undefine_query);
            await transaction.commit();
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::undefine[]
    // tag::insert[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const insert_query = `
                                insert
                                $user1 isa user, has name "Alice", has email "alice@vaticle.com";
                                $user2 isa user, has name "Bob", has email "bob@vaticle.com";
                                $friendship (friend:$user1, friend: $user2) isa friendship;
                                `;
            await transaction.query.insert(insert_query);
            await transaction.commit();
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::insert[]
    // tag::match-insert[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const match_insert_query = `
                                match
                                $u isa user, has name "Bob";
                                insert
                                $new-u isa user, has name "Charlie", has email "charlie@vaticle.com";
                                $f($u,$new-u) isa friendship;
                                `;
            let response = await transaction.query.insert(match_insert_query).collect();
            if (response.length == 1) {
                await transaction.commit();
            }
            else {await transaction.close();}
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::match-insert[]
    // tag::delete[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const delete_query = `
                                match
                                $u isa user, has name "Charlie";
                                $f ($u) isa friendship;
                                delete
                                $f isa friendship;
                                `;
            await transaction.query.delete(delete_query);
            await transaction.commit();
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::delete[]
    // tag::update[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const update_query = `
                                match
                                $u isa user, has name "Charlie", has email $e;
                                delete
                                $u has $e;
                                insert
                                $u has email "charles@vaticle.com";
                                `;
            let response = await transaction.query.update(update_query).collect();
            if (response.length == 1) {
                await transaction.commit();
            }
            else {await transaction.close();}
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::update[]
    // tag::fetch[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            transaction = await session.transaction(TransactionType.READ);
            const fetch_query = `
                                match
                                $u isa user;
                                fetch
                                $u: name, email;
                                `;
            let response = await transaction.query.fetch(fetch_query).collect();
            for(let i = 0; i < response.length; i++) {
                console.log("User #" + (i + 1) + ": " + JSON.stringify(response[i], null, 4));
            }
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::fetch[]
    // tag::get[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            transaction = await session.transaction(TransactionType.READ);
            const get_query = `
                                match
                                $u isa user, has email $e;
                                get
                                $e;
                                `;
            let response = await transaction.query.get(get_query).collect();
            for(let i = 0; i < response.length; i++) {
                console.log("Email #" + (i + 1) + ": " + response[i].get("e").value);
            }
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::get[]
    // tag::infer-rule[]
    try {
        session = await driver.session(DB_NAME, SessionType.SCHEMA);
        try {
            transaction = await session.transaction(TransactionType.WRITE);
            const define_query = `
                                define
                                rule users:
                                when {
                                    $u isa user;
                                } then {
                                    $u has name "User";
                                };
                                `;
            await transaction.query.define(define_query);
            await transaction.commit();
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::infer-rule[]
    // tag::infer-fetch[]
    try {
        session = await driver.session(DB_NAME, SessionType.DATA);
        try {
            let options = new TypeDBOptions();
            options.infer = true;
            transaction = await session.transaction(TransactionType.READ, options);
            const fetch_query = `
                                match
                                $u isa user;
                                fetch
                                $u: name, email;
                                `;
            let response = await transaction.query.fetch(fetch_query).collect();
            for(let i = 0; i < response.length; i++) {
                console.log("User #" + (i + 1) + ": " + JSON.stringify(response[i], null, 4));
            }
        }
        finally {if (transaction.isOpen()) {await transaction.close()};}
    }
    finally {await session?.close();}
    // end::infer-fetch[]
};

main();
