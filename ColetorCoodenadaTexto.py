import re
import pandas as pd
import sys

# para funcionar precisar instalar biblioteca do geopandas
# Memorial descritivo de uma fazenda, exemplo, pode usar cofiguração E/N ou X/Y

# Se quiser importar o texto de algum arquivo
# Coloquei o endereço do texto
with open(r'C:\\Users\\luciana\\Desktop\\python\\texto.docx') as f:
     texto = f.read()

# Texto exemplo extraido de um PDF

#COLE SEU TEXTO APÓS AS '''
textooriginal = f


#subtitui o formato do texto
texto =  textooriginal.replace(":","=") or textooriginal.replace("x","e") or textooriginal.replace("x","n") 


# Extraindo longitude (E) e latitude (N)
# \d = Qualquer dígito; \s = Whitespace (https://docs.python.org/3/library/re.html)
e_raw = re.findall(r'E=\s[\d\.-]+[\d]', texto)
n_raw = re.findall(r'N=\s[\d\.-]+[\d\.-]+[\d]', texto)

if len(e_raw) != len(n_raw):
    sys.exit('Erro na quantidade de coordenadas obtidas.')

# Removendo caracteres como letras e pontos
e_string = []; n_string = []

for i in range(len(e_raw)):
    e_string.append(e_raw[i].replace('E= ', '').replace('E=\n', '')\
                    .replace('.', ''))
        
    n_string.append(n_raw[i].replace('N= ', '').replace('N=\n', '')\
                    .replace('.', ''))

# Convertendo para número inteiro
e_int = list(map(float, e_string))
n_int = list(map(float, n_string))
coord = [e_int, n_int]

# Salve dataframe do Pandas e em CSV para abrir no SIG
dt_coord = pd.DataFrame(coord).transpose()
dt_coord.columns = ['E_UTM', 'N_UTM']
dt_coord.to_csv (r'export_dataframe.csv', index = False, header=True)
print(dt_coord.head(100))
# 100 esta limitado a extrair somente 100 coodenada, podendo aumentar a critério 

