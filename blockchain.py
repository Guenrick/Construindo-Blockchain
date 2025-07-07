import hashlib
import time
import json

# Classe do Bloco
class Block:
    def __init__(self, index, nome_arquivo, hash_arquivo, url, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = {
            "nome_arquivo": nome_arquivo,
            "hash_arquivo": hash_arquivo, 
            "url": url
        }
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()



    def compute_hash(self):
        data_string = json.dumps(self.data, sort_keys=True)
        block_string = f"{self.index}{self.timestamp}{data_string}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

# Classe para Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()


    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            nome_arquivo="genesis.dat",
            hash_arquivo="00000000000000000000000000000000",
            url="none",
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    # Prova de Trabaho
    def proof_of_work(self, block, difficulty=4):
            block.nonce = 0
            computed_hash = block.compute_hash()
            while not computed_hash.startswith('0' * difficulty):
                block.nonce += 1
                computed_hash = block.compute_hash()
            return computed_hash

    # Adiciona bloco
    def add_block(self, nome_arquivo, hash_arquivo, url):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            nome_arquivo=nome_arquivo,
            hash_arquivo=hash_arquivo,
            url=url,
            previous_hash=last_block.hash
        )
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    # Verifica se a chain é válida  
    def is_chain_valid(self):
            for i in range(1, len(self.chain)):
                current = self.chain[i]
                previous = self.chain[i-1]
                if current.hash != current.compute_hash():
                    return False
                if current.previous_hash != previous.hash:
                    return False
            return True

# Código para testar
# Inicializa a blockchain
bc = Blockchain()

print("Minerando Bloco 1...")
# Usando campos do JSON como argumentos para a função
bc.add_block(
    nome_arquivo="exemplo.txt",
    hash_arquivo="a1b2c3d4e5f67890abcdef1234567890",
    url="https://www.example.com/arquivos/exemplo.txt"
)

print("Minerando Bloco 2...")
bc.add_block(
    nome_arquivo="documento_secreto.pdf",
    hash_arquivo="fedcba9876543210fedcba9876543210",
    url="https://www.example.com/arquivos/secreto.pdf"
)

# Código para imprimir e validar a corrente
print("\n--- Blockchain Final ---")
for block in bc.chain:
    print(f"Índice: {block.index}, Dados: {block.data}")

print("\nBlockchain válida:", bc.is_chain_valid())