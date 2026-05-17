'use strict';

const OperationBase = require('./utils/operation-base');
const { ISSUER_DID, SCHEMA_ID } = require('../../../networks/besu/setup_ids.json');

function generateString(tam) {
    const base58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    let randomString = '';
    for (let i = 0; i < tam; i++) {
        randomString += base58chars.charAt(Math.floor(Math.random() * base58chars.length));
    }
    return randomString;
}

class createCredentialDefinition extends OperationBase {
    constructor() {
        super();
    }

    async submitTransaction() {
        const did_end = generateString(18)
        const credDef = [`${ISSUER_DID}/anoncreds/v0/CLAIM_DEF/${SCHEMA_ID}/${did_end}`, ISSUER_DID, SCHEMA_ID, "CL", "BasicIdentity", "<keys>"]
        // const credDef = ["did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN/anoncreds/v0/CLAIM_DEF/did:indy2:indy_besu:MRDxoJ2Mz3ZuyqaqsjVTdN/anoncreds/v0/SCHEMA/BasicIdentity/1.0.0/BasicIdentity233","did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN","did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN/anoncreds/v0/SCHEMA/ScoreSch233/233","CL","BasicIdentity","<keys>"]

        await this.sutAdapter.sendRequests(this.createConnectorRequest('createCredentialDefinition', credDef));
    }
}

function createWorkloadModule() {
    return new createCredentialDefinition();
}

module.exports.createWorkloadModule = createWorkloadModule;