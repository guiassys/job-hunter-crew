# main.py
import os
from datetime import datetime
from src.crew import JobHunterCrew

CURRICULO_PATH = "/home/guiassys/devtools/repos/interview-guiassys/docs/resume/cv-guilherme-main.md"
OUTPUT_DIR = "/home/guiassys/devtools/repos/job-hunter-crew/output"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(CURRICULO_PATH):
        with open(CURRICULO_PATH, "r", encoding="utf-8") as f:
            curriculo_conteudo = f.read()
    else:
        raise FileNotFoundError(f"Não foi possível encontrar o currículo em: {CURRICULO_PATH}")

    print("## Iniciando Pipeline Job Hunter Modularizado ##")

    inputs = {'curriculo_conteudo': curriculo_conteudo}
    resultado = JobHunterCrew(curriculo_conteudo=curriculo_conteudo).crew().kickoff(inputs=inputs)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_report_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(resultado))

    print("\n\n##################################################")
    print(f"## RELATÓRIO SALVO COM SUCESSO: {filepath} ##")
    print("##################################################\n")
    print(resultado)