# PooPet ![Python Logo](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 

---

# 🐕 Sistema de Adoção de Animais
## 📋 Descrição do Projeto

Sistema desenvolvido para gerenciar o processo completo de adoção de animais, incluindo cadastro, triagem de adotantes, reservas, adoções, devoluções e geração de relatórios. O projeto implementará a Programação Orientada a Objetos (POO), incluindo herança, encapsulamento e padrões de design, conforme os Requisitos Técnicos.

## Objetivo 🎯

Implementar uma solução em Python que permita o controle eficiente de animais disponíveis para adoção, garantindo compatibilidade entre adotantes e animais através de políticas configuráveis e regras de negócio bem definidas, junto com seus relatórios.

---

## 3. Estrutura de Classes Planejada (UML Textual)

### A. Classes, Atributos e Métodos Principais

| Classe | Atributos Principais | Métodos Principais |
| :--- | :--- | :--- |
| **Animal** | `id: int`, `especie: str`, `raca: str`, `nome: str`, `sexo: str`, `idade_meses: int`, `porte: str`, `temperamento: list[str]`, **`-status: StatusAnimal`** (Encapsulado), `data_entrada: date`, **`historico: list[Evento]`** | `mudar_status(novo_status)`, `aplicar_vacina()`, `get_resumo()` |
| **Cachorro** | `sociavel_com_gatos: bool` | **(Herda métodos de Animal)** |
| **Gato** | `usa_caixa_areia: bool` | **(Herda métodos de Animal)** |
| **Adotante** | `id: int`, `nome: str`, `idade: int`, `moradia: str`, `area_util: float`, **`-experiencia_pets: bool`** (Encapsulado), **`-possui_criancas: bool`** (Encapsulado), `outros_animais: bool` | `verificar_elegibilidade()`, `solicitar_reserva()`, `finalizar_adocao()` |
| **Reserva** | `animal: Animal`, `adotante: Adotante`, `data_reserva: date`, `data_expiracao: date`, `status: str` | `processar_confirmacao()`, `encerrar_reserva()`, `verificar_expiracao()` |
| **Adocao** | `animal: Animal`, `adotante: Adotante`, `data_adocao: date`, `taxa: float`, `estrategia_taxa: str` | `emitir_contrato()`, `registrar_transacao_saida()` |
| **Devolucao** | `animal: Animal`, `adotante: Adotante`, `data_devolucao: date`, `motivo: str` | `registrar_evento()`, `ajustar_status_animal()` |
| **Evento** | `tipo: str`, `descricao: str`, `data: datetime` | (Classe de dados para o histórico) |
| **Relatorios** | `tipo: str`, `filtros`, `data_geracao: date` | `processar_dados()`, `imprimir_relatorio()` |

### B. Relacionamentos entre Classes

| Classe Origem | Relação | Classe Destino | Cardinalidade | Descrição |
| :--- | :--- | :--- | :--- | :--- |
| **Animal** | Herança | **Cachorro/Gato** | 1 para N | `Cachorro` e `Gato` especializam `Animal`. |
| **Animal** | Composição | **Evento** | 1 para N | O animal possui um histórico composto por vários eventos. |
| **Adotante** | Associação | **Reserva** | 1 para N | Um adotante pode fazer **várias** reservas. |
| **Reserva** | Associação | **Animal** | 1 para 1 | Cada reserva envolve **um único** animal. |
| **Adotante** | Associação | **Adocao** | 1 para N | Um adotante pode ter **várias** adoções registradas. |
| **Adocao** | Associação | **Animal** | 1 para 1 | Cada adoção envolve **um único** animal. |
| **Devolucao** | Associação | **Animal** | 1 para 1 | Cada devolução registra o retorno de **um único** animal. |
| **Devolucao** | Associação | **Adotante** | 1 para N | Um adotante pode ter **várias** devoluções registradas. |
---
