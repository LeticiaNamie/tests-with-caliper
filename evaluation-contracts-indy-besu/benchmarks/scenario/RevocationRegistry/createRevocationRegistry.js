'use strict';

const OperationBase = require('./utils/operation-base');
const { ISSUER_DID, CRED_DEF_ID } = require('../../../networks/besu/setup_ids.json');

function generateString(tam) {
    const base58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    let result = '';
    for (let i = 0; i < tam; i++) {
        result += base58chars.charAt(Math.floor(Math.random() * base58chars.length));
    }
    return result;
}

class createRevocationRegistry extends OperationBase {
    constructor() {
        super();
    }

    async submitTransaction() {

        const suffix = generateString(12)
        const revRegistry = ["1.0.0", `revReg${suffix}`, "CL", CRED_DEF_ID, "test-tag", "value123", ISSUER_DID]

        // const revRegistry =  ["1.0.0", "revReg123", "CL", "did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN/anoncreds/v0/CLAIM_DEF/did:indy2:indy_besu:MRDxoJ2Mz3ZuyqaqsjVTdN/anoncreds/v0/SCHEMA/BasicIdentity/1.0.0/BasicIdentity233", "test-tag", "value123", "did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN"]

        await this.sutAdapter.sendRequests(this.createConnectorRequest('createRevocationRegistry', revRegistry));
    }
}

function createWorkloadModule() {
    return new createRevocationRegistry();
}

module.exports.createWorkloadModule = createWorkloadModule;