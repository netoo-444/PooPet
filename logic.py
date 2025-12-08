from models import Cachorro, Gato, Adotante
from repository import Repositorio

class SistemaAdocao:
    def __init__(self):
        self.repo = Repositorio()
        self.animais = []
        self.adotantes = []
        self.adocoes = []
        
    
        self._carregar_dados_iniciais()

    def _carregar_dados_iniciais(self):

        rex = Cachorro(1, "Vira-lata", "Rex", "M", 12, "M", ["Dócil"], True)
        joao = Adotante(1, "Joao Silva", 25, "Casa", 100.0, False, True, False)
        self.animais.append(rex)
        self.adotantes.append(joao)

    def cadastrar_animal(self, tipo, nome):
        id_novo = len(self.animais) + 1
        if tipo == "CACHORRO":
            novo_animal = Cachorro(id_novo, "SRD", nome, "M", 12, "M", [], True)
        else:
            novo_animal = Gato(id_novo, "SRD", nome, "M", 12, "P", [], True)
        
        self.animais.append(novo_animal)
        return novo_animal

    def cadastrar_adotante(self, nome, idade, moradia):
        novo_adotante = Adotante(len(self.adotantes)+1, nome, idade, moradia, 50.0, False, True, False)
        self.adotantes.append(novo_adotante)
        return novo_adotante

    def listar_animais(self):
        return [a.get_resumo() for a in self.animais]
    
    def listar_animais_disponiveis(self):
        return [a for a in self.animais if a.status == "DISPONIVEL"]

    def buscar_adotante(self, indice):
        try:
            return self.adotantes[indice]
        except IndexError:
            return None

    def buscar_animal_disponivel(self, indice):
        disponiveis = self.listar_animais_disponiveis()
        try:
            return disponiveis[indice]
        except IndexError:
            return None

    def processar_adocao(self, indice_adotante, indice_animal):
        adotante = self.buscar_adotante(indice_adotante)
        animal = self.buscar_animal_disponivel(indice_animal)

        if not adotante:
            return False, "❌ Adotante inválido."
        if not animal:
            return False, "❌ Animal inválido."

        # Validação de Regras
        if adotante.verificar_elegibilidade(animal):
            try:
                adocao = adotante.finalizar_adocao(animal, taxa=50.0)
                self.adocoes.append(adocao)
                return True, f"🎉 Sucesso! {animal.nome} foi adotado por {adotante.nome}!"
            except ValueError as e:
                return False, f"Erro: {e}"
        else:
            return False, "Adoção negada pelas regras do sistema."

    def salvar_dados(self):
        self.repo.salvar_dados(self.animais, self.adocoes)
