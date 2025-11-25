from datetime import date, datetime
from typing import List


class Evento:
    """
    Classe de dados simples que representa um registro de ocorrência no histórico do Animal.
    É responsável por armazenar a data, o tipo de evento (vacina, mudança de status)
    """
    def __init__(self, tipo: str, descricao: str):
        self.tipo = tipo
        self.descricao = descricao
        self.data = datetime.now()



class Animal:
    """
    Representa a entidade principal do sistema: o animal disponível para adoção.
    É responsável por armazenar dados de cadastro (espécie, porte, temperamento),
    gerenciar seu status através de regras de transição e registrar a cronologia completa de eventos (vacinas, mudanças de status)
    em seu histórico. Serve como classe base para Cachorro e Gato.
    """
    def __init__(self, id: int, especie: str, raca: str, nome: str, sexo: str, 
                idade_meses: int, porte: str, temperamento: List[str]):
        self.id = id
        self.especie = especie
        self.raca = raca
        self.nome = nome
        self.sexo = sexo
        self.idade_meses = idade_meses
        self.porte = porte
        self.temperamento = temperamento
        
        
        self._status = "DISPONIVEL"
        self.data_entrada = date.today()
        self.historico: List[Evento] = []

    @property
    def status(self):
        """Permite ler o status."""
        return self._status

    def mudar_status(self, novo_status: str):
        antigo_status = self._status
        self._status = novo_status
        self.adicionar_evento("Mudança de Status", f"De {antigo_status} para {novo_status}")
    
    def aplicar_vacina(self, vacina: str):
        self.adicionar_evento("Vacina", f"Aplicação de: {vacina}")

    def adicionar_evento(self, tipo: str, descricao: str):
        """Método auxiliar para adicionar eventos ao histórico."""
        novo_evento = Evento(tipo, descricao)
        self.historico.append(novo_evento)

    def get_resumo(self) -> str:
        return f"[{self.status}] {self.nome} - {self.especie}"


class Adotante:
    """
    Representa a pessoa que solicita uma adoção.
    É responsável por armazenar os dados utilizados na Triagem de adotantes (idade,
    moradia, área útil e experiência com pets). Contém a lógica inicial para
    verificar a elegibilidade conforme o sistema.
    """
    def __init__(self, id: int, nome: str, idade: int, moradia: str, area_util: float, 
                outros_animais: bool, experiencia_pets: bool, possui_criancas: bool):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.moradia = moradia
        self.area_util = area_util
        self.outros_animais = outros_animais
        
        self.possui_criancas = possui_criancas
        self.experiencia_pets = experiencia_pets
        
    @property
    def possui_criancas(self):
        return self._possui_criancas

    @possui_criancas.setter
    def possui_criancas(self, valor: bool):
        if not isinstance(valor, bool):
            raise ValueError("O campo 'possui_criancas' deve ser True ou False.")
        self._possui_criancas = valor

    @property
    def experiencia_pets(self):
        return self._experiencia_pets

    @experiencia_pets.setter
    def experiencia_pets(self, valor: bool):
        if not isinstance(valor, bool):
            raise ValueError("A experiência deve ser True ou False.")
        self._experiencia_pets = valor

    def verificar_elegibilidade(self) -> bool:
        """
        Usa os dados encapsulados para determinar se o adotante é elegível.
        """
    
        if self._possui_criancas and not self._experiencia_pets:
            return False 
        return True

    def solicitar_reserva(self, animal: Animal):
        pass

    def finalizar_adocao(self, animal: Animal):
        pass

class Adocao:
    """
    Classe de Transação que formaliza a saída definitiva do Animal.
    
    É responsável por registrar a data da transação, o valor final da taxa cobrada
    e documentar qual Estratégia de cálculo foi aplicada.
    Contém a lógica para emissão do contrato final.
    """

    def __init__(self, animal: Animal, adotante: Adotante, taxa: float, estrategia_taxa: str):
        self.animal = animal
        self.adotante = adotante
        self.data_adocao = date.today()
        self.taxa = taxa
        self.estrategia_taxa = estrategia_taxa

    def emitir_contrato(self):
        pass
    
    def registrar_transacao_saida(self):
        pass

class Devolucao:
    """
    Classe de Transação que registra o retorno de um Animal após ter sido adotado.
    É responsável por documentar o motivo detalhado do retorno e por acionar o
    processo de reavaliação do Animal, ajustando seu status para DEVOLVIDO ou QUARENTENA.
    """
    def __init__(self, animal: Animal, adotante: Adotante, motivo: str):
        self.animal = animal
        self.adotante = adotante
        self.data_devolucao = date.today()
        self.motivo = motivo

    def registrar_evento(self):
        pass
    
    def ajustar_status_animal(self):
        pass

class Relatorios:
    """
    Classe de Serviço responsável por processar dados de persistência
    (Repository) para gerar métricas e informações consolidadas.
    
    Lida com o cálculo de taxas de adoção, o tempo médio de permanência
    e a identificação dos animais mais/menos adotados.
    """
    def __init__(self, tipo: str, filtros: dict):
        self.tipo = tipo
        self.filtros = filtros
        self.data_geracao = date.today()

    def processar_dados(self):
        pass

    def imprimir_relatorio(self):
        pass

class Reserva:
    """
    Classe de Transação que registra o bloqueio temporário (48h) de um Animal
    por um Adotante, controlando o prazo de expiração.
    """
    def __init__(self, animal: Animal, adotante: Adotante, data_reserva: date, data_expiracao: date):
        self.animal = animal
        self.adotante = adotante
        self.data_reserva = data_reserva
        self.data_expiracao = data_expiracao
        self.status = "ATIVA"

    def processar_confirmacao(self):
        pass

    def encerrar_reserva(self):
        pass
    
    def verificar_expiracao(self) -> bool:
        return date.today() > self.data_expiracao


class Cachorro(Animal):
    """
    Subclasse que herda de Animal, especializando atributos e comportamentos caninos,
    como a sociabilidade com outros pets.
    """
    def __init__(self, id: int, raca: str, nome: str, sexo: str, idade_meses: int, 
                porte: str, temperamento: List[str], sociavel_com_gatos: bool):
        
        super().__init__(id, "Cachorro", raca, nome, sexo, idade_meses, porte, temperamento)
        self.sociavel_com_gatos = sociavel_com_gatos

class Gato(Animal):
    """
    Subclasse que herda de Animal, especializando atributos e comportamentos felinos,
    como o uso da caixa de areia.
    """
    def __init__(self, id: int, raca: str, nome: str, sexo: str, idade_meses: int, 
                porte: str, temperamento: List[str], usa_caixa_areia: bool):
        
        super().__init__(id, "Gato", raca, nome, sexo, idade_meses, porte, temperamento)
        self.usa_caixa_areia = usa_caixa_areia


