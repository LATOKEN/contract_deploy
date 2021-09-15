# How to deploy smart contracts on testnet/devnet

1. Download this python script
2. Change the name of the wasm and abi files according to your smart contracts
1. Use feed_wallet.deploy_contract(bytecode, abi) to deploy contracts. The returned value is the address on which the contract is deployed.
