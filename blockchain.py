import hashlib
import time
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError


# Classe Block
class Block:
    # O bloco agora armazena uma LISTA de transações em seu campo 'data'
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions # Mudei 'data' para 'transactions'
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        # A lista de transações agora é uma string JSON ordenada
        tx_string = json.dumps(self.transactions, sort_keys=True)
        block_string = f"{self.index}{self.timestamp}{tx_string}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()


# Classe Blockchain

class Blockchain:
    def __init__(self):
        # Lista para transações pendentes 
        self.pending_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # O bloco gênesis agora tem uma lista de transações vazia
        genesis_block = Block(0, transactions=[], previous_hash="0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Adiciona uma transação à lista de pendentes APÓS verificar sua assinatura.
        Esta é a porta de entrada para a rede.
        """
        if not verify_transaction(transaction):
            print("Transação inválida! Assinatura não corresponde.")
            return False
        
        self.pending_transactions.append(transaction)
        print("Transação válida adicionada à piscina de pendentes.")
        return True

    def mine_pending_transactions(self):
        """
        Minera um novo bloco com todas as transações pendentes e o adiciona à cadeia.
        """
        if not self.pending_transactions:
            print("Nenhuma transação pendente para minerar.")
            return None

        # Cria o novo bloco com todas as transações pendentes
        new_block = Block(
            index=self.get_last_block().index + 1,
            transactions=self.pending_transactions,
            previous_hash=self.get_last_block().hash
        )

        # Realiza a prova de trabalho para encontrar o hash válido
        proof = self.proof_of_work(new_block)
        new_block.hash = proof # Atribui o hash encontrado
        
        # Adiciona o bloco minerado à cadeia
        self.chain.append(new_block)

        print(f"Bloco {new_block.index} minerado com sucesso com {len(self.pending_transactions)} transações.")
        
        # Limpa a lista de transações pendentes, pois elas já foram incluídas
        self.pending_transactions = []
        return new_block.index

    def proof_of_work(self, block, difficulty=4):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

# Trabalho Prático 2
def create_transaction(sender_private_key, sender_public_key, receiver, amount):
    sender_hex = sender_public_key.to_string().hex()
    message = f"{sender_hex}->{receiver}:{amount}".encode()
    signature = sender_private_key.sign(message)
    return {
        "sender": sender_hex,
        "receiver": receiver,
        "amount": amount,
        "signature": signature.hex()
    }

def verify_transaction(transaction):
    try:
        pubkey_bytes = bytes.fromhex(transaction['sender'])
        vk = VerifyingKey.from_string(pubkey_bytes, curve=SECP256k1)
        message = f"{transaction['sender']}->{transaction['receiver']}:{transaction['amount']}".encode()
        signature = bytes.fromhex(transaction['signature'])
        return vk.verify(signature, message)
    except (BadSignatureError, KeyError, ValueError):
        # Captura vários erros possíveis (assinatura ruim, campo faltando, etc.)
        return False

# Teste final da Integração
if __name__ == '__main__':
    # Criar carteiras
    alice_private_key = SigningKey.generate(curve=SECP256k1)
    alice_public_key = alice_private_key.get_verifying_key()
    
    bob_private_key = SigningKey.generate(curve=SECP256k1)
    bob_public_key = bob_private_key.get_verifying_key()

    # Iniciar a Blockchain
    my_blockchain = Blockchain()

    # Criar e adicionar transações válidas à piscina
    print("\n--- Adicionando Transações Válidas ---")
    tx1 = create_transaction(alice_private_key, alice_public_key, "Bob", 100)
    my_blockchain.add_transaction(tx1)
    
    tx2 = create_transaction(bob_private_key, bob_public_key, "Alice", 50)
    my_blockchain.add_transaction(tx2)

    # Minerar o bloco com as transações pendentes
    print("\n--- Minerador iniciando ---")
    my_blockchain.mine_pending_transactions()

    # Tentar adicionar uma transação fraudulenta
    print("\n--- Tentando adicionar uma transação fraudulenta ---")
    tx_fraudulenta = create_transaction(alice_private_key, alice_public_key, "Eve (Hacker)", 999)
    # Hacker tenta alterar a transação depois de assinada
    tx_fraudulenta['amount'] = 99999
    my_blockchain.add_transaction(tx_fraudulenta) # Esta transação deve ser rejeitada

    # Minerar novamente (não haverá transações, pois a fraudulenta foi rejeitada)
    print("\n--- Minerador iniciando novamente ---")
    my_blockchain.mine_pending_transactions()

    # Imprimir a blockchain final
    print("\n--- Blockchain Final ---")
    for block in my_blockchain.chain:
        print(f"Índice: {block.index}")
        print(f"Transações: {json.dumps(block.transactions, indent=2)}")
        print(f"Hash: {block.hash}")
        print("-" * 20)