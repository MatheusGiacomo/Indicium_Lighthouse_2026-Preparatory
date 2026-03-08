import subprocess
import os
from prefect import flow, task
from dotenv import load_dotenv

load_dotenv()

# Caminhos para os executáveis dentro do .venv
VENV_PYTHON = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
VENV_DBT = os.path.join(os.getcwd(), ".venv", "Scripts", "dbt.exe")

@task(retries=2, retry_delay_seconds=60)
def run_ingestion():
    """Tarefa para rodar a ingestão"""
    print("Iniciando Ingestão")
    result = subprocess.run(
        [VENV_PYTHON, "ingestion/main_ingestion.py"], 
        capture_output=True, 
        text=True, 
        encoding='utf-8', 
        errors='replace',
        env=os.environ.copy()
    )
    if result.returncode != 0:
        raise Exception(f"Erro na Ingestão: {result.stderr}")
    print("Ingestão finalizada com sucesso")

@task
def run_dbt_transformation():
    import subprocess
    
    # Caminho da pasta onde está o seu dbt (ajuste se for diferente)
    dbt_path = "transform" 
    
    print("Instalando dependências do dbt")
    subprocess.run(["dbt", "deps"], cwd=dbt_path, check=True)

    print("Iniciando Transformações dbt")
    result_run = subprocess.run(["dbt", "run"], cwd=dbt_path, capture_output=True, text=True)
    
    if result_run.returncode != 0:
        raise Exception(f"Erro no dbt Run: {result_run.stdout[:500]}")

    print("Iniciando Testes de Qualidade dbt")
    result_test = subprocess.run(["dbt", "test"], cwd=dbt_path, capture_output=True, text=True)
    
    if result_test.returncode != 0:
        raise Exception(f"Erro nos Testes dbt: {result_test.stdout[:500]}")
    
    print("Transformação e Testes finalizados com sucesso")

@flow(name="Lighthouse Data Pipeline")
def main_flow():
    run_ingestion()
    run_dbt_transformation()

# Para deploy automatico todo dia caso ativo
if __name__ == "__main__":
    main_flow.serve(
        name="lighthouse-daily-deployment",
        cron="0 21 * * *", 
        tags=["producao", "econometria"],
        description="Pipeline diário de ingestão e transformação de dados do PIB e Petróleo."
    )