# PooPet ![Python Logo](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 

---

# 🐕 Sistema de Adoção de Animais
## 📋 Descrição do Projeto

Sistema desenvolvido para gerenciar o processo completo de adoção de animais, incluindo cadastro, triagem de adotantes, reservas, adoções, devoluções e geração de relatórios. O projeto implementa rigorosamente a **Programação Orientada a Objetos (POO)**, utilizando herança múltipla, mixins, encapsulamento e padrões de design (Strategy, State, Repository).

## Objetivo 🎯

Implementar uma solução em Python que permita o controle eficiente de animais disponíveis para adoção, garantindo compatibilidade entre adotantes e animais através de políticas configuráveis e regras de negócio bem definidas (como filas de espera priorizadas), junto com seus relatórios estatísticos.

---

## 3. Estrutura de Classes Implementada (UML Textual)

### A. Classes, Atributos e Métodos Principais

| Classe | Atributos Principais | Métodos Principais |
| :--- | :--- | :--- |
| **Animal** (Abstrata) | `id`, `especie`, `nome`, `raca`, `sexo`, `idade`, `porte`, `temperamento`, **`_status: StatusAnimal`** (Enum), `historico`, **`fila_espera: FilaEspera`** | `mudar_status()`, `adicionar_evento()`, `__iter__()` (itera histórico) |
| **Cachorro** | `sociavel_com_gatos: bool` | **(Herda de Animal + AdestravelMixin)** |
| **Gato** | `usa_caixa_areia: bool` | **(Herda de Animal)** |
| **Adotante** | `id`, `nome`, `idade`, `moradia`, `area_util`, **`_experiencia_pets`** (Property), **`_possui_criancas`** (Property) | `verificar_elegibilidade()`, `solicitar_reserva()`, `finalizar_adocao()` |
| **Reserva** | `animal`, `adotante`, `data_reserva`, `data_expiracao` | `verificar_expiracao()` |
| **Adocao** | `animal`, `adotante`, `data_adocao`, `taxa`, **`estrategia: EstrategiaTaxa`** | `emitir_contrato()`, `registrar_transacao_saida()` |
| **FilaEspera** | `candidatos: list` | `adicionar()`, `obter_proximo()` (Prioriza por Score), `__len__()` |
| **Mixins** | `VacinavelMixin`, `AdestravelMixin` | `vacinar()`, `treinar()` |

### B. Relacionamentos e Padrões

| Classe Origem | Relação | Classe Destino | Descrição |
| :--- | :--- | :--- | :--- |
| **Cachorro** | Herança Múltipla | **Animal, AdestravelMixin** | Cães herdam comportamento base e capacidade de treino. |
| **Animal** | Composição | **FilaEspera** | Cada animal gerencia sua própria fila de interessados. |
| **Animal** | State (Enum) | **StatusAnimal** | Controle rígido de transições (`DISPONIVEL` -> `RESERVADO`). |
| **Adocao** | Strategy | **EstrategiaTaxa** | Cálculo dinâmico de taxa (`TaxaIdoso`, `TaxaFilhote`, etc.). |
| **Adotante** | Associação | **Reserva** | Um adotante pode fazer reservas. |
| **Sistema** | Repository | **Repositorio** | Isolamento da camada de persistência JSON. |

---

## 🛠️ Tecnologias e Dependências

### 🐍 Linguagem e Ambiente

* **Python 3.x**: Linguagem principal, utilizada para a implementação da Programação Orientada a Objetos (POO).
* **CLI (Terminal)**: A interface de execução primária para as interações do usuário (`app.py`).

### 💾 Persistência

* **JSON**: Formato de arquivo utilizado para a persistência de dados (`database_animais.json`, `database_adocoes.json`, `database_adotantes.json`).
* **Settings**: Configurações de negócio (pesos de compatibilidade, tempo de reserva) externas em `settings.json`.

---

## 🚀 Como Executar o PooPet

Siga os passos abaixo para clonar e rodar o Sistema de Adoção de Animais **PooPet** na sua máquina.

### 1. Clone o Repositório

Abra o seu terminal ou prompt de comando:

```bash
# Clone o repositório oficial
git clone https://github.com/netoo-444/PooPet.git

# Entre na pasta do projeto
cd PooPet
