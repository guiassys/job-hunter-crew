# 🤖 Job Hunter Crew (CrewAI + Ollama Local)

Pipeline de Inteligência Artificial autônoma construída com **CrewAI** para pesquisar, filtrar, analisar e documentar vagas de emprego de tecnologia alinhadas ao seu perfil profissional. O sistema roda 100% local utilizando modelos executados via **Ollama** e ferramentas gratuitas de busca web, seguindo uma arquitetura modular baseada em boas práticas.

---

## 🏗️ Como o Projeto Funciona (Arquitetura)

O projeto utiliza um pipeline sequencial composto por três agentes especializados, com prompts e tarefas desacoplados em arquivos de configuração YAML:

1. **Recrutador Especialista e Pesquisador de Vagas (`job_hunter_agent`)**:
   - Lê o seu currículo oficial.
   - Utiliza a ferramenta de busca web (`DuckDuckGo`) para encontrar vagas recentes e aderentes ao seu perfil (Java, Spring Boot, GCP, IA).
2. **Consultor de Carreira Sênior (`career_advisor_agent`)**:
   - Analisa as oportunidades encontradas.
   - Seleciona as **5 melhores vagas** com maior fit técnico e cultural, detalhando requisitos e justificativas.
3. **Editor Técnico e Especialista em Documentação (`report_editor_agent`)**:
   - Recebe o relatório consolidado, valida a formatação em Markdown e aciona a ferramenta de salvamento automático para gravar o resultado de forma única (evitando sobrescrita).

---

## 📂 Estrutura do Projeto

```text
job-hunter-crew/
├── config/
│   ├── agents.yaml       # Configuração de papéis, goals e backstories dos agentes
│   └── tasks.yaml        # Descrições e expected_outputs das tarefas
├── output/               # Diretório onde os relatórios em Markdown são salvos com timestamp
├── src/
│   ├── __init__.py
│   ├── crew.py           # Classe orquestradora da Crew utilizando @CrewBase
│   └── tools.py          # Ferramentas customizadas (DuckDuckGo search)
├── .env
├── README.md
├── main.py               # Script principal e ponto de entrada leve
└── requirements.txt      # Dependências do projeto
```

---

## ⚙️ Pré-requisitos

- **Python 3.10+** (Ambiente WSL / Ubuntu recomendado)
- **Ollama** rodando localmente (ex: via Docker) com o modelo configurado (`qwen3-coder:30b`).

---

## 🚀 Instalação e Configuração

Abra o seu terminal no WSL/Ubuntu e siga os passos abaixo:

1. **Navegue até o diretório do projeto**
```bash
cd ~/devtools/repos/job-hunter-crew
```

2. **Criar e ativar o ambiente virtual Python**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar as dependências do projeto**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Como Executar o Projeto

Certifique-se de que o seu container do Ollama está rodando e acessível na porta `11434`. Com o ambiente virtual ativado (`source venv/bin/activate`), basta executar o script principal:

```bash
python main.py
```

O pipeline será iniciado, os agentes farão as buscas e análises de mercado, e o relatório final em Markdown será exibido no console e salvo automaticamente no diretório `output/` com um timestamp exclusivo (ex: `job_report_20261111_183000.md`).