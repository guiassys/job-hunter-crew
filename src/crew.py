# src/crew.py
import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tools import web_search_tool

@CrewBase
class JobHunterCrew():
    """Job Hunter Crew"""

    # Define os caminhos absolutos a partir da pasta atual do arquivo (src/)
    agents_config = os.path.join(os.path.dirname(__file__), 'config', 'agents.yaml')
    tasks_config = os.path.join(os.path.dirname(__file__), 'config', 'tasks.yaml')

    def __init__(self, curriculo_conteudo: str):
        self.curriculo_conteudo = curriculo_conteudo
        self.ollama_llm = LLM(
            model="ollama/qwen3-coder:30b",
            base_url="http://localhost:11434"
        )

    @agent
    def job_hunter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_hunter_agent'],
            tools=[web_search_tool],
            llm=self.ollama_llm,
            verbose=True
        )

    @agent
    def career_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['career_advisor_agent'],
            llm=self.ollama_llm,
            verbose=True
        )

    @agent
    def report_editor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['report_editor_agent'],
            llm=self.ollama_llm,
            verbose=True
        )

    @task
    def search_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_task'],
            agent=self.job_hunter_agent()
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'],
            agent=self.career_advisor_agent()
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config['edit_task'],
            agent=self.report_editor_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )