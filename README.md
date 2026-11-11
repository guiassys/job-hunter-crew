# 🤖 Job Hunter Crew (CrewAI + Ollama Local)

Pipeline de Inteligência Artificial autônoma construída com **CrewAI** para pesquisar, filtrar, analisar e documentar vagas de emprego de tecnologia alinhadas ao seu perfil profissional. O sistema roda 100% local utilizando modelos executados via **Ollama** e ferramentas gratuitas de busca web.

---

## 🏗️ Como o Projeto Funciona (Arquitetura)

O projeto utiliza um pipeline sequencial composto por três agentes especializados:

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
│
├── main.py             # Script principal contendo os agentes, tasks e pipeline do CrewAI
├── output/             # Diretório onde os relatórios em Markdown são salvos com timestamp
└── README.md           # Documentação do projeto