def premiacao():
    from selenium import webdriver
    import time
    import streamlit as st
    import os
    import pandas as pd
    import shutil
    from selenium.common.exceptions import NoSuchElementException        
    from pathlib import Path
    from openpyxl import load_workbook
    from glob import glob
    import numpy as np
    from datetime import datetime
    from colorama import Fore, Style
    from selenium.webdriver.chrome.service import Service

    # Configurações principais
    dataAtual = datetime.now().strftime('%d/%m/%y')
    previsao = datetime.today().strftime('%m/%y')
    usuario = os.getlogin()

    # Configurando o Chrome WebDriver
    driver_service = Service(executable_path=fr"R:\Controladoria\113. Geovanna\Chrome Driver\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element('xpath', xpath)
        except NoSuchElementException:
            return False
        return True

    def check_exists_by_id(id):
        try:
            driver.find_element('id', id)
        except NoSuchElementException:
            return False
        return True

    # Abertura da página e login
    driver.get('https://sistema.ssw.inf.br/bin/ssw0422')
    while not check_exists_by_xpath('/html/body/form/input[1]'):
        time.sleep(5)
    driver.find_element('xpath', '/html/body/form/input[1]').send_keys('RVE')

    while not check_exists_by_xpath('/html/body/form/input[2]'):
        time.sleep(5)
    driver.find_element('xpath', '/html/body/form/input[2]').send_keys('51930766882')

    while not check_exists_by_xpath('/html/body/form/input[3]'):
        time.sleep(5)
    driver.find_element('xpath', '/html/body/form/input[3]').send_keys('51930766')

    while not check_exists_by_xpath('/html/body/form/input[4]'):
        time.sleep(5)
    driver.find_element('xpath', '/html/body/form/input[4]').send_keys('expresso')    
    time.sleep(1)
    driver.find_element('id', '5').click()

    # PRIMEIRA PÁGINA
    time.sleep(5)
    while not check_exists_by_id('2'):
        time.sleep(5)
    driver.find_element('id', '2').clear()
    driver.find_element('id', '2').send_keys('MTZ')

    while not check_exists_by_id('3'):
        time.sleep(5)
    driver.find_element('id', '3').clear()
    driver.find_element('id', '3').send_keys('455')

    # SEGUNDA TELA
    driver.get('https://sistema.ssw.inf.br/bin/ssw0230')

    # Configuração do Período de Autorização e outros campos
    while not check_exists_by_id('2'):
        time.sleep(5)
    driver.find_element('id', '2').clear()

    while not check_exists_by_id('11'):
        time.sleep(5)
    driver.find_element('id', '11').clear()

    driver.find_element('id', '11').send_keys(f'01{previsao}')    

    driver.find_element('id', '12').send_keys(f'{dataAtual}')

    while not check_exists_by_id('21'):
        time.sleep(5)
    driver.find_element('id', '21').clear()
    driver.find_element('id', '21').send_keys('x')                  

    while not check_exists_by_id('35'):
        time.sleep(5)
    driver.find_element('id', '35').clear()
    driver.find_element('id', '35').send_keys('E')    
            
    driver.find_element('id', '37').send_keys('A')
    driver.find_element('id', '38').click()
    time.sleep(1)
    driver.find_element('id', '38').send_keys('E')
    driver.find_element('id', '39').send_keys('H')

    driver.find_element('id', '40').click()

    # Fila de relatórios        
    driver.get('https://sistema.ssw.inf.br/bin/ssw1440')

    while not check_exists_by_xpath('//*[@id="tblsr"]/tbody/tr[2]'):
        time.sleep(5)
    seq = driver.find_element('xpath', '//*[@id="tblsr"]/tbody/tr[2]/td[1]/div').text
    print(Fore.BLUE + Style.BRIGHT + 'Sequência do seu relatório: ' + Style.RESET_ALL + seq)

    i = 2
    while True:
        sequencia = driver.find_element('xpath', fr'//*[@id="tblsr"]/tbody/tr[{i}]/td[1]/div')
        baixar = driver.find_element('xpath', fr'//*[@id="tblsr"]/tbody/tr[{i}]/td[9]/div')
        se = sequencia.text
        ba = baixar.text
        if str(se) == seq and str(ba) == 'Baixar':
            driver.find_element('xpath', fr'/html/body/form/div[2]/div[2]/table[1]/tbody/tr[{i}]/td[9]/div/a/u').click()
            break
        elif str(ba) == 'Excluir' and str(se) == seq:
            driver.find_element('id', '2').click()
            time.sleep(5)
        elif str(ba) == 'Interromper' and str(se) == seq:
            driver.find_element('id', '2').click()
            time.sleep(5)
            print(Fore.BLUE + Style.BRIGHT + 'Quase pronto para baixar! ' + Style.RESET_ALL)
        else:
            i += 1
            
    time.sleep(15)        
    driver.close()
    
    import os
    import shutil
    import pandas as pd
    from glob import glob
    import time
    from colorama import Fore, Style
    import locale
    from datetime import datetime
    
    # Caminho de origem
    caminho = r"C:\Users\kleber.benites\Downloads"
    lista_arquivo = os.listdir(caminho)
    
    # Lista de arquivos com suas datas de modificação
    lista_datas = []
    for arquivo in lista_arquivo: 
        data = os.path.getmtime(os.path.join(caminho, arquivo))
        lista_datas.append((data, arquivo))
    
    # Ordenar arquivos pela data de modificação
    lista_datas.sort(reverse=True)
    ultimo_arquivo = lista_datas[0]
    
    print(Fore.GREEN + Style.BRIGHT + "Vamos salvar o arquivo na pasta" + Style.RESET_ALL)
    time.sleep(3)
    
    # Caminho de destino
    destination = r"C:\Users\kleber.benites\Desktop\455"
    
    # Apagar arquivos CSV antigos
    tabela = glob(os.path.join(destination, "CSVRVE*"))
    for i in tabela:
        os.remove(i)
    
    # Mover o arquivo mais recente para o destino
    new_path = shutil.move(os.path.join(caminho, ultimo_arquivo[1]), destination)
    
    # Criando o DataFrame
    caminho = destination
    lista_arquivo = os.listdir(caminho)
    lista_datas = []
    for arquivo in lista_arquivo: 
        data = os.path.getmtime(os.path.join(caminho, arquivo))
        lista_datas.append((data, arquivo))
    
    # Ordenar arquivos pela data de modificação
    lista_datas.sort(reverse=True)
    ultimo_arquivo = lista_datas[0]
    
    # Ler o arquivo CSV mais recente
    data = []
    with open(os.path.join(caminho, ultimo_arquivo[1]), 'r') as arquivo:
        texto = arquivo.readlines()
        for linha in texto:
            data.append(linha.strip().split(';'))  # Use o delimitador ';' para dividir as colunas
    
    # Criar o DataFrame
    df = pd.DataFrame(data)
    
    # Eliminando a primeira linha
    df = df.drop(index=0).reset_index(drop=True)
    
    # Apagando as colunas especificadas
    colunas_para_apagar = [
        1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 30, 
        33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 
        63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74
    ] + list(range(76, 139))  # Adiciona colunas de 75 até 138
    
    # Subtraindo 1 de cada índice porque as colunas no DataFrame começam em 0
    colunas_para_apagar = [col - 1 for col in colunas_para_apagar]
    
    df = df.drop(df.columns[colunas_para_apagar], axis=1)
    
    # Definindo o locale para Português do Brasil
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    
    # Obtendo o nome do mês em português
    mes_atual = datetime.now().strftime('%B')
    ano_atual = datetime.now().strftime('%Y')
    
    df['Mês Atual'] = mes_atual.capitalize()  # Capitaliza a primeira letra do mês
    df['Ano Atual'] = ano_atual
        # Salvando o DataFrame como um arquivo Excel
    caminho_destino = r"R:\Controladoria\108. Gabriel\aehminuto"
    
    # Certifique-se de que o diretório existe
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)
    
    nome_arquivo = "resultado.xlsx"
    caminho_completo = os.path.join(caminho_destino, nome_arquivo)
    
    # Salvando o DataFrame sem o índice das linhas
    df.to_excel(caminho_completo, index=False, header=False)
    
    print(f"Arquivo Excel salvo com sucesso em: {caminho_completo}")

premiacao()