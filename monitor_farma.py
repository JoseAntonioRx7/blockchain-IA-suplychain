import json
from web3 import Web3
import time

# --- CONFIGURAÇÃO DE INFRAESTRUTURA ---
# Conecta ao seu Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# DADOS DO CONTRATO (Cole aqui o que você pegou no Remix)
contract_address = "0x36a075f350ebF154f496b3E16F90B9594F2B6d40"
abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_nome",
				"type": "string"
			}
		],
		"name": "iniciarJornada",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_id",
				"type": "uint256"
			},
			{
				"internalType": "int256",
				"name": "_temp",
				"type": "int256"
			},
			{
				"internalType": "string",
				"name": "_data",
				"type": "string"
			}
		],
		"name": "registrarAnomalia",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "lotes",
		"outputs": [
			{
				"internalType": "string",
				"name": "nomeMedicamento",
				"type": "string"
			},
			{
				"internalType": "enum RastreioFarma.Estado",
				"name": "statusAtual",
				"type": "uint8"
			},
			{
				"internalType": "int256",
				"name": "ultimaTemperatura",
				"type": "int256"
			},
			{
				"internalType": "string",
				"name": "timestampFalha",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = web3.eth.contract(address=contract_address, abi=abi)
conta_admin = web3.eth.accounts[0] # Usa a primeira conta da lista do Ganache

# --- LÓGICA DA SOLUÇÃO ---

def iniciar_lote(id_lote, nome):
    """ Registra o medicamento no início da jornada """
    print(f"\n[SISTEMA] Iniciando rastreio do lote {id_lote}: {nome}")
    tx = contract.functions.iniciarJornada(id_lote, nome).transact({'from': conta_admin})
    web3.eth.wait_for_transaction_receipt(tx)
    print("Registro de origem gravado no Blockchain.")

def ia_analisador_coldchain(id_lote, temperatura):
    """ 
    Simulação da IA: Ela decide se o dado é uma anomalia.
    Para o artigo: 'Algoritmo de monitoramento autônomo de integridade térmica'.
    """
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{timestamp}] Sensor detectou: {temperatura}°C")
    
    # Regra de Ouro: Entre 2°C e 8°C (Insulina/Vacinas)
    if temperatura < 2 or temperatura > 8:
        print(f"IA DETECTOU QUEBRA DE PROTOCOLO: {temperatura}°C!")
        print("IA Acionando contrato inteligente para bloqueio do lote...")
        
        # Grava a falha de forma imutável
        tx = contract.functions.registrarAnomalia(id_lote, int(temperatura), timestamp).transact({'from': conta_admin})
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        
        print(f"LOTE COMPROMETIDO REGISTRADO. Hash: {receipt.transactionHash.hex()}")
    else:
        print("Temperatura estável. Integridade garantida.")

# --- EXECUÇÃO DO EXPERIMENTO (Para os resultados da sua IC) ---

# 1. Cadastro inicial
iniciar_lote(1001, "Insulina Humana (Alto Custo)")

# 2. Simulação de transporte normal
time.sleep(1)
ia_analisador_coldchain(1001, 5.0)

# 3. Simulação da DOR (Falha no compressor de refrigeração)
time.sleep(2)
ia_analisador_coldchain(1001, 12.0)