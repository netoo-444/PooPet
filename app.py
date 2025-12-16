from logic import SistemaAdocao
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print("\n--- 🐕 SISTEMA POOPET ---")
    print("1. Cadastrar Animal")
    print("2. Cadastrar Adotante")
    print("3. Realizar Adoção")
    print("4. Listar Animais")
    print("5. Verificar Reservas Vencidas")
    print("6. Reservar Animal (48h)")
    print("7. Gerenciar Status (Devolução/Quarentena)")
    print("8. Cuidados (Vacina/Treino)")
    print("0. Sair e Salvar")
    return input("Escolha uma opção: ")

def main():
    sistema = SistemaAdocao()

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            print("\n--- Novo Animal ---")
            tipo = input("Tipo (Cachorro/Gato): ").upper()
            nome = input("Nome: ")
            
            try:
                raca = input("Raça (ou SRD): ")
                idade = int(input("Idade em meses: "))
                sexo = input("Sexo (M/F): ").upper()
                porte = input("Porte (P/M/G): ").upper()
                especial = input("Necessita tratamento especial? (S/N): ").upper() == 'S'
                
                # Pergunta específica por tipo
                info_extra = True
                if tipo == "CACHORRO":
                    resp = input("É sociável com gatos? (S/N): ").strip().upper()
                    info_extra = (resp == "S")
                else: # GATO
                    resp = input("Usa caixa de areia? (S/N): ").strip().upper()
                    info_extra = (resp == "S")

                temp_input = input("Temperamento (separe por vírgula, ex: Calmo,Brincalhão): ")
                temperamento = [t.strip() for t in temp_input.split(",") if t.strip()]

                animal = sistema.cadastrar_animal(tipo, nome, raca, sexo, idade, porte, especial, temperamento, info_extra)
                print(f"✅ {animal.nome} cadastrado com sucesso!")
            except ValueError:
                print("❌ Erro: Idade deve ser um número.")

        elif opcao == "2":
            print("\n--- Novo Adotante ---")
            nome = input("Nome: ")
            try:
                idade = int(input("Idade: "))
                moradia = input("Moradia (Casa/Apartamento): ")
                area_util = float(input("Área útil (m²): "))
                
                
                outros_animais = input("Possui outros animais? (S/N): ").upper() == 'S'
                experiencia_pets = input("Tem experiência com pets? (S/N): ").upper() == 'S'
                criancas = input("Possui crianças em casa? (S/N): ").upper() == 'S'
                
                adotante = sistema.cadastrar_adotante(nome, idade, moradia, area_util, outros_animais, experiencia_pets, criancas)
                print(f"✅ {adotante.nome} cadastrado!")
            except ValueError:
                print("❌ Erro: Certifique-se de digitar números para idade e área.")

        elif opcao == "3":
            print("\n--- Realizar Adoção ---")
            
            # Listar Adotantes
            for i, a in enumerate(sistema.adotantes):
                print(f"{i}. {a.nome} (Idade: {a.idade})")
            
            try:
                idx_adotante = int(input("Escolha o ID do Adotante: "))
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            # Listar Animais Disponíveis
            disponiveis = sistema.listar_animais_disponiveis()
            if not disponiveis:
                print("❌ Nenhum animal disponível.")
                continue

            for i, a in enumerate(disponiveis):
                print(f"{i}. {a.nome} ({a.especie})")
            
            try:
                idx_animal = int(input("Escolha o ID do Animal: "))
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            # Processar
            print(f"\nProcessando adoção...")
            sucesso, mensagem = sistema.processar_adocao(idx_adotante, idx_animal)
            print(mensagem)

        elif opcao == "4":
            print("\n--- Lista de Animais ---")
            for resumo in sistema.listar_animais():
                print(resumo)

        elif opcao == "5":
            print("\n--- Verificando Reservas ---")
            logs = sistema.processar_expiracoes()
            if not logs: print("ℹ️ Nenhuma alteração.")
            for log in logs:
                print(f"ℹ️ {log}")

        elif opcao == "6":
            print("\n--- Reservar Animal ---")
            for i, a in enumerate(sistema.adotantes):
                print(f"{i}. {a.nome}")
            
            try:
                idx_adotante = int(input("ID do Adotante: "))
                
                print("\nAnimais:")
                todos = sistema.animais
                for i, a in enumerate(todos):
                    print(f"{i}. {a.nome} [{a.status}]")
                
                idx_animal = int(input("ID do Animal: "))

                sucesso, msg = sistema.reservar_animal(idx_adotante, idx_animal)
                print(msg)
            except ValueError:
                print("❌ Entrada inválida.")

        elif opcao == "7":
            print("\n--- Gerenciamento de Status ---")
            print("1. Registrar Devolução (ADOTADO -> DEVOLVIDO/QUARENTENA)")
            print("2. Alterar Status Manualmente (QUARENTENA/INADOTAVEL/DISPONIVEL)")
            sub_opcao = input("Escolha: ")

            if sub_opcao == "1":
                adotados = sistema.listar_animais_por_status("ADOTADO")
                if not adotados:
                    print("Nenhum animal adotado para devolver.")
                else:
                    for i, a in enumerate(adotados):
                        print(f"{i}. {a.nome} (ID: {a.id})")
                    try:
                        idx = int(input("ID da lista acima: "))
                        motivo = input("Motivo da devolução: ")
                        sucesso, msg = sistema.processar_devolucao(idx, motivo)
                        print(msg)
                    except ValueError:
                        print("❌ Entrada inválida.")

            elif sub_opcao == "2":
                todos = sistema.animais
                for i, a in enumerate(todos):
                    print(f"{i}. {a.nome} [{a.status}]")
                try:
                    idx = int(input("ID do animal na lista geral: "))
                    print("Status válidos: DISPONIVEL, QUARENTENA, INADOTAVEL")
                    novo_status = input("Digite o novo status: ").upper()
                    
                    if novo_status in ["DISPONIVEL", "QUARENTENA", "INADOTAVEL"]:
                        sucesso, msg = sistema.alterar_status_manual(idx, novo_status)
                        print(msg)
                    else:
                        print("❌ Status inválido.")
                except ValueError:
                    print("❌ Entrada inválida.")

        elif opcao == "8":
            print("\n--- Cuidados e Eventos ---")
            animais = sistema.listar_animais()
            if not animais:
                print("Nenhum animal cadastrado.")
                continue
            
            for i, a in enumerate(animais):
                print(f"{i}. {a}")
            
            try:
                idx = int(input("Escolha o ID do animal na lista acima: "))
                print("\n1. Registrar Vacina")
                print("2. Registrar Treino (Apenas Cães)")
                acao = input("Escolha a ação: ")
                
                if acao == "1":
                    vacina = input("Nome da vacina (ex: Raiva, V10): ")
                    sucesso, msg = sistema.registrar_vacina(idx, vacina)
                    print(msg)
                elif acao == "2":
                    sucesso, msg = sistema.registrar_treino(idx)
                    print(msg)
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida.")

        elif opcao == "0":
            print("\n📊 --- Relatório Final do Sistema ---")
            
            relatorios = sistema.gerar_relatorios()

        
            print("\n🏆 Top 5 Animais Mais Adotáveis (Compatibilidade Média):")
            if not relatorios['top5']:
                print("   (Sem dados suficientes)")
            for r in relatorios['top5']:
                print(f"   - {r['nome']} ({r['especie']}): {r['score_medio']:.1f}/100")

            # 2. Taxa de Adoções por Tipo
            print("\n📈 Taxa de Adoções (Espécie/Porte):")
            if not relatorios['taxa_tipo']:
                print("   (Nenhuma adoção registrada)")
            for k, v in relatorios['taxa_tipo'].items():
                print(f"   - {k}: {v}")

            # 3. Tempo Médio de Adoção
            print(f"\n⏱️ Tempo Médio entre Entrada e Adoção: {relatorios['tempo_medio']:.1f} dias")

            # 4. Devoluções por Motivo
            print("\n⚠️ Devoluções/Cancelamentos por Motivo:")
            if not relatorios['devolucoes']:
                print("   (Nenhuma devolução registrada)")
            for motivo, qtd in relatorios['devolucoes'].items():
                print(f"   - {motivo}: {qtd}")

            print("\n💾 Salvando dados...")
            sistema.salvar_dados()
            print("👋 Até logo!")
            break
        
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()