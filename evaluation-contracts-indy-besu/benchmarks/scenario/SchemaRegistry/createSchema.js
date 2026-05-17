'use strict';

const OperationBase = require('./utils/operation-base');
const { ISSUER_DID } = require('../../../networks/besu/setup_ids.json');

function generateString(tam) {
    const base58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    let randomString = '';
    for (let i = 0; i < tam; i++) {
        randomString += base58chars.charAt(Math.floor(Math.random() * base58chars.length));
    }
    return randomString;
}

class CreateSchema extends OperationBase {
    constructor() {
        super();
    }

    async submitTransaction() {
        const did_end = generateString(4)
        const schema = [
            `${ISSUER_DID}/anoncreds/v0/SCHEMA/GradeSch${did_end}/1.0`,
            ISSUER_DID,
            `GradeSch${did_end}`,
            "1.0",
            ["grade", "subject"]
        ]
        // const schema = ["did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN/anoncreds/v0/SCHEMA/ScoreSch233/233","did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN","ScoreSch233","233",["grade", "score"]]
        await this.sutAdapter.sendRequests(this.createConnectorRequest('createSchema', schema));
    }
}

function createWorkloadModule() {
    return new CreateSchema();
}

module.exports.createWorkloadModule = createWorkloadModule;
