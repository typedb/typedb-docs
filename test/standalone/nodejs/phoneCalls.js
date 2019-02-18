const Grakn = require("grakn");
const fs = require("fs");

const PhoneCallsCSVMigration = require("PhoneCallsCSVMigration.js");
const PhoneCallsJSONMigration = require("PhoneCallsJSONMigration.js");
const PhoneCallsXMLMigration = require("PhoneCallsXMLMigration.js");

beforeAll(async () => {
    await loadSchemaPhoneCalls();
});

loadSchemaPhoneCalls = async () => {
    const defineQuery = fs.readFileSync("files/phone-calls/schema.gql");
    const client = new Grakn("localhost:48555");
    const session = client.session("phone_calls");
    const transaction = await session.transaction(grakn.TxType.WRITE);
    await transaction.query(defineQuery);
    transaction.commit();
    session.close();
};

describe("Test migration scripts for phone_calls", () => {
    test("CSV migration", async () => {
        await PhoneCallsCSVMigration.buildPhoneCallGraph();
    });

    test("JSON migration", async () => {
        await PhoneCallsJSONMigration.buildPhoneCallGraph();
    });

    test("XML migration", async () => {
        await PhoneCallsXMLMigration.buildPhoneCallGraph();
    });
});