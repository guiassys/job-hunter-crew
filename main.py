import os
from datetime import datetime
from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from duckduckgo_search import DDGS

# 1. Configuração do LLM apontando diretamente para o localhost exposto pelo Docker
ollama_llm = LLM(
    model="ollama/qwen3-coder:30b",
    base_url="http://localhost:11434"
)

# 2. Caminhos e Diretórios
CURRICULO_PATH = "/home/guiassys/devtools/repos/interview-guiassys/docs/resume/cv-guilherme-main.md"
OUTPUT_DIR = "/home/guiassys/devtools/repos/job-hunter-crew/output"

# Garante que o diretório de saída existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

if os.path.exists(CURRICULO_PATH):
    with open(CURRICULO_PATH, "r", encoding="utf-8") as f:
        curriculo_conteudo = f.read()
else:
    raise FileNotFoundError(f"Não foi possível encontrar o currículo em: {CURRICULO_PATH}")

# 3. Ferramenta de Busca Web nativa com DuckDuckGo (Gratuito / Sem API Key)
@tool("Busca Web DuckDuckGo")
def web_search_tool(query: str) -> str:
    """Realiza uma busca na web usando o DuckDuckGo e retorna os principais resultados contendo títulos, links e resumos."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"Título: {r.get('title')}\nLink: {r.get('href')}\nResumo: {r.get('body')}\n")
    return "\n---\n".join(results) if results else "Nenhum resultado encontrado."

# Ferramenta para salvar o relatório em Markdown com timestamp
@tool("Salvar Relatório em Markdown")
def save_markdown_report(content: str) -> str:
    """Recebe o conteúdo consolidado em Markdown, gera um nome baseado em timestamp e salva no diretório de output."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_report_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Relatório salvo com sucesso no caminho: {filepath}"

# 4. Definição dos Agentes (Incluindo o editor responsável por salvar)
job_hunter_agent = Agent(
    role="Recrutador Especialista e Pesquisador de Vagas",
    goal="Encontrar vagas de emprego abertas na internet totalmente aderentes ao perfil técnico e sênior do candidato.",
    backstory=(
        "Você é um pesquisador experiente de mercado de tecnologia, especialista em identificar oportunidades de emprego reais "
        "para engenheiros de software sêniores com foco em Java, Spring Boot, React, Cloud (GCP) e IA Generativa."
    ),
    tools=[web_search_tool],
    verbose=True,
    llm=ollama_llm,
)

career_advisor_agent = Agent(
    role="Consultor de Carreira Sênior",
    goal="Analisar as vagas encontradas e consolidar um relatório estruturado com as 5 melhores oportunidades.",
    backstory=(
        "Você é um consultor de carreira especializado no setor de tecnologia que ajuda profissionais sêniores a "
        "avaliar aderência técnica, senioridade e fit cultural em vagas de mercado."
    ),
    verbose=True,
    llm=ollama_llm,
)

report_editor_agent = Agent(
    role="Editor Técnico e Especialista em Documentação",
    goal="Revisar e persistir o relatório final em formato Markdown utilizando a ferramenta de salvamento.",
    backstory=(
        "Você é um revisor técnico responsável por garantir que o relatório final esteja bem formatado e salvo "
        "corretamente no diretório de saída com nome único."
    ),
    tools=[save_markdown_report],
    verbose=True,
    llm=ollama_llm,
)

# 5. Definição das Tarefas (Incluindo a task de salvamento)
search_task = Task(
    description=(
        f"Com base no resumo profissional a seguir:\n\n{curriculo_conteudo}\n\n"
        "Faça buscas na internet por vagas de emprego recentes (Remotas ou no Brasil) para cargos como "
        "Engenheiro de Software Sênior, Arquiteto de Soluções ou Tech Lead com forte atuação em Java, Spring Boot, GCP ou IA."
    ),
    expected_output=(
        "Uma lista contendo detalhes, nomes das empresas, cargos e links ou locais onde as vagas foram encontradas."
    ),
    agent=job_hunter_agent,
)

report_task = Task(
    description=(
        "Analise as oportunidades obtidas no passo anterior e selecione as 5 vagas que possuem maior alinhamento "
        "com a trajetória do candidato (Guilherme Augusto de Assis).\n\n"
        "Monte um relatório detalhado formatado em Markdown contendo exatamente 5 oportunidades de emprego, informando:\n"
        "1. **Título do Cargo e Empresa**\n"
        "2. **Localização / Modalidade** (Remoto ou Híbrido)\n"
        "3. **Link / Fonte da Vaga**\n"
        "4. **Por que é um bom fit?** (Alinhamento com Java, Spring, Cloud, IA, etc.)\n"
        "5. **Principais Requisitos/Pontos de Atenção**"
    ),
    expected_output=(
        "Um relatório profissional formatado em Markdown com as 5 melhores vagas selecionadas e justificadas."
    ),
    agent=career_advisor_agent,
)

save_task = Task(
    description=(
        "Receba o relatório consolidado, revise sua estrutura em Markdown e utilize a ferramenta "
        "'Salvar Relatório em Markdown' para persistir o documento no diretório de saída."
    ),
    expected_output=(
        "A confirmação de que o arquivo Markdown foi gerado e salvo com sucesso."
    ),
    agent=report_editor_agent,
)

# 6. Montagem e Execução da Crew
job_pipeline = Crew(
    agents=[job_hunter_agent, career_advisor_agent, report_editor_agent],
    tasks=[search_task, report_task, save_task],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("## Iniciando Pipeline Job Hunter Nativo com Salvamento Automático ##")
    resultado = job_pipeline.kickoff()
    print("\n\n##################################################")
    print("## RELATÓRIO FINAL E ARQUIVO SALVO COM SUCESSO ##")
    print("##################################################\n")
    print(resultado)