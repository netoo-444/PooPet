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
            
            animal = sistema.cadastrar_animal(tipo, nome)
            print(f"✅ {animal.nome} cadastrado com sucesso!")

        elif opcao == "2":
            print("\n--- Novo Adotante ---")
            nome = input("Nome: ")
            try:
                idade = int(input("Idade: "))
                moradia = input("Moradia (Casa/Apartamento): ")
                
                adotante = sistema.cadastrar_adotante(nome, idade, moradia)
                print(f"✅ {adotante.nome} cadastrado!")
            except ValueError:
                print("❌ Idade deve ser um número.")

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

        elif opcao == "0":
            print("\nSalvando dados...")
            sistema.salvar_dados()
            print("Até logo!")
            break
        
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()