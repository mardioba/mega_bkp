import subprocess
import re, os
from subprocess import PIPE
from datetime import datetime
import time
import sys
import os
import subprocess
import re

def Tamanho_diretorio_em_gb(directory):
    total_size = 0
    # Percorre o diretório e todos os subdiretórios
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Somar o tamanho de cada arquivo
            total_size += os.path.getsize(file_path)
    
    # Converter bytes para gigabytes
    size_in_gb = total_size / (1024 ** 3)
    return round(size_in_gb, 2)


def Tamanho_arquivo_em_mb(file_path):
    # Obtém o tamanho do arquivo em bytes
    file_size = os.path.getsize(file_path)
    # Converte de bytes para megabytes
    size_in_mb = file_size / (1024 ** 2)
    return round(size_in_mb, 2)
  
def bytes_para_gigabytes(bytes_value):
    gigabytes = bytes_value / (1024**3)  # 1024^3 = 1,073,741,824
    return round(gigabytes, 2)  # Retorna com duas casas decimais

def Login(usuario, senha):
  saida=subprocess.Popen(['mega-login', usuario, senha], stdout=subprocess.PIPE)
  saida_filtrada=re.sub(r'^b\'\[.{2,}\]|\\n\'|\:.{2,}$', '', str(saida.stdout.read()))
  # print(saida_filtrada)
  if 'Login failed' in saida_filtrada:
    msg='Login falhou'
    print(msg)
  else:
    msg='Login efetuado com sucesso'
    print(msg)

def Verificar_Logado():
  pass
  ls=subprocess.Popen(['mega-ls'], stdout=subprocess.PIPE)
  saida=ls.stdout.read().decode('utf-8')
  saida_filtrada=re.sub(r"^b\'|\[.{2,}\] |\\n\'$", '', saida)
  # print(saida_filtrada)
  if 'Not logged in.' in saida_filtrada:
    return False
  else:
    return True

def informacoes():
  """Retorna o espaço usado e o total de espaço na nuvem em Gigabyte

  Returns:
      tipo: tupla
  """
  if Verificar_Logado():
    df=subprocess.Popen(['mega-df'], stdout=subprocess.PIPE)
    saida=df.stdout.read().decode('utf-8')
    filtrar=saida.splitlines()[4]
    # filtrar=re.sub(r'  ', '_', filtrar)
    filtrar=filtrar.split()
    usado=bytes_para_gigabytes(int(filtrar[2]))
    espaco_total=bytes_para_gigabytes(int(filtrar[5]))
    # print(f'Espaço usado: {usado} GB de um total de {espaco_total} GB')
    return usado, espaco_total
  else:
    print('Você não está logado')
def Put_arquivo(arquivo, dir_remoto):
  try:
    pass
    ver=os.path.isfile(arquivo)
    # print(f"VER: {ver}")
    if ver:
      # comment: 
      tamanho=Tamanho_diretorio_em_gb(arquivo)
      print(f"tamanho: {tamanho} GB")
    else:
      print("O diretório não existe")
  except Exception as e:
    raise e
def Put_diretorio(diretorio, dir_remoto):
  try:
    diretorio=diretorio.replace(" ", '')
    ver=os.path.isdir(diretorio)
    print(f"VER: {ver}")
    diretorio_filtrado=re.sub(r'\/$', '', diretorio)
    print(f"VER: {ver}")
    if ver:
      tamanho=Tamanho_diretorio_em_gb(diretorio_filtrado)
      print(f"tamanho: {tamanho} GB")
      comando = subprocess.Popen(['mega-put', '-c', diretorio, dir_remoto], stdout=subprocess.PIPE)
      saida = comando.stdout.read().decode('utf-8')
      print(saida)
    else:
      print(f"O diretório {diretorio} não existe")
  except Exception as e:
    raise e
  
