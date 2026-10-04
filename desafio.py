import time
from tqdm import tqdm

# Inicialização das listas sincronizadas
pedidos_ids = []
pedidos_pesos = []
pedidos_tipos = []
pedidos_valores = []

CAPACIDADE_MAXIMA = 1000.0  # Limite máximo do caminhão em kg

while True:
    print("\n=== LOGI EXPRESS ===")
    print("1: Cadastrar novo pedido")
    print("2: Processar/Carregar caminhão")
    print("3: Exibir relatório")
    print("0: Encerrar o turno")
    
    opcao = input("Escolha uma opção: ")
    
    match opcao:
        case "1":
            try:
                codigo = int(input("Código do pedido (inteiro): "))
            except ValueError:
                print("Erro: O código tem de ser um número inteiro.")
                continue
                
            # Evita cadastrar o mesmo ID
            if codigo in pedidos_ids:
                print("Erro: Já existe um pedido registado com este ID!")
                continue
                
            peso = float(input("Peso em kg: "))
            
            if peso <= 0:
                print("Erro: O peso não pode ser menor ou igual a 0.")
                continue
                
            # Variável auxiliar: Soma o peso de todos os pedidos já pendentes + o peso atual do pedido
            aux_soma = sum(pedidos_pesos) + peso
            
            # Se a soma total ultrapassar a capacidade máxima, o pedido não é cadastrado
            if aux_soma > CAPACIDADE_MAXIMA:
                print(f"Erro: A capacidade máxima do caminhão seria ultrapassada! Peso total acumulado seria {aux_soma} kg (Limite: {CAPACIDADE_MAXIMA} kg).")
                continue
                
            tipo = input("Tipo (VIP, EXPRESSO, CONVENCIONAL): ").strip().upper()
            valor = float(input("Valor declarado (R$): "))
            
            # Validações restantes
            if valor <= 0:
                print("Erro: O valor não pode ser menor ou igual a 0.")
            elif tipo not in ["VIP", "EXPRESSO", "CONVENCIONAL"]:
                print("Erro: Tipo inválido. Use VIP, EXPRESSO ou CONVENCIONAL.")
            else:
                # Barra de progresso tqdm para o cadastro
                for _ in tqdm(range(20), desc="A registar novo pedido"):
                    time.sleep(0.03)
                
                # Prioridade para valores acima de R$ 5.000,00 (entra na posição 0)
                if valor > 5000.00:
                    pedidos_ids.insert(0, codigo)
                    pedidos_pesos.insert(0, peso)
                    pedidos_tipos.insert(0, tipo)
                    pedidos_valores.insert(0, valor)
                    print("Pedido de alto valor registado com prioridade no início da fila.")
                else:
                    pedidos_ids.append(codigo)
                    pedidos_pesos.append(peso)
                    pedidos_tipos.append(tipo)
                    pedidos_valores.append(valor)
                    print("Pedido registado com sucesso.")
                    
        case "2":
            if not pedidos_ids:
                print("Não há pedidos pendentes.")
                continue
            
            for _ in tqdm(range(20), desc="A processar triagem e carga"):
                time.sleep(0.03)
                
            caminhao_carga = []
            peso_acumulado = 0.0
            remover_indices = []
            
            # Processamento percorrendo o vetor de pedidos
            for i in range(len(pedidos_ids)):
                peso_pedido = pedidos_pesos[i]
                tipo_atual = pedidos_tipos[i]
                
                match tipo_atual:
                    case "VIP":
                        taxa = "Isento"
                    case "EXPRESSO":
                        taxa = "+15% no frete"
                    case "CONVENCIONAL":
                        taxa = "+5% no frete"
                
                # Variável auxiliar para somar o peso acumulado atual com o peso do pedido da vez
                aux_carga = peso_acumulado + peso_pedido
                
                if aux_carga <= CAPACIDADE_MAXIMA:
                    caminhao_carga.append(pedidos_ids[i])
                    peso_acumulado = aux_carga  # Atualiza o peso acumulado
                    remover_indices.append(i)
                else:
                    continue
            
            # Remove os pedidos carregados da lista de pendentes (de trás para frente)
            for i in sorted(remover_indices, reverse=True):
                print(f"Carregando ID {pedidos_ids[i]} ({pedidos_tipos[i]}, {pedidos_pesos[i]}kg)")
                pedidos_ids.pop(i)
                pedidos_pesos.pop(i)
                pedidos_tipos.pop(i)
                pedidos_valores.pop(i)
            
            print(f"\nCaminhão carregado! Peso total acumulado: {peso_acumulado}kg / {CAPACIDADE_MAXIMA}kg")
            print(f"IDs no caminhão: {caminhao_carga}")
            
        case "3":
            for _ in tqdm(range(20), desc="A carregar relatório"):
                time.sleep(0.03)
                
            if not pedidos_ids:
                print("Nenhum pedido pendente na fila.")
            else:
                print("\n--- Relatório de Pedidos Pendentes ---")
                for i in range(len(pedidos_ids)):
                    print(f"ID: {pedidos_ids[i]} | Peso: {pedidos_pesos[i]}kg | Tipo: {pedidos_tipos[i]} | Valor: R$ {pedidos_valores[i]:.2f}")
                    
        case "0":
            for _ in tqdm(range(20), desc="A encerrar o turno"):
                time.sleep(0.03)
            print("Turno encerrado com sucesso. Até logo!")
            break
            
        case _:
            print("Opção inválida! Tente novamente.")