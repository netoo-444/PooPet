from models import Cachorro, Gato, Adotante, TaxaPadrao, TaxaIdoso, TaxaFilhote, TaxaEspecial, Relatorios, Adocao, StatusAnimal, RepositorioError
from repository import Repositorio
import json
import os
from datetime import datetime

class SistemaAdocao:
    def __init__(self):
        self.repo = Repositorio()
        self.animais = []
        self.adotantes = []
        self.adocoes = []
        self.config = self._carregar_configuracoes()
        
            # Carrega dados existentes
        try:
            self._carregar_do_arquivo()
        except RepositorioError as e:
            print(f"⚠️ Erro crítico ao carregar dados: {e}")

    def _carregar_configuracoes(self):
        """Lê o arquivo settings.json"""
        try:
            caminho = os.path.join(os.path.dirname(__file__), 'settings.json')
            with open(caminho, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def calcular_compatibilidade(self, animal, adotante):
        """Calcula score de 0 a 100 baseado nas configurações."""
        score = 50 # Base inicial
        pesos = self.config.get('pesos_compatibilidade', {})
        
        # 1. Regra de Moradia vs Porte
        if adotante.moradia.lower() == 'casa':
            score += pesos.get('moradia_casa', 10)
        elif adotante.moradia.lower() == 'apartamento':
            if adotante.area_util < 50 and animal.porte == 'G':
                score -= 20 # Penalidade forte para animal grande em apto pequeno
            elif adotante.area_util < 50:
                score += pesos.get('moradia_apto_pequeno', -10)
            
        # 2. Regra de Experiência
        if adotante.experiencia_pets:
            score += pesos.get('experiencia', 10)
            
        # 3. Regra de Crianças vs Temperamento
        if adotante.possui_criancas:
            
            temperamentos_ruins = ["agitado", "arisco", "bravo", "raivoso", "agressivo", "nervoso", "independente", "assustado"]
            # Lista de temperamentos ideais
            temperamentos_bons = ["dócil", "calmo", "amoroso", "carinhoso", "fofo", "paciente"]
            
            temps_animal = [t.lower() for t in animal.temperamento]
            
            if any(t in temperamentos_ruins for t in temps_animal):
                score -= 30 # Penalidade alta
            elif any(t in temperamentos_bons for t in temps_animal):
                score += 15 # Bônus

    
        if adotante.idade > 60:
            if animal.idade_meses < 24:
                score -= 15 # Idoso com filhote pode ser difícil
            elif animal.idade_meses > 60:
                score += 15 # Idoso com animal adulto/idoso é match perfeito

        # Normaliza para 0-100
        return max(0, min(100, score))

    def _carregar_do_arquivo(self):
        """Tenta carregar dados do JSON e converter para objetos."""
        dados_animais = self.repo.carregar_dados()
        
        
        if dados_animais:
            for item in dados_animais:
                raca = item.get('raca', 'SRD')
                sexo = item.get('sexo', 'M')
                idade = item.get('idade_meses', 0)
                porte = item.get('porte', 'M')
                temperamento = item.get('temperamento', [])
                
                if 'especie' not in item:
                    print(f"⚠️ Item corrompido ignorado (sem espécie): {item}")
                    continue

                if item['especie'] == "Cachorro":
                    # Assumindo True para sociavel_com_gatos se não existir
                    animal = Cachorro(item['id'], raca, item['nome'], sexo, idade, porte, temperamento, True)
                else:
                    # Assumindo True para usa_caixa_areia se não existir
                    animal = Gato(item['id'], raca, item['nome'], sexo, idade, porte, temperamento, True)
                
                # Restaura o status salvo
                if item['status'] != "DISPONIVEL":
                    try:
                        animal._status = StatusAnimal(item['status']) # Define Enum diretamente
                    except ValueError:
                        animal._status = StatusAnimal.DISPONIVEL
                
                self.animais.append(animal)

        # Carregar Adotantes 
        dados_adotantes = self.repo.carregar_adotantes()
        if dados_adotantes:
            for item in dados_adotantes:
                try:
                    adotante = Adotante(
                        item['id'], item['nome'], item['idade'], item['moradia'], 
                        item['area_util'], item['outros_animais'], 
                        item['experiencia_pets'], item['possui_criancas']
                    )
                    self.adotantes.append(adotante)
                except KeyError:
                    print(f"⚠️ Adotante corrompido ignorado: {item}")

        # Carregar Adoções
        dados_adocoes = self.repo.carregar_adocoes()
        if dados_adocoes:
            for item in dados_adocoes:
                # Tenta encontrar o animal pelo nome (já que não salvamos ID na adoção)
                animal_obj = next((a for a in self.animais if a.nome == item['animal']), None)
                
                if animal_obj:
                    # Tenta encontrar o adotante pelo nome
                    adotante_obj = next((a for a in self.adotantes if a.nome == item['adotante']), None)
                    
                    # Se não achar, cria um temporário (legado)
                    if not adotante_obj:
                        adotante_obj = Adotante(0, item['adotante'], 0, "", 0, False, False, False)
                    
                    adocao = Adocao(animal_obj, adotante_obj, item['taxa'])
                    # Converte string ISO para date
                    try:
                        adocao.data_adocao = datetime.fromisoformat(item['data']).date()
                    except ValueError:
                        pass 
                        
                    self.adocoes.append(adocao)

        return True

    def _carregar_dados_iniciais(self):
        if not self.animais:
            rex = Cachorro(1, "Vira-lata", "Rex", "M", 12, "M", ["Dócil"], True)
            self.animais.append(rex)
        
        if not self.adotantes:
            joao = Adotante(1, "Joao Silva", 25, "Casa", 100.0, False, True, False)
            self.adotantes.append(joao)

    def cadastrar_animal(self, tipo, nome, raca="SRD", sexo="M", idade=0, porte="M", especial=False, temperamento=None, info_extra=True):
        id_novo = len(self.animais) + 1
        
        if temperamento is None:
            temperamento = []

        if tipo == "CACHORRO":
            novo_animal = Cachorro(id_novo, raca, nome, sexo, idade, porte, temperamento, info_extra)
        else:
            novo_animal = Gato(id_novo, raca, nome, sexo, idade, porte, temperamento, info_extra)
        
        # Atributo dinâmico para controle de taxa especial
        novo_animal.tratamento_especial = especial
        
        # Registra evento de entrada
        novo_animal.adicionar_evento("Entrada", "Animal cadastrado no sistema.")

        self.animais.append(novo_animal)
        return novo_animal

    def cadastrar_adotante(self, nome, idade, moradia, area_util, outros_animais, experiencia_pets, possui_criancas):
        novo_adotante = Adotante(len(self.adotantes)+1, nome, idade, moradia, area_util, outros_animais, experiencia_pets, possui_criancas)
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

    def buscar_animal_por_id(self, id_animal):
        """Busca animal pelo ID (independente do status)."""
        for animal in self.animais:
            if animal.id == id_animal:
                return animal
        return None

    def reservar_animal(self, indice_adotante, indice_animal):
        """Realiza a reserva de um animal ou coloca na fila de espera."""
        adotante = self.buscar_adotante(indice_adotante)
        animal = self.buscar_animal_disponivel(indice_animal)
        if not animal:
            # Tenta buscar por ID direto na lista geral (caso esteja reservado)
            try:
                animal = self.animais[indice_animal] 
            except IndexError:
                return False, "Animal inválido."

        if not adotante:
            return False, "Adotante inválido."

       
        if animal.status == "RESERVADO":
            # Verifica se já não é o dono da reserva atual
            if animal.reserva_ativa and animal.reserva_ativa.adotante.id == adotante.id:
                return False, "⚠️ Você já possui a reserva ativa deste animal."
            
            
            score = self.calcular_compatibilidade(animal, adotante)
            
            
            animal.fila_espera.adicionar(adotante, score)
            
            return True, f"⏳ Animal reservado. {adotante.nome} entrou na fila de espera (Posição definida por compatibilidade: {score}/100)."

        try:
            horas = self.config.get('reserva_horas', 48)
            reserva = adotante.solicitar_reserva(animal, horas_validade=horas)
            
            animal.reserva_ativa = reserva # Vincula a reserva ao animal
            return True, f"Reserva realizada com sucesso para {animal.nome}! Vence em: {reserva.data_expiracao}"
        except Exception as e:
            return False, f"Erro na reserva: {str(e)}"

    def processar_expiracoes(self):
        """Verifica reservas vencidas e passa para o próximo da fila (por prioridade)."""
        log = []
        agora = datetime.now()
        
        for animal in self.animais:
            if animal.status == "RESERVADO" and animal.reserva_ativa:
                if animal.reserva_ativa.verificar_expiracao():
                    log.append(f"Reserva de {animal.nome} expirou.")
                    animal.reserva_ativa = None # Remove a reserva vencida
                    
                    if animal.fila_espera:
                        # Usa o método da classe FilaEspera para pegar o melhor candidato
                        melhor_candidato = animal.fila_espera.obter_proximo()
                        
                        proximo_adotante = melhor_candidato['adotante']
                        score_proximo = melhor_candidato['score']
                        
                        # Cria nova reserva automaticamente
                        horas = self.config.get('reserva_horas', 48)
                        nova_reserva = proximo_adotante.solicitar_reserva(animal, horas_validade=horas) 
                        animal.reserva_ativa = nova_reserva
                        
                        log.append(f"Animal realocado para {proximo_adotante.nome} da fila de espera (Score: {score_proximo}). Nova expiração: {nova_reserva.data_expiracao}")
                    else:
                        animal.mudar_status("DISPONIVEL")
                        log.append(f"{animal.nome} voltou a ficar DISPONIVEL.")
                else:
                    log.append(f"Reserva de {animal.nome} ainda válida até {animal.reserva_ativa.data_expiracao}.")
        
        if not log:
            return ["Nenhuma reserva expirada encontrada."]
        return log



    def processar_adocao(self, indice_adotante, indice_animal):
        adotante = self.buscar_adotante(indice_adotante)
        animal = self.buscar_animal_disponivel(indice_animal)

        if not adotante:
            return False, "❌ Adotante inválido."
        if not animal:
            return False, "❌ Animal inválido."

        # Validação de Regras
        if adotante.verificar_elegibilidade(animal):
            # Verifica compatibilidade
            score = self.calcular_compatibilidade(animal, adotante)
            if score < 30: # Nota de corte arbitrária
                return False, f"❌ Compatibilidade muito baixa ({score}). Adoção não recomendada."

            # Define estratégia de taxa
            nome_estrategia = "PADRAO"
            if getattr(animal, 'tratamento_especial', False):
                estrategia = TaxaEspecial()
                nome_estrategia = "ESPECIAL"
            elif animal.idade_meses < 6:
                estrategia = TaxaFilhote()
                nome_estrategia = "FILHOTE"
            elif animal.idade_meses > 8 * 12: # 8 anos
                estrategia = TaxaIdoso()
                nome_estrategia = "IDOSO"
            else:
                estrategia = TaxaPadrao()
            
            valor_taxa = estrategia.calcular(animal)

            try:
                adocao = adotante.finalizar_adocao(animal, taxa=valor_taxa, estrategia_nome=nome_estrategia)
                self.adocoes.append(adocao)
                
                # Imprime o contrato no console
                print(adocao.emitir_contrato())
                
                return True, f"🎉 Sucesso! {animal.nome} foi adotado por {adotante.nome}! Taxa: R${valor_taxa:.2f}"
            except Exception as e:
                return False, f"Erro ao processar: {str(e)}"
        
        return False, "❌ Adotante não elegível."

    def listar_animais_por_status(self, status):
        """Retorna lista de animais com um status específico."""
        return [a for a in self.animais if a.status == status]

    def processar_devolucao(self, indice_animal_adotado, motivo):
        """Registra a devolução de um animal adotado."""
        adotados = self.listar_animais_por_status("ADOTADO")
        
        if 0 <= indice_animal_adotado < len(adotados):
            animal = adotados[indice_animal_adotado]
            novo_status = "QUARENTENA" if "doente" in motivo.lower() else "DEVOLVIDO"
            
            try:
                animal.mudar_status(novo_status)
                # Adiciona evento extra com o motivo
                if hasattr(animal, 'adicionar_evento'):
                    animal.adicionar_evento("Devolução", f"Motivo: {motivo}")
                return True, f"⚠️ {animal.nome} foi devolvido e está agora como {novo_status}."
            except Exception as e:
                return False, f"Erro ao mudar status: {e}"
        
        return False, "❌ Animal inválido."

    def alterar_status_manual(self, indice_geral, novo_status):
        """Permite ao admin mudar o status (ex: Quarentena -> Disponivel)."""
        if 0 <= indice_geral < len(self.animais):
            animal = self.animais[indice_geral]
            try:
                animal.mudar_status(novo_status)
                return True, f"✅ Status de {animal.nome} alterado para {novo_status}."
            except Exception as e:
                return False, f"Erro: {e}"
        return False, "❌ Índice inválido."

    def registrar_vacina(self, indice_animal, tipo_vacina):
        """Registra vacina em qualquer animal (disponível ou não)."""
        if 0 <= indice_animal < len(self.animais):
            animal = self.animais[indice_animal]
            if hasattr(animal, 'vacinar'):
                animal.vacinar(tipo_vacina)
                return True, f"💉 {animal.nome} foi vacinado contra {tipo_vacina}."
            return False, "❌ Este animal não pode ser vacinado."
        return False, "❌ Índice inválido."

    def registrar_treino(self, indice_animal):
        """Registra treino apenas em cachorros."""
        if 0 <= indice_animal < len(self.animais):
            animal = self.animais[indice_animal]
            if hasattr(animal, 'treinar'):
                animal.treinar()
                return True, f"🎓 {animal.nome} completou uma sessão de adestramento."
            return False, "❌ Apenas cachorros podem ser adestrados."
        return False, "❌ Índice inválido."

    def salvar_dados(self):
        try:
            self.repo.salvar_dados(self.animais, self.adocoes, self.adotantes)
        except RepositorioError as e:
            print(f"❌ Erro ao salvar: {e}")

    def gerar_relatorios(self):
        """Gera um dicionário com todos os relatórios do sistema."""
        
        top5 = []
        if self.adotantes:
            # Calcula compatibilidade média para cada animal disponível
            for animal in self.listar_animais_disponiveis():
                scores = [self.calcular_compatibilidade(animal, ad) for ad in self.adotantes]
                media = sum(scores) / len(scores) if scores else 0
                top5.append({"nome": animal.nome, "especie": animal.especie, "score_medio": media})
            
            # Ordena e pega os 5 melhores
            top5 = sorted(top5, key=lambda x: x['score_medio'], reverse=True)[:5]

        return {
            "top5": top5,
            "tempo_medio": Relatorios.tempo_medio_adocao(self.adocoes),
            "taxa_tipo": Relatorios.taxa_adocoes_por_tipo(self.adocoes),
            "devolucoes": Relatorios.devolucoes_por_motivo(self.animais)
        }
