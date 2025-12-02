import json
import os

class Repositorio:
    def __init__(self):
        # Garante que os arquivos sejam salvos na mesma pasta do script, independente de onde for executado
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.arquivo_animais = os.path.join(base_path, "database_animais.json")
        self.arquivo_adocoes = os.path.join(base_path, "database_adocoes.json")

    def salvar_dados(self, lista_animais, lista_adocoes):
        """Salva as listas de objetos em arquivos JSON."""
        
        
        dados_animais = [animal.to_dict() for animal in lista_animais]
        dados_adocoes = [adocao.to_dict() for adocao in lista_adocoes]

        
        with open(self.arquivo_animais, 'w', encoding='utf-8') as f:
            json.dump(dados_animais, f, indent=4, ensure_ascii=False)
            
        with open(self.arquivo_adocoes, 'w', encoding='utf-8') as f:
            json.dump(dados_adocoes, f, indent=4, ensure_ascii=False)
            
        print("💾 Dados salvos com sucesso!")

    def carregar_dados(self):
        """Carrega os dados para leitura."""
        if not os.path.exists(self.arquivo_animais):
            return []
            
        with open(self.arquivo_animais, 'r', encoding='utf-8') as f:
            return json.load(f)