const fs = require('fs-extra')
fs.copySync(
    '../../../external/graknlabs_client_nodejs/',
    '../../../external/graknlabs_client_nodejs_nosymlinks/', {
        dereference: true,
        filter: (src, dest) => {
            if (src.includes('client-nodejs') && !src.includes('client-nodejs-proto')) {
                return false;
            }
            return true;
        }
    });

const Grakn = require('../../../../external/graknlabs_client_nodejs_nosymlinks/');

const PhoneCallsCSVMigration = require("./PhoneCallsCSVMigration.js");
const PhoneCallsJSONMigration = require("./PhoneCallsJSONMigration.js");
const PhoneCallsXMLMigration = require("./PhoneCallsXMLMigration.js");

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