import os
import subprocess
from datetime import datetime

# Caminhos para cada configuração de função
BENCHMARK_FILES = {
    "createRevocationRegistry": 'benchmarks/scenario/RevocationRegistry/config_createRevocationRegistry.yaml'
}

BENCHMARK_FILES_BAK = {
    "createDid": 'benchmarks/scenario/IndyDidRegistry/config-createDid.yaml',
    "updateDid": 'benchmarks/scenario/IndyDidRegistry/config-updateDid.yaml'
}

BENCHMARK_FILES_SEPARATE = {
    "createRevocationRegistry": 'benchmarks/scenario/RevocationRegistry/config_createRevocationRegistry.yaml',
    "createCredentialDefinition": 'benchmarks/scenario/CredentialDefinitionRegistry/config.yaml',
    "createOrUpdateEntry": 'benchmarks/scenario/RevocationRegistry/config_createOrUpdateEntry.yaml'
}

# TPS a ser testado (20 a 120, de 20 em 20)
TPS_LIST = [20, 40, 60, 80, 100, 120]

# Atualiza o valor de TPS no arquivo de benchmark YAML
def update_tps_in_file(file_path, tps):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("tps:"):
            new_lines.append(f"          tps: {tps}\n")
        else:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Executa o Caliper para uma função e TPS
def run_test(tps, function_name, benchmark_file):
    update_tps_in_file(benchmark_file, tps)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_dir = f"src/reports/{function_name}"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{function_name}_report_{tps}_{timestamp}.html")
    cmd = [
        'npx', 'caliper', 'launch', 'manager',
        '--caliper-workspace', './',
        '--caliper-benchconfig', benchmark_file,
        '--caliper-networkconfig', 'networks/besu/networkconfig.json',
        '--caliper-bind-sut', 'besu:latest',
        '--caliper-flow-skip-install'
    ]

    subprocess.run(cmd)

    if os.path.exists('report.html'):
        os.rename('report.html', report_path)
        print(f"✅ Relatório salvo em {report_path}")
    else:
        print(f"⚠️ Relatório não encontrado para {function_name} @ {tps} TPS.")

# Garante que o DID issuer existe na chain antes dos testes
def setup_issuer():
    print("\n🔧 Verificando/criando DID issuer na chain...")
    result = subprocess.run(['node', 'setup_issuer.js'], capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"❌ Setup falhou: {result.stderr.strip()}")
        exit(1)

# Executa todos os testes
if __name__ == "__main__":
    import time

    setup_issuer()

    for function_name, benchmark_file in BENCHMARK_FILES_BAK.items():
        print(f"\n🚀 Iniciando testes para função: {function_name}")
        for tps in TPS_LIST:
            run_test(tps, function_name, benchmark_file)
        if list(BENCHMARK_FILES_BAK.keys())[-1] != function_name:
            print("⏳ Aguardando 5s antes da próxima função...")
            time.sleep(5)
