import subprocess
import requests
import tarfile
import os
import tempfile
import sys

os.makedirs('/kaggle/working/zrok')

__key__ = sys.argv[1]

with open('/kaggle/working/zrok/zrok_key.txt', 'w') as key:
    key.write(__key__)

def obter_ultima_versao_zrok():
    url = 'https://api.github.com/repos/openziti/zrok/releases/latest'
    resposta = requests.get(url)
    resposta.raise_for_status()
    return resposta.json()['tag_name']

# Definir a função para determinar a arquitetura
def determinar_arquitetura():
    arquitetura = subprocess.check_output(['uname', '-m']).decode().strip()
    if arquitetura == 'x86_64':
        return 'amd64'
    elif arquitetura in ['aarch64', 'arm64']:
        return 'arm64'
    elif arquitetura in ['armv7', 'armhf', 'arm']:
        return 'arm'
    else:
        raise ValueError(f"ERROR: unknown arch '{arquitetura}'")

# Obter a última versão do zrok
versao_zrok = obter_ultima_versao_zrok()

# Determinar a arquitetura
arquitetura_gox = determinar_arquitetura()

# Definir o URL para download

url_download = f"https://github.com/openziti/zrok/releases/download/{versao_zrok}/zrok_{versao_zrok.lstrip('v')}_linux_{arquitetura_gox}.tar.gz"

response = requests.get(url_download)

with open('zrok.tar.gz', 'wb') as file:
    file.write(response.content)

with tarfile.open('zrok.tar.gz', 'r:gz') as tar:
    tar.extractall('/kaggle/working/zrok')

os.remove('zrok.tar.gz')

with open('/dev/null', 'w') as devnull:
    subprocess.run(["git", "clone", "https://github.com/NoxKray/DeFooocusBR.git"], stderr=devnull, stdout=devnull)
