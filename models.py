from datetime import date, datetime
from typing import List, Union
from abc import ABC, abstractmethod
from enum import Enum

# --- Enum para Status ---
class StatusAnimal(Enum):
    DISPONIVEL = "DISPONIVEL"
    RESERVADO = "RESERVADO"
    ADOTADO = "ADOTADO"
    DEVOLVIDO = "DEVOLVIDO"
    QUARENTENA = "QUARENTENA"
    INADOTAVEL = "INADOTAVEL"

# --- Exceções Customizadas ---
class ReservaInvalidaError(Exception):
    """Erro levantado quando uma reserva não pode ser feita."""
    pass

class PoliticaNaoAtendidaError(Exception):
    """Erro levantado quando o adotante não atende aos requisitos."""
    pass

class TransicaoDeEstadoInvalidaError(Exception):
    """Erro levantado ao tentar mudar para um status proibido."""
    pass

class RepositorioError(Exception):
    """Erro genérico para falhas no repositório de dados."""
    pass

# --- Classe Base (Herança) ---
class Pessoa(ABC):
    """Classe abstrata que representa uma pessoa genérica no sistema."""
    def __init__(self, id: int, nome: str, idade: int):
        self.id = id
        self.nome = nome
        self.idade = idade

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nome}>"

# --- Mixins (Herança Múltipla) ---
class VacinavelMixin:
    """Mixin para animais que podem ser vacinados."""
    def __init__(self):
        self.vacinas = []

    def vacinar(self, nome_vacina: str):
        self.vacinas.append({"nome": nome_vacina, "data": date.today().isoformat()})
        # Se a classe que usar isso tiver historico, adiciona lá também
        if hasattr(self, 'adicionar_evento'):
            self.adicionar_evento("Vacinação", f"Recebeu vacina: {nome_vacina}")

class AdestravelMixin:
    """Mixin para animais que podem ser treinados."""
    def __init__(self):
        self.nivel_adestramento = 0

    def treinar(self):
        self.nivel_adestramento += 1
        if hasattr(self, 'adicionar_evento'):
            self.adicionar_evento("Treinamento", f"Nível de adestramento subiu para {self.nivel_adestramento}")

# --- Padrão Strategy para Taxas ---
class EstrategiaTaxa(ABC):
    """Classe base abstrata para cálculo de taxas."""
    @abstractmethod
    def calcular(self, animal) -> float:
        pass

class TaxaPadrao(EstrategiaTaxa):
    def calcular(self, animal) -> float:
        return 50.0

class TaxaIdoso(EstrategiaTaxa):
    def calcular(self, animal) -> float:
        return 25.0 # Desconto para idosos

class TaxaFilhote(EstrategiaTaxa):
    def calcular(self, animal) -> float:
        return 60.0 # Mais caro por causa das vacinas iniciais

class TaxaEspecial(EstrategiaTaxa):
    def calcular(self, animal) -> float:
        return 30.0 # Valor simbólico para animais com necessidades especiais


class Evento:
    """
    Classe de dados simples que representa um registro de ocorrência no histórico do Animal.
    É responsável por armazenar a data, o tipo de evento (vacina, mudança de status)
    """
    def __init__(self, tipo: str, descricao: str):
        self.tipo = tipo
        self.descricao = descricao
        self.data = datetime.now()

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "descricao": self.descricao,
            "data": self.data.isoformat()
        }

class FilaEspera:
    """
    Encapsula a lógica de fila de espera com prioridade.
    Implementa __len__ para saber quantos estão na fila.
    """
    def __init__(self):
        self._candidatos = [] # Lista de dicionários

    def adicionar(self, adotante, score):
        """Adiciona um interessado na fila."""
        self._candidatos.append({
            "adotante": adotante,
            "score": score,
            "data_entrada": datetime.now()
        })

    def obter_proximo(self):
        """Retorna o candidato com maior prioridade (Score > Data) e remove da fila."""
        if not self._candidatos:
            return None
        
        # Ordena: Score decrescente, depois Data crescente (mais antigo primeiro)
        self._candidatos.sort(key=lambda x: (-x['score'], x['data_entrada']))
        
        return self._candidatos.pop(0) # Retorna o primeiro da lista ordenada

    def __len__(self):
        return len(self._candidatos)

    def __bool__(self):
        return len(self._candidatos) > 0


class Animal(VacinavelMixin):
    """
    Representa a entidade principal do sistema: o animal disponível para adoção.
    """
    def __init__(self, id: int, especie: str, raca: str, nome: str, sexo: str, 
                idade_meses: int, porte: str, temperamento: List[str]):
        super().__init__() # Inicializa o VacinavelMixin
        self.id = id
        self.especie = especie
        self.raca = raca
        self.nome = nome
        self.sexo = sexo
        self.idade_meses = idade_meses
        self.porte = porte
        self.temperamento = temperamento
        
        self._status = StatusAnimal.DISPONIVEL
        self.data_entrada = date.today()
        self.historico: List[Evento] = []
        self.fila_espera = FilaEspera() # Usa a classe customizada
        self.reserva_ativa = None # Armazena o objeto Reserva atual

    def __iter__(self):
        """Permite iterar diretamente sobre o histórico do animal."""
        return iter(self.historico)

    @property
    def status(self):
        """Retorna o valor string do status atual."""
        return self._status.value

    def mudar_status(self, novo_status: Union[str, StatusAnimal]):
        """Altera o status do animal e registra no histórico, com validação via Enum."""
        if isinstance(novo_status, str):
            try:
                novo_status = StatusAnimal(novo_status.upper())
            except ValueError:
                raise TransicaoDeEstadoInvalidaError(f"Status '{novo_status}' não existe.")
        
        if not isinstance(novo_status, StatusAnimal):
             raise TransicaoDeEstadoInvalidaError("Status inválido.")

        # --- Máquina de Estados (Regras de Transição) ---
        atual = self._status
        
        # Regras permitidas (origem -> destinos permitidos)
        transicoes_permitidas = {
            StatusAnimal.DISPONIVEL: [StatusAnimal.RESERVADO, StatusAnimal.INADOTAVEL, StatusAnimal.ADOTADO], # ADOTADO direto permitido? Sim.
            StatusAnimal.RESERVADO: [StatusAnimal.ADOTADO, StatusAnimal.DISPONIVEL], # Pode cancelar reserva
            StatusAnimal.ADOTADO: [StatusAnimal.DEVOLVIDO, StatusAnimal.QUARENTENA], # Permitir Quarentena direto se doente
            StatusAnimal.DEVOLVIDO: [StatusAnimal.QUARENTENA, StatusAnimal.DISPONIVEL, StatusAnimal.INADOTAVEL],
            StatusAnimal.QUARENTENA: [StatusAnimal.DISPONIVEL, StatusAnimal.INADOTAVEL],
            StatusAnimal.INADOTAVEL: [StatusAnimal.DISPONIVEL] # Pode voltar a ser adotável? Sim.
        }

        if novo_status not in transicoes_permitidas.get(atual, []):
             # Permite manter o mesmo status (idempotência)
             if novo_status != atual:
                raise TransicaoDeEstadoInvalidaError(f"Transição inválida: De {atual.value} para {novo_status.value}")

        evento = Evento("Mudança de Status", f"De {self._status.value} para {novo_status.value}")
        self.historico.append(evento)
        self._status = novo_status

    def __repr__(self):
        return f"<Animal {self.nome} id={self.id}>"

    def __eq__(self, other):
        if isinstance(other, Animal):
            return self.id == other.id
        return False

    def __lt__(self, other):
        # Ordenação por data de entrada (mais antigos primeiro)
        return self.data_entrada < other.data_entrada

    def aplicar_vacina(self, vacina: str):
        self.adicionar_evento("Vacina", f"Aplicação de: {vacina}")

    def adicionar_evento(self, tipo: str, descricao: str):
        """Método auxiliar para adicionar eventos ao histórico."""
        novo_evento = Evento(tipo, descricao)
        self.historico.append(novo_evento)

    def get_resumo(self) -> str:
        return f"[{self.status}] {self.nome} - {self.especie}"
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            "id": self.id,
            "especie": self.especie,
            "raca": self.raca,
            "nome": self.nome,
            "sexo": self.sexo,
            "idade_meses": self.idade_meses,
            "porte": self.porte,
            "temperamento": self.temperamento,
            "status": self.status,
            "historico": [e.to_dict() for e in self.historico]
        }

class Adocao:
    """
    Classe de Transação que formaliza a saída definitiva do Animal.
    
    É responsável por registrar a data da transação, o valor final da taxa cobrada
    e documentar qual Estratégia de cálculo foi aplicada.
    Contém a lógica para emissão do contrato final.
    """

    def __init__(self, animal: Animal, adotante: 'Adotante', taxa: float, estrategia_taxa: str = "PADRAO"):
        self.animal = animal
        self.adotante = adotante
        self.data_adocao = date.today()
        self.taxa = taxa
        self.estrategia_taxa = estrategia_taxa

    def to_dict(self):
        return {
            "animal": self.animal.nome,
            "adotante": self.adotante.nome,
            "data": self.data_adocao.isoformat(),
            "taxa": self.taxa
        }

    def emitir_contrato(self):
        return f"""
        ================ CONTRATO DE ADOÇÃO ================
        DATA: {self.data_adocao.strftime('%d/%m/%Y')}
        
        PARTES:
        ADOTANTE: {self.adotante.nome} (ID: {self.adotante.id})
        ANIMAL: {self.animal.nome} - {self.animal.especie} (ID: {self.animal.id})
        
        TERMOS:
        1. O adotante compromete-se a cuidar do animal com zelo.
        2. O animal não poderá ser abandonado. Em caso de desistência,
        deve ser devolvido a esta instituição.
        3. O adotante declara estar ciente das necessidades do animal.
        
        TAXA DE ADOÇÃO: R$ {self.taxa:.2f} ({self.estrategia_taxa})
        
        _____________________________      _____________________________
        Assinatura do Adotante             Assinatura do Responsável
        ====================================================
        """
    
    def registrar_transacao_saida(self):
        pass

class Reserva:
    """
    Classe de Transação que registra o bloqueio temporário (48h) de um Animal
    por um Adotante, controlando o prazo de expiração.
    """
    def __init__(self, animal: Animal, adotante: 'Adotante', data_reserva: date = None, data_expiracao: date = None):
        self.animal = animal
        self.adotante = adotante
        self.data_reserva = data_reserva or date.today()
        # Reserva expira em 2 dias por padrão
        self.data_expiracao = data_expiracao or date.fromordinal(self.data_reserva.toordinal() + 2)
        self.status = "ATIVA"

    def to_dict(self):
        return {
            "animal": self.animal.nome,
            "adotante": self.adotante.nome,
            "data": self.data_reserva.isoformat(),
            "status": self.status
        }

    def processar_confirmacao(self):
        pass

    def encerrar_reserva(self):
        pass
    
    def verificar_expiracao(self) -> bool:
        return date.today() > self.data_expiracao

class Adotante(Pessoa):
    """
    Representa a pessoa que solicita uma adoção.
    É responsável por armazenar os dados utilizados na Triagem de adotantes (idade,
    moradia, área útil e experiência com pets). Contém a lógica inicial para
    verificar a elegibilidade conforme o sistema.
    """
    def __init__(self, id: int, nome: str, idade: int, moradia: str, area_util: float, 
                outros_animais: bool, experiencia_pets: bool, possui_criancas: bool):
        super().__init__(id, nome, idade)
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


    def solicitar_reserva(self, animal: Animal, horas_validade: int = 48) -> Reserva:
        if animal.status != "DISPONIVEL":
            raise ValueError("Animal não está disponível para reserva.")
        
        animal.mudar_status(StatusAnimal.RESERVADO)
        
        # Calcula expiração baseada nas horas passadas
        data_reserva = datetime.now()
        # Usando timedelta para precisão de horas, mas mantendo compatibilidade com date se necessário
        # O modelo Reserva original usava date, vamos adaptar para datetime ou manter date + dias
        
        # Se a classe Reserva espera date, convertemos horas para dias (arredondando para cima)
        dias = max(1, int(horas_validade / 24))
        data_exp = date.fromordinal(date.today().toordinal() + dias)
        
        nova_reserva = Reserva(animal, self, date.today(), data_exp)
        return nova_reserva

    def finalizar_adocao(self, animal: Animal, taxa: float, estrategia_nome: str = "PADRAO") -> Adocao:
        """Cria uma relação de Adoção e finaliza o processo."""
        if animal.status not in ["DISPONIVEL", "RESERVADO"]:
            raise ValueError("Status inválido para adoção.")
            
        animal.mudar_status("ADOTADO")
        nova_adocao = Adocao(animal, self, taxa, estrategia_nome)
        return nova_adocao

    def verificar_elegibilidade(self, animal: Animal = None) -> bool:
        """
        Usa os dados encapsulados para determinar se o adotante é elegível.
        Regras:
        1. Maior de 18 anos.
        2. Se tiver crianças, precisa ter experiência prévia.
        3. Se o animal for Grande, não pode morar em Apartamento pequeno.
        """
        # Regra 1: Idade Mínima
        if self.idade < 18:
            print(f"❌ Reprovado: Adotante menor de idade ({self.idade} anos).")
            return False

        # Regra 2: Crianças vs Experiência
        if self._possui_criancas and not self._experiencia_pets:
            print("❌ Reprovado: Possui crianças mas não tem experiência com pets.")
            return False 
        
        # Regra 3: Porte vs Moradia
        if animal:
            # Exige moradia "Casa" para animais de grande porte
            if animal.porte == "G":
                if self.moradia.lower() != "casa":
                    print("❌ Reprovado: Animais de grande porte exigem moradia em Casa.")
                    return False
                # Se for Casa, verifica área mínima (ex: 80m2)
                if self.area_util < 80:
                    print("❌ Reprovado: Área útil insuficiente para animal de grande porte.")
                    return False

        return True
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "moradia": self.moradia,
            "area_util": self.area_util,
            "outros_animais": self.outros_animais,
            "experiencia_pets": self.experiencia_pets,
            "possui_criancas": self.possui_criancas
        }

    def __str__(self):
        return f"[{self.id}] {self.nome} - {self.moradia}"

    def __eq__(self, other):
        if isinstance(other, Adotante):
            return self.id == other.id
        return False

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
    para gerar métricas e informações consolidadas.
    """
    @staticmethod
    def top_5_adotaveis(animais, adotantes, func_compatibilidade):
        """Retorna os 5 animais com maior média de compatibilidade com os adotantes cadastrados."""
        ranking = []
        for animal in animais:
            if animal.status == 'DISPONIVEL':
                scores = [func_compatibilidade(animal, ad) for ad in adotantes]
                media = sum(scores) / len(scores) if scores else 0
                ranking.append({"nome": animal.nome, "media": media, "especie": animal.especie})
        
        # Ordena pela média decrescente
        return sorted(ranking, key=lambda x: x['media'], reverse=True)[:5]

    @staticmethod
    def tempo_medio_adocao(adocoes):
        """Calcula o tempo médio (em dias) entre a entrada e a adoção."""
        if not adocoes:
            return 0.0
            
        total_dias = 0
        for adocao in adocoes:
            # Garante que as datas sejam do tipo date
            d_adocao = adocao.data_adocao
            d_entrada = adocao.animal.data_entrada
            
            # Se for datetime, converte para date
            if isinstance(d_adocao, datetime): d_adocao = d_adocao.date()
            if isinstance(d_entrada, datetime): d_entrada = d_entrada.date()
                
            delta = d_adocao - d_entrada
            total_dias += delta.days
            
        return total_dias / len(adocoes)

    @staticmethod
    def taxa_adocoes_por_tipo(adocoes):
        """Retorna a contagem de adoções agrupada por Espécie e Porte."""
        stats = {}
        total = len(adocoes)
        if total == 0: return {}

        for adocao in adocoes:
            chave = f"{adocao.animal.especie} ({adocao.animal.porte})"
            stats[chave] = stats.get(chave, 0) + 1
            
        # Converte para porcentagem
        return {k: f"{(v/total)*100:.1f}% ({v})" for k, v in stats.items()}

    @staticmethod
    def devolucoes_por_motivo(animais):
        """Analisa o histórico de todos os animais buscando devoluções."""
        motivos = {}
        for animal in animais:
            for evento in animal.historico:
                if evento.tipo == "Devolução":
                    # Extrai o motivo da string "Motivo: XXXXX"
                    motivo_texto = evento.descricao.replace("Motivo: ", "")
                    motivos[motivo_texto] = motivos.get(motivo_texto, 0) + 1
        return motivos


class Cachorro(Animal, AdestravelMixin):
    """
    Subclasse que herda de Animal, especializando atributos e comportamentos caninos,
    """
    def __init__(self, id: int, raca: str, nome: str, sexo: str, idade_meses: int, 
                porte: str, temperamento: List[str], sociavel_com_gatos: bool):
        
        Animal.__init__(self, id, "Cachorro", raca, nome, sexo, idade_meses, porte, temperamento)
        AdestravelMixin.__init__(self) # Inicializa o mixin
        self.sociavel_com_gatos = sociavel_com_gatos

class Gato(Animal):
    """
    Subclasse que herda de Animal, especializando atributos e comportamentos felinos
    """
    def __init__(self, id: int, raca: str, nome: str, sexo: str, idade_meses: int, 
                porte: str, temperamento: List[str], usa_caixa_areia: bool):
        
        super().__init__(id, "Gato", raca, nome, sexo, idade_meses, porte, temperamento)
        self.usa_caixa_areia = usa_caixa_areia


