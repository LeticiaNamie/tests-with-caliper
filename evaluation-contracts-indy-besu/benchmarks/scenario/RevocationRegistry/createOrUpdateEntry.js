'use strict';

const OperationBase = require('./utils/operation-base');
const { ISSUER_DID } = require('../../../networks/besu/setup_ids.json');

function generateNumber(tam) {
    var randomNumber = "";
    var numbers = '0123456789';
    for (var i = 0; i < tam; i++) {
        randomNumber += numbers.charAt(Math.floor(Math.random() * numbers.length));
    }
    return randomNumber;
}


class createOrUpdateEntry extends OperationBase {
    constructor() {
        super();
    }

    async submitTransaction() {
        const revEntry_end =  generateNumber(3)
        const revEntry = [
            "revReg123",
            "CL_ACCUM",
            `revocationEntry${revEntry_end}`,
            ISSUER_DID
        ]
        // const revEntry =  ["revReg123","CL", "revocationEntry1","did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN"]

        await this.sutAdapter.sendRequests(this.createConnectorRequest('createOrUpdateEntry', revEntry));
    }
}

function createWorkloadModule() {
    return new createOrUpdateEntry();
}

module.exports.createWorkloadModule = createWorkloadModule;