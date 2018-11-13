# FCR
Repositório para trabalhos de robótica

# SISTEMA E VERSÕES
Sistema Operacional: Ubuntu 18.04  
RosDistro:  Melodic [Full]  
Roscpp: 1.14.3  
Rospy: 1.14.3  
Python: 2.7.15  


# ORGANIZAÇÃO DOS ARQUIVOS:

 assets:                                    #Pasta contendo arquivos não script  
    imgs:                                   #Pasta com imagens utilizadas  
        FGH.pgm                                 #Imagem do mapa modificada, possuindo os quadrantes e número de cada no  
    text:                                   #Pasta com arquivos texto  
        grafo.txt                               #Arquivo texto contendo as cordenadas de cado no e seus adjacentes  

 src:                                       #Pasta contendo os scripts e modulos  
    160032458_main.py                           #Arquivo principal (executável)  
    160032458_set_grapho.py                     #Arquivo gerador do arquivo grafo.txt  
    cords_calc.py                               #Modulo que realiza os calculos relacionados a cordenadas  
    data.py                                     #Modulo que captura e armazena todos os dados que seram manipulados  
    grapho.py                                   #Modulo que gera o grapho a partir do arquivo grapho.txt  
    move_logic.py                               #Modulo que realiza a logica de movimentação e desvio do robo para alcançar um dado ponto  
    
OBS: alguns pontos ficaram mals mapeados, dificultando a passagem do robô por caminhos estreitos  
OBS2: iniciar o robô no canto superior esquerdo, pois o inicio do grafo se encontra la, como pode ser visto na imagem FGH.pgm  
