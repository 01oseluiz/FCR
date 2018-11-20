# FCR
Repositório para trabalhos de robótica.  

# SISTEMA E VERSÕES
Sistema Operacional: Ubuntu 18.04  
RosDistro:  Melodic [Full]  
Roscpp: 1.14.3  
Rospy: 1.14.3  
Python: 2.7.15  


# ROTEIRO 5

## LÓGICA
Dado que o robo esta em um no valido (já mapeado).  
Ele irá pegar todos os pontos que formam este nó e andará pelas suas arestas criando o mapa de ocupação.

## OBSERVAÇÔES
* O robô irá criar o mapa de ocupação para o nó em que estiver no momento da execução do programa.    
* A imagem que indica as divisões e os números de cada nó esta em: assets > imgs > FGH.pgm  
* A saida do programa (mapa de ocupação) e dada em um txt localizado em: assets > text > map_NumeroDoNo.txt