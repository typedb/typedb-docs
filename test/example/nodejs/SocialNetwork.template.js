const fs = require('fs')
const { TypeDB } = require("typedb-client/TypeDB");
const { SessionType } = require("typedb-client/api/TypeDBSession");
const { TransactionType } = require("typedb-client/api/TypeDBTransaction");
const reporters = require('jasmine-reporters');

const tapReporter = new reporters.TapReporter();
jasmine.getEnv().addReporter(tapReporter)

jasmine.DEFAULT_TIMEOUT_INTERVAL = 500000;

beforeAll(async function() {
    const client = TypeDB.coreClient("localhost:1729");
    if (await(client.databases().contains('social_network'))) {
        await (await client.databases().get('social_network')).delete();
    }
    await client.databases().create('social_network');
    const session = await client.session("social_network", SessionType.SCHEMA);
    const transaction = await session.transaction(TransactionType.WRITE);
    const defineQuery = fs.readFileSync("files/social-network/schema.tql", "utf8");
    await transaction.query().define(defineQuery);
    await transaction.commit();
    await session.close();
    console.log("Loaded the social_network schema");
});

describe("Quickstart Tests", function() {
    it("test socialNetworkQuickstartQuery.js", async function() {
        // socialNetworkQuickstartQuery.js
    });
});

describe("Client Quickstart Tests", function() {
    it("tests socialNetworkNodejsClientA.js", function() {
        // socialNetworkNodejsClientA.js
    });

    it("tests socialNetworkNodejsClientB.js", async function() {
        // socialNetworkNodejsClientB.js
    });

    it("tests socialNetworkNodejsClientC", async function() {
        // socialNetworkNodejsClientC.js
    });

    it("tests socialNetworkNodejsClientD.js", async function() {
        // socialNetworkNodejsClientD.js
    });
});
