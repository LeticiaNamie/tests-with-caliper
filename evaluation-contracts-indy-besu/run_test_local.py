import os
import subprocess
from datetime import datetime

# Caminhos para cada configuração de função
BENCHMARK_FILES = {
    "createDid":                    'benchmarks/scenario/IndyDidRegistry/config-createDid.yaml',
    "updateDid":                    'benchmarks/scenario/IndyDidRegistry/config-updateDid.yaml',
    "createSchema":                 'benchmarks/scenario/SchemaRegistry/config.yaml',
    "createCredentialDefinition":   'benchmarks/scenario/CredentialDefinitionRegistry/config.yaml',
    "createRevocationRegistry":     'benchmarks/scenario/RevocationRegistry/config_createRevocationRegistry.yaml',
    "createOrUpdateEntry":          'benchmarks/scenario/RevocationRegistry/config_createOrUpdateEntry.yaml',
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

# Executa o Caliper para uma função e TPS, com retry se WS não estiver pronto
def run_test(tps, function_name, benchmark_file, max_retries=3, retry_delay=15):
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
        '--caliper-flow-skip-install'
    ]

    for attempt in range(1, max_retries + 1):
        subprocess.run(cmd)
        if os.path.exists('report.html'):
            os.rename('report.html', report_path)
            print(f"✅ Relatório salvo em {report_path}")
            return
        if attempt < max_retries:
            print(f"⚠️ {function_name}@{tps}TPS tentativa {attempt}/{max_retries} falhou (WS não disponível). Aguardando {retry_delay}s...")
            time.sleep(retry_delay)

    print(f"⚠️ Relatório não encontrado para {function_name} @ {tps} TPS após {max_retries} tentativas.")

# Faz o bind do Caliper com Besu uma única vez antes de todos os testes
def bind_caliper():
    print("\n🔗 Realizando bind do Caliper com Besu...")
    result = subprocess.run([
        'npx', 'caliper', 'bind',
        '--caliper-bind-sut', 'besu:latest',
        '--caliper-bind-cwd', './'
    ])
    if result.returncode != 0:
        print("❌ Bind do Caliper falhou")
        exit(1)
    print("✅ Bind concluído")

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

    bind_caliper()
    setup_issuer()

    for repetition in range(1, 6):
        print(f"\n{'='*50}")
        print(f"🔁 Repetição {repetition}/5")
        print(f"{'='*50}")
        for function_name, benchmark_file in BENCHMARK_FILES.items():
            print(f"\n{'='*50}")
            print(f"🚀 Iniciando testes para função: {function_name}")
            print(f"{'='*50}")
            for tps in TPS_LIST:
                run_test(tps, function_name, benchmark_file)
