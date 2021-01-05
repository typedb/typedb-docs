const fs = require('fs')
const Grakn = require("grakn-client");
const reporters = require('jasmine-reporters');

const tapReporter = new reporters.TapReporter();
jasmine.getEnv().addReporter(tapReporter)

jasmine.DEFAULT_TIMEOUT_INTERVAL = 300000;

const loadSchema = async () => {
    const client = new Grakn("localhost:1729");
    const session = await client.session("phone_calls");
    const transaction = await session.transaction().write();
    const defineQuery = fs.readFileSync("files/phone-calls/schema.gql", "utf8");
    await transaction.query(defineQuery);
    await transaction.commit();
    await session.close();
    await client.close();
    console.log("Loaded the phone_calls schema");
};

const deleteDatabase = async () => {
    const client = new Grakn("localhost:1729");
    await client.databases().delete("phone_calls");
    console.log("Deleted the phone_calls database");
    await client.close();
}


describe("Query example for phone_calls", function() {
    beforeAll(async function() { await loadSchema(); });

    it("tests phoneCallsFirstQuery.js", async function() {
        // phoneCallsFirstQuery.js
    });

    it("tests phoneCallsSecondQuery.js", async function() {
        // phoneCallsSecondQuery.js
    });

    it("tests phoneCallsThirdQuery.js", async function() {
        // phoneCallsThirdQuery.js
    });

    it("tests phoneCallsForthQuery.js", async function() {
        // phoneCallsForthQuery.js
    });

    it("tests phoneCallsFifthQuery.js", async function() {
        // phoneCallsFifthQuery.js
    });

    afterAll(async function() { await deleteDatabase(); });
});

describe("Migration of data into phone_calls", function() {
    beforeAll(async function() { await loadSchema(); });
    
    it("tests phoneCallsCSVMigration.js", async function() {
        // phoneCallsCSVMigration.js
    });
    
    it("tests phoneCallsJSONMigration.js", async function() {
        // phoneCallsJSONMigration.js
    });
    
    it("phoneCallsXMLMigration.js", async function() {
        // phoneCallsXMLMigration.js
    });

    afterAll(async function() { await deleteDatabase(); });
});

