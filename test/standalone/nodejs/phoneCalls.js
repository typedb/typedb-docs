const fs = require('fs')
const Grakn = require("grakn-client");

const PhoneCallsCSVMigration = require("../generated/phoneCallsCSVMigration.js");
const PhoneCallsJSONMigration = require("../generated/phoneCallsJSONMigration.js");
const PhoneCallsXMLMigration = require("../generated/phoneCallsXMLMigration.js");

jasmine.DEFAULT_TIMEOUT_INTERVAL = 500000;

beforeAll(async function() {
    const client = new Grakn("localhost:48555");
    const session = await client.session("phone_calls");
    const transaction = await session.transaction(Grakn.txType.WRITE);
    const defineQuery = fs.readFileSync("files/phone-calls/schema.gql", "utf8");
    await transaction.query(defineQuery);
    await transaction.commit();
    await session.close();
});

describe("Migration of data into phone_calls", function() {
    it("migrates csv data into phone_calls", async function() {
        await PhoneCallsCSVMigration.initiate();
    });

    it("migrates json data into phone_calls", async function() {
        await PhoneCallsJSONMigration.initiate();
    });

    it("migrates xml data into phone_calls", async function() {
        await PhoneCallsXMLMigration.initiate();
    });
});

afterAll(async function() {
    const client = new Grakn("localhost:48555");
    const session = await client.session("phone_calls");
    const transaction = await session.transaction(Grakn.txType.WRITE);
    await transaction.query("match $x isa relationship; delete $x;");
    await transaction.query("match $x isa entity; delete $x;");
    await transaction.query("match $x isa attribute; delete $x;");
    await transaction.commit();
    await session.close();
});