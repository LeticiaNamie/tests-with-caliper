'use strict';

const OperationBase = require('./utils/operation-base');
const { UPDATE_DID } = require('../../../networks/besu/setup_ids.json');

function generateString(tam) {
    const base58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    let result = '';
    for (let i = 0; i < tam; i++) {
        result += base58chars.charAt(Math.floor(Math.random() * base58chars.length));
    }
    return result;
}

class UpdateDid extends OperationBase {
    constructor() {
        super();
    }

    async submitTransaction() {
        const document = [
            [],
            UPDATE_DID,
            [],
            [["did:indy2:indy_besu:RQDxoJ2Mz3WuyqaqsjVTdN#KEY-1", "Ed25519VerificationKey2018", `did:indy2:testnet:${generateString(22)}`, generateString(44), ""]],
            [["did:indy2:indy_besu:RQDxoJ2Mz3WuyqaqsjVTdN#KEY-1", ["1", "1", "1", "1", "1"]]],
            [], [], [], [], [], []
        ];
        await this.sutAdapter.sendRequests(this.createConnectorRequest('updateDid', document));
    }
}

function createWorkloadModule() {
    return new UpdateDid();
}

module.exports.createWorkloadModule = createWorkloadModule;
