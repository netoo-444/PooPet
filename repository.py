import json
import os
from models import RepositorioError

class Repositorio:
    def __init__(self):
        # Garante que os arquivos sejam salvos na mesma pasta do script, independente de onde for executado
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.arquivo_animais = os.path.join(base_path, "database_animais.json")
        self.arquivo_adocoes = os.path.join(base_path, "database_adocoes.json")
        self.arquivo_adotantes = os.path.join(base_path, "database_adotantes.json")

    def salvar_dados(self, lista_animais, lista_adocoes, lista_adotantes):
        """Salva as listas de objetos em arquivos JSON."""
        try:
            dados_animais = [animal.to_dict() for animal in lista_animais]
            dados_adocoes = [adocao.to_dict() for adocao in lista_adocoes]
            dados_adotantes = [adotante.to_dict() for adotante in lista_adotantes]

            with open(self.arquivo_animais, 'w', encoding='utf-8') as f:
                json.dump(dados_animais, f, indent=4, ensure_ascii=False)
                
            with open(self.arquivo_adocoes, 'w', encoding='utf-8') as f:
                json.dump(dados_adocoes, f, indent=4, ensure_ascii=False)

            with open(self.arquivo_adotantes, 'w', encoding='utf-8') as f:
                json.dump(dados_adotantes, f, indent=4, ensure_ascii=False)
                
            print("💾 Dados salvos com sucesso!")
        except IOError as e:
            raise RepositorioError(f"Falha ao escrever no disco: {e}")
        except Exception as e:
            raise RepositorioError(f"Erro inesperado ao salvar: {e}")

    def carregar_dados(self):
        """Carrega os dados de animais para leitura."""
        if not os.path.exists(self.arquivo_animais):
            return []
            
        try:
            with open(self.arquivo_animais, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise RepositorioError("Arquivo de dados de animais corrompido.")
        except IOError as e:
            raise RepositorioError(f"Erro ao ler arquivo de animais: {e}")

    def carregar_adocoes(self):
        """Carrega os dados de adoções para leitura."""
        if not os.path.exists(self.arquivo_adocoes):
            return []
            
        try:
            with open(self.arquivo_adocoes, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise RepositorioError("Arquivo de dados de adoções corrompido.")
        except IOError as e:
            raise RepositorioError(f"Erro ao ler arquivo de adoções: {e}")

    def carregar_adotantes(self):
        """Carrega os dados de adotantes para leitura."""
        if not os.path.exists(self.arquivo_adotantes):
            return []
            
        try:
            with open(self.arquivo_adotantes, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise RepositorioError("Arquivo de dados de adotantes corrompido.")
        except IOError as e:
            raise RepositorioError(f"Erro ao ler arquivo de adotantes: {e}")