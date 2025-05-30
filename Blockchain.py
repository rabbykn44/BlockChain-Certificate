from Block import Block
import time

class Blockchain:
    difficulty = 2  # Difficulty for proof-of-work

    def __init__(self):
        self.unconfirmed_transactions = []  # Data yet to be added to the chain
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the blockchain, also known as the genesis block.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Return the last block in the chain.
        """
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Perform proof of work by finding a hash that meets the difficulty level.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_new_transaction(self, transaction):
        """
        Add a new transaction to the list of unconfirmed transactions.
        """
        self.unconfirmed_transactions.append(transaction)

    def mine_block(self):
        """
        Add a block with the unconfirmed transactions to the blockchain.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.compute_hash())

        # Perform proof of work
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []  # Reset the unconfirmed transactions
        return new_block
