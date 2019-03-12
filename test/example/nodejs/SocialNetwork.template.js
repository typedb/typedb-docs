const fs = require('fs')
const Grakn = require("grakn-client");
const reporters = require('jasmine-reporters');

const tapReporter = new reporters.TapReporter();
jasmine.getEnv().addReporter(tapReporter)

jasmine.DEFAULT_TIMEOUT_INTERVAL = 500000;

beforeAll(async function() {
    const client = new Grakn("localhost:48555");
    const session = await client.session("social_network");
    const transaction = await session.transaction().write();
    const defineQuery = fs.readFileSync("files/social-network/schema.gql", "utf8");
    await transaction.query(defineQuery);
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

afterAll(async function() {
    const client = new Grakn("localhost:48555");
    await client.keyspaces().delete("social_network");
    console.log("Deleted the social_network keyspace");
});