from web3 import Web3
import json
import time

# 1. Configuração de Conexão (Ganache)
ganache_url = "http://127.0.0.1:7545" # Verifique a porta no seu Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificando conexão
if not web3.is_connected():
    print("Erro: Não foi possível conectar ao Ganache!")
    exit()

# 2. Endereços e Credenciais
# Substitua pelos dados do seu Remix/Ganache
contract_address = "COLE_AQUI_O_ENDERECO_DO_CONTRATO"
wallet_address = web3.eth.accounts[0] # Usa a primeira conta do Ganache

# Cole aqui o ABI gerado pelo Remix (formato de lista/json)
contract_abi = json.loads('[COLE_AQUI_O_ABI_COMPLETO]')

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def monitorar_sensor_ia(id_lote, temperatura):
    """
    Simula o 'Cérebro' da arquitetura.
    Analisa os dados e decide se deve acionar o Blockchain.
    """
    print(f"[{time.strftime('%H:%M:%S')}] IA Analisando Lote {id_lote}: {temperatura}°C")
    
    # Lógica de decisão (A 'IA' detectando a falha)
    if temperatura < 2 or temperatura > 8:
        print(f"⚠️ ALERTA: Temperatura crítica detectada ({temperatura}°C)!")
        registrar_no_blockchain(id_lote, temperatura)
    else:
        print("Status: Condições ideais.")

def registrar_no_blockchain(id_lote, temp):
    """
    A ponte Web3: Transforma a decisão da IA em um registro imutável.
    """
    print("Registrando anomalia no Blockchain de forma imutável...")
    
    tx_hash = contract.functions.registrarAnomalia(
        id_lote, 
        int(temp), 
        time.strftime("%d/%m/%Y %H:%M:%S")
    ).transact({'from': wallet_address})
    
    # Aguarda a mineração do bloco
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transação confirmada! Bloco: {receipt.blockNumber}")
    print(f"Hash: {tx_hash.hex()}")

# --- SIMULAÇÃO PRÁTICA ---
# Lote 101: Insulina (Alto Custo)
print("--- Iniciando Monitoramento de Lote Farmacêutico ---")
monitorar_sensor_ia(101, 5.2)  # OK
time.sleep(2)
monitorar_sensor_ia(101, 9.5)  # FALHA - Aciona o Blockchain