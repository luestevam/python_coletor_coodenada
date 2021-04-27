import re
import pandas as pd
import sys

# para funcionar precisar instalar biblioteca do geopandas
# Memorial descritivo de uma fazenda, exemplo, pode usar cofiguração E/N ou X/Y

# Se quiser importar o texto de algum arquivo
# Coloquei o endereço do texto
# With open(r'C:\\teste\\texto.txt') as f:
#    texto = f.read()

# Texto exemplo extraido de um PDF

#COLE SEU TEXTO APÓS AS '''
textooriginal = '''
Inicia-se a descrição deste perímetro no vértice AL3-M-2983, de coordenadas N: 7.544.671,6460m e E: 202.858,5561m; situado na divisa da Fazenda Santa Rosa, código do INCRA n°
950.068.341.100-6, matrícula 1.577 de prop riedade de Espólio de Alicio de Moraes e Silva e da Fazenda Serra do Santo Antônio, código do INCRA n° 513.024.000.078-3, registro
2.073 de propriedade de Espólio de Antônio Machado Fontes; deste, segue confrontando com a Fazenda Serra do Santo Antônio, código do INCRA n° 513.024.000.078-3, registro 2.073
de propriedade de Espólio de Antônio Machado Fontes, com os seguintes azimutes e distâncias: 104°17'02" e 1.048,3273 m até o vértice AL3-M-2984, de coordenadas N: 7.544.412,9967m e
E: 203.874,4747m; 95°58'15" e 320,2690 m até o vértice AL3-M-2985, de coordenadas N: 7.544.379,6819m e E: 204.193,0063m; 58°58'50" e 319,7886 m até o vértice AL3-M-2986, de coordenadas
N: 7.544.544,4788m e E: 204.467,0624m; situado na divisa da Fazenda Serra do Santo Antônio, código do INCRA n° 513.024.000.078-3 , registro 2.073 de propriedade de Espólio de Antônio Machado Fontes e
da Fazenda São José do Sossego, código do INCRA n° 513.024.000.671-4, matrícula 55 de propriedade de Marcos Vinicius Marins Crespo; deste, segue confrontando com a Fazenda São José do Sossego, código do
INCRA n° 513.024.000.671-4, matrícula 55 de propriedade de Marcos Vinicius Marins Crespo, com os seguintes azimutes e distancias: 133°13'12" e 680,8454 m até o vértice AL3-M-2987, de coordenadas
N: 7.544.078,2354m e E: 204.963,2151m; 104°15'45" e 297,6542 m até o vértice AL3-M-2988, de coordenadas N: 7.544.004,9032m e E: 205.251,6946m; 139°41'55" e 198,3764 m até o vértice AL3-M-2989, de coordenadas
N: 7.543.853,6111m e E: 205.380,0063m; situado na divisa da Fazenda São José do Sossego, código do INCRA n° 513 .024.000.671-4, matrícula 55 de propriedade de Marcos Vinicius Marins Crespo e da Estrada de Santa Maria;
deste,segue confrontando com a Fazenda Santo Antônio, código do INCRA n° 513.024.005.231-7, matrícula 225 de propriedade de Agropecuária Ventania LTDA, com os seguintes azimutes e distancias: 240°41'33" e 253,1096 m até o vértice
RL_1557, de coordenadas N: 7.543.729,7145m e E: 205.159,2936m; 279°07'14" e 50,1183 m até o vértice 9, de coordenadas N: 7.543.737,6588m e E: 205.109,8089m; 342°15'11" e 16,0382 m até o vértice 10, de coordenadas
N: 7.543.752,9338m e E: 205.104,9202m; 260°17'13" e 26,5861 m até o vértice 11, de coordenadas N: 7.543.748,4483m e E: 205.078,7152m; 287°23'04" e 78,8422 m até o vértice 12, de coordenadas N: 7.543.772,0050m e
E: 205.003,4744m; 284°17'47" e 54,5130 m até o vértice 13, de coordenadas N: 7.543.785,4663m e E: 204.950,6496m; 260°21'47" e 37,8806 m até o vértice 14, de coordenadas N: 7.543.779,1250m e E: 204.913,3035m; 292°18'19" e
47,4884 m até o vértice 15, de coordenadas N: 7.543.797,1489m e E: 204.869,3685m; 328°38'15" e 28,7643 m até o vértice 16, de coordenadas N: 7.543.821,7105m e E: 204.854,3981m; 259°58'08" e 23,8670 m até o vértice 17, de
coordenadas N: 7.543.817,5533m e E: 204.830,8959m; 303°27'36" e 25,2964 m até o vértice 18, de coordenadas N: 7.543.831,5006m e E: 204.809,7919m; 263°03'25" e 130,3395 m até o vértice 19, de coordenadas N: 7.543.815,7449m e
E: 204.680,4082m; 232°26'25" e 20,7665 m até o vértice 20, de coordenadas N: 7.543.803,0859m e E: 204.663,9462m; 226°51'56" e 124,0783 m até o vértice RL_1556, de coordenadas N: 7.543.718,2519m e E: 204.573,4000m; 295°38'54" e
59,1331 m até o vértice 22, de coordenadas N: 7.543.743,8475m e E: 204.520,0935m; 272°38'42" e 23,1244 m até o vértice 23, de coordenadas N: 7.543.744,9146m e E: 204.496,9937m; 260°16'33" e 18,5963 m até o vértice 24, de
coordenadas N: 7.543.741,7736m e E: 204.478,6646m; 17°37'49" e 26,3421 m até o vértice 25, de coordenadas N: 7.543.766,8784m e E: 204.486,6429m; 278°32'25" e 34,7923 m até o vértice 26, de coordenadas N: 7.543.772,0452m e
E: 204.452,2364m; 198°07'49" e 39,9665 m até o vértice 27, de coordenadas N: 7.543.734,0630m e E: 204.439,7996m; 210°43'55" e 84,0329 m até o vértice 28, de coordenadas N: 7.543.661,8311m e E: 204.396,8569m; 125°01'52"
e 34,0205 m até o vértice 29, de coordenadas N: 7.543.642,3026m e E: 204.424,7143m; 210°42'39" e 27,5176 m até o vértice 30, de coordenadas N: 7.543.618,6442m e E: 204.410,6609m; 137°45'35" e 71,4196 m até o vértice 31, d
e coordenadas N: 7.543.565,7699m e E: 204.458,6720m; 203°18'42" e 79,6308 m até o vértice RL_1555, de coordenadas N: 7.543.492,6397m e E: 204.427,1595m; 168°49'16" e 76,9482 m até o vértice 33, de coordenadas
N: 7.543.417,1514m e E: 204.442,0776m; 160°26'01" e 77,5305 m até o vértice 34, de coordenadas N: 7.543.344,0979m e E: 204.468,0424m; 293°57'21" e 51,2836 m até o vértice 35, de coordenadas N: 7.543.364,9207m e E: 204.421,1764m;
311°36'46" e 88,9169 m até o vértice 36, de coordenadas N: 7.543.423,9697m e E: 204.354,6976m; 10°04'45" e 72,7705 m até o vértice 37, de coordenadas N: 7.543.495,6171m e E: 204.367,4332m; 293°44'51" e 45,2852 m até o vértice 38,
de coordenadas N: 7.543.513,8537m e E: 204.325,9823m; 265°20'29" e 45,6435 m até o vértice 39, de coordenadas N: 7.543.510,1466m e E: 204.280,4896m; 192°26'20" e 44,5865 m até o vértice 40, de coordenadas N: 7.543.466,6067m e
E: 204.270,8858m; 267°20'09" e 72,7289 m até o vértice 41, de coordenadas N: 7.543.463,2261m e E: 204.198,2355m; 281°10'34" e 63,4222 m até o vértice 42, de coordenadas N: 7.543.475,5190m e E: 204.136,0161m; 244°25'36" e
69,1698 m até o vértice 43, de coordenadas N: 7.543.445,6609m e E: 204.073,6226m; 290°54'34" e 130,4800 m até o vértice 44, de coordenadas N: 7.543.492,2280m e E: 203.951,7352m; 33°28'39" e 56,4231 m até o vértice 45, de
coordenadas N: 7.543.539,2906m e E: 203.982,8588m; 13°27'35" e 35,9598 m até o vértice 46, de coordenadas N: 7.543.574,2627m e E: 203.991,2289m; 72°58'28" e 21,4476 m até o vértice 47, de coordenadas N: 7.543.580,5425m e
E: 204.011,7365m; 28°34'42" e 67,6427 m até o vértice 48, de coordenadas N: 7.543.639,9438m e E: 204.044,0941m; 344°45'15" e 42,6515 m até o vértice 49, de coordenadas N: 7.543.681,0943m e E: 204.032,8785m; 318°24'18" e
36,8934 m até o vértice 50, de coordenadas N: 7.543.708,6853m e E: 204.008,3864m; 311°48'03" e
100,8504 
'''

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
e_int = list(map(int, e_string))
n_int = list(map(int, n_string))
coord = [e_int, n_int]

# Salve dataframe do Pandas e em CSV para abrir no SIG
dt_coord = pd.DataFrame(coord).transpose()
dt_coord.columns = ['E_UTM', 'N_UTM']
print(dt_coord.head(50))
