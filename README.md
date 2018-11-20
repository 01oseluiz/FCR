# FCR
Repositório para trabalhos de robótica: https://github.com/01oseluiz/FCR

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

# ROTEIRO 6

## LÓGICA
Dado que até aqui o robo já possui a logica de caminhos intermediarios,
a logica adicional para mover o robo de um ponto a outro por meio dos nós necessita somente
do calculo da rota, e a alteração na main.py para movimentar o robo pela rota traçada

## OBSERVAÇÕES
* Veja a relação de nós e seus números em assets > imgs > FGH.pgm
* O calculo de rotas esta em graph -> (calc_route, convert_graph_to_py_format, find_path)
* E a sua execução é realizada diretamente pela main
* Faça um teste básico primeiro, coloque o robô no nó 1 (canto superior esquerdo) para ir ao nó 7

## ERROS
* Logica para definição se o robo está ou não em um nó, possui falhas caso a area seja muito grande ou deformada.