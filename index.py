import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(f'{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}'.encode())
        return sha.hexdigest()
    
    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
    def __repr__(self):
        return (f'Block {self.index}:\n'
                f'  Index: {self.index}\n'
                f'  Timestamp: {self.timestamp}\n'
                f'  Data: {self.data}\n'
                f'  Previous Hash: {self.previous_hash}\n'
                f'  Hash: {self.hash}\n'
                f'  Nonce: {self.nonce}\n')

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        
    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def __repr__(self):
        return '\n'.join([str(block) for block in self.chain])

# Create a blockchain
my_blockchain = Blockchain(difficulty=4)

# Add some blocks
my_blockchain.add_block(Block(1, datetime.datetime.now(), "Block 1 Data", ""))
my_blockchain.add_block(Block(2, datetime.datetime.now(), "Block 2 Data", ""))

# Print the blockchain
print(my_blockchain)

# Check if the blockchain is valid
print("\nIs blockchain valid?", my_blockchain.is_chain_valid())
