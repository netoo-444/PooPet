from models import Cachorro, Adotante, Gato
from repository import Repositorio

def main():
    print("--- 🐕 SISTEMA POOPET ---")


    repo = Repositorio()
    animais_cadastrados = []
    adocoes_realizadas = []


    rex = Cachorro(1, "Vira-lata", "Rex", "M", 12, "M", ["Dócil"], True)
    mimi = Gato(2, "Siamês", "Mimi", "F", 24, "P", ["Manso"], True)
    
    animais_cadastrados.append(rex)
    animais_cadastrados.append(mimi)


    joao = Adotante(1, "Joao Silva", 30, "Casa", 100.0, False, True, False)

    
    print(f"\n1. Status inicial de {rex.nome}: {rex.status}")
    
    try:
        reserva = joao.solicitar_reserva(rex)
        print(f"2. Reserva realizada para: {reserva.animal.nome}")
        print(f"3. Novo Status de {rex.nome}: {rex.status}")
    except ValueError as e:
        print(e)

    adocao = joao.finalizar_adocao(rex, taxa=50.0)
    adocoes_realizadas.append(adocao)
    print(f"4. Adoção finalizada! Status final: {rex.status}")


    print("\n--- SALVANDO DADOS ---")
    repo.salvar_dados(animais_cadastrados, adocoes_realizadas)

    
    print("\n--- 📊 RELATÓRIO SIMPLES ---")
    dados_lidos = repo.carregar_dados()
    for item in dados_lidos:
        print(f"ID: {item['id']} | Nome: {item['nome']} | Status: {item['status']}")

if __name__ == "__main__":
    main()