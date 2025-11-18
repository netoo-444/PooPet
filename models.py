class Animal:
        """
    Representa a entidade principal do sistema: o animal disponível para adoção.
    É responsável por armazenar dados de cadastro (espécie, porte, temperamento),
    gerenciar seu status através de regras de transição e registrar a cronologia completa de eventos (vacinas, mudanças de status)
    em seu histórico. Serve como classe base para Cachorro e Gato.
    """
        pass

class Adotante:
    """
    Representa a pessoa que solicita uma adoção.
    É responsável por armazenar os dados utilizados na Triagem de adotantes (idade,
    moradia, área útil e experiência com pets). Contém a lógica inicial para
    verificar a elegibilidade conforme o sistema.
    """
    pass

class Adocao:
    """
    Classe de Transação que formaliza a saída definitiva do Animal.
    
    É responsável por registrar a data da transação, o valor final da taxa cobrada
    e documentar qual Estratégia de cálculo foi aplicada.
    Contém a lógica para emissão do contrato final.
    """

    pass

class Devolucao:
    """
    Classe de Transação que registra o retorno de um Animal após ter sido adotado.
    É responsável por documentar o motivo detalhado do retorno e por acionar o
    processo de reavaliação do Animal, ajustando seu status para DEVOLVIDO ou QUARENTENA.
    """
    pass

class Relatorios:
    """
    Classe de Serviço responsável por processar dados de persistência
    (Repository) para gerar métricas e informações consolidadas.
    
    Lida com o cálculo de taxas de adoção, o tempo médio de permanência
    e a identificação dos animais mais/menos adotados.
    """
    pass

class Reserva:
    """
    Classe de Transação que registra o bloqueio temporário (48h) de um Animal
    por um Adotante, controlando o prazo de expiração.
    """
    pass

class Evento:
    """
    Classe de dados simples que representa um registro de ocorrência no histórico do Animal.
    É responsável por armazenar a data, o tipo de evento (vacina, mudança de status)
    """
    pass

class Cachorro(Animal):
    """
    Subclasse que herda de Animal, especializando atributos e comportamentos caninos,
    como a sociabilidade com outros pets.
    """
    pass

class Gato(Animal):
    """
    Subclasse que herda de Animal, especializando atributos e comportamentos felinos,
    como o uso da caixa de areia.
    """
    pass


