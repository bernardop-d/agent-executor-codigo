# 🤖 Agent Executor — Multi-Agent Workflow Automation Platform

> **Automatize fluxos de trabalho complexos com uma arquitetura de agentes inteligentes orquestrados por LLM (Gemini 2.5 Flash), capaz de pesquisar na web, escrever e executar código Python, manipular arquivos e rodar comandos de sistema — tudo de forma autônoma e encadeada.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Agent%20Development%20Kit-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://google.github.io/adk-docs/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](tests/)

---

## 📌 O Problema que Este Projeto Resolve

Tarefas modernas de engenharia e automação raramente são simples ou isoladas. Elas envolvem múltiplas etapas: pesquisar informações, processar dados com código, salvar resultados em arquivos e executar comandos no sistema operacional.

Ferramentas tradicionais exigem que o desenvolvedor orquestre cada etapa manualmente. O **Agent Executor** resolve isso com uma arquitetura multi-agente que **delega, encadeia e executa** essas etapas de forma autônoma, a partir de uma única instrução em linguagem natural.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|---|---|---|
| **Python** | 3.11+ | Linguagem principal |
| **Google ADK** | Latest | Framework de agentes inteligentes |
| **Gemini 2.5 Flash** | Latest | Modelo LLM para raciocínio dos agentes |
| **Pytest** | 7+ | Suite de testes unitários |
| **subprocess** | stdlib | Execução segura de comandos shell |
| **os** | stdlib | Manipulação de sistema de arquivos |

---

## ✨ Funcionalidades Principais

- **🔍 Pesquisa Inteligente na Web** — O `search_agent` utiliza a ferramenta nativa `google_search` do ADK para buscar e sumarizar informações atualizadas em tempo real.
- **💻 Escrita e Execução de Código** — O `coding_agent` é equipado com `BuiltInCodeExecutor`, permitindo que o agente escreva código Python, execute-o em sandbox e retorne o resultado ou diagnóstico de erro.
- **📁 Manipulação de Arquivos** — O `file_agent` expõe ferramentas para leitura (`read_file`), escrita (`write_file`) e listagem (`list_directory`) de arquivos e diretórios.
- **🐚 Automação via Shell** — O `shell_agent` executa comandos do sistema operacional com timeout e captura de stderr, ideal para instalar dependências, mover arquivos e checar processos.
- **🧠 Orquestração Inteligente** — O `root_agent` analisa a tarefa recebida, decompõe em sub-tarefas e delega a cada agente especializado de forma sequencial e adaptativa.
- **♻️ Resiliência a Falhas** — A estratégia de orquestração instrui o agente orquestrador a tentar abordagens alternativas antes de reportar um erro ao usuário.

---

## 🏗️ Arquitetura e Design de Software

O projeto segue o padrão **Hierarchical Multi-Agent Architecture**, onde um agente orquestrador (root) coordena sub-agentes especializados.

```
                        ┌──────────────────┐
                        │   root_agent     │  ← Orquestrador (Gemini 2.5 Flash)
                        │  (Orchestrator)  │
                        └────────┬─────────┘
                                 │ AgentTool delegation
              ┌──────────────────┼──────────────────┬──────────────┐
              ▼                  ▼                  ▼              ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐
     │ search_agent │  │ coding_agent │  │  file_agent  │  │shell_agent │
     │ google_search│  │ BuiltInCode  │  │  read_file   │  │run_shell   │
     │              │  │ Executor     │  │  write_file  │  │_command    │
     └──────────────┘  └──────────────┘  │ list_dir     │  └────────────┘
                                         └──────────────┘
```

**Decisões de Design:**
- **AgentTool Pattern**: Cada sub-agente é encapsulado como uma ferramenta do agente raiz, permitindo composição limpa e extensível.
- **Separation of Concerns**: Cada agente tem uma responsabilidade única e bem definida, seguindo o princípio SRP (Single Responsibility Principle).
- **Tool Abstraction Layer**: As ferramentas em `tools.py` são funções puras com tipagem estática, docstrings no padrão Google e tratamento de exceções centralizado.
- **Two-module Structure**: O repositório contém dois módulos independentes (`agentCoder` e `workflowAgent`), evoluindo de um agente simples para uma arquitetura completa.

---

## ⚙️ Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- Conta no Google AI Studio com acesso à API Gemini

### 1. Clone o repositório

```bash
git clone https://github.com/bernardop-d/agent-executor-codigo.git
cd agent-executor-codigo
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install google-adk pytest pytest-cov
```

### 4. Configure a variável de ambiente

```bash
export GOOGLE_API_KEY="sua-chave-aqui"
```

### 5. Execute o agente

```bash
cd workflowAgent
adk run .
```

---

## 🧪 Como Executar os Testes

```bash
pytest tests/ -v
```

Com cobertura:

```bash
pytest tests/ -v --cov=workflowAgent --cov-report=term-missing
```

---

## 📂 Estrutura do Projeto

```
agent-executor-codigo/
├── agentCoder/
│   ├── __init__.py
│   └── agent.py
├── workflowAgent/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
├── tests/
│   ├── __init__.py
│   └── test_tools.py
├── .gitignore
└── README.md
```

---

## 🔮 Roadmap

- [ ] Interface REST via FastAPI
- [ ] Persistência de histórico de sessões
- [ ] CI/CD com GitHub Actions
- [ ] Agente de análise de dados com Pandas

---

## 👨‍💻 Autor

**Bernardo P. D.** — [@bernardop-d](https://github.com/bernardop-d)
