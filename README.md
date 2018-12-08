# FCR - UnB - 2018/2
Repositório para trabalhos de robótica: https://github.com/01oseluiz/FCR  


# TRABALHO 2
**Video:**  
&emsp; Pasta raiz > Robo_em_funcionamento.mp4  

**Documentação, como usar, referências e outros:**  
&emsp; **(PDF)** Pasta raiz > documentação.pdf  
&emsp; **(HTML)** Pasta raiz > documentação.html  
&emsp; **(WIKI)** [FCR/wiki](https://github.com/01oseluiz/FCR/wiki)

> Recomenda-se a leitura na wiki pois a página é mais dinâmica e estruturada


## VISÃO GERAL DO TRABALHO

## OBJETIVOS
- Deslocar o robô por 10 nós do mapa topológico
- Construir a grade de ocupação de cada nó visitado
- Com o mapa contruido ir de um ponto A ao ponto B
- Não colidir com nenhum objeto ao deslocar-se de A a B
- Exibir no terminal a posição do robô em realação ao mapa ocupacional e topológico

## ABORDAGEM UTILIZADA
### Mover do nó inicial para o nó B e criar o mapa ocupacional para cada nó
- Realizar uma leitura 360 do ambiente para o primeiro nó, verificando o que há atrás
- Calcular a rota para até o nó B
- Andar x distância em diração ao proximo nó, e realizar um escaneamento para o mapa
- Ao cruzar de um nó para o outro, salvar o mapa no arquivo e inicializar outro mapa para o nó atual
- Repetir até o ultimo nó
- Ao chegar no centro do nó final, realizar um untimo escaneamento e salvar o mapa

### Mover do ponto inicial para o ponto final, exibindo a posição do robo no mapa no terminal
- Calcular a rota até o ponto final
- Ler do arquivo o mapa do nó atual
- Andar uma distância x em direção ao próximo nó, e exibir na tela o mapa com a posição do robo atual
- Repetir até o ultimo nó
- Ao chegar no centro do ultimo nó, mover o robo até o ponto entrado pelo usuario


## COMO USAR
- Abra o terminal na pasta src
- De permissão de execução para o arquivo 1600324458_main.py
- Rode o arquivo supracitado
- Selecione a opção no menu que aparecerá
- Para a opção 1:
    - Entre com o numero do nó destino
    - Entre com a escala para criação do mapa, onde 1 é escala real, ou seja, para cada 1 unidade inteira no mapa será um bloco,
    tenha em mente que o mapa FGH inteiro possui cerca de 140 unidades em ponto flutuante
    - Recomenda-se para visualização em tela-cheia no terminal a escala 0.7 (0.7 unidade é o tamanho de um bloco no mapa ocupacional)
    - O robo se moverá até o centro do nó final e criara os mapas na pasta text
- Para a opção 2:
    - Entre com as coordenadas x e y do ultimo ponto, individualmente (pode-se utilizar os pontos do grafo.txt como base)
    - O robo irá se mover até o ponto indicado, exibindo no terminal o mapa ocupacional e sua posição atual dentro dele

## OBS
- Alguns blocos ficam em branco, mesmo sendo preenchidos devido aos arredondamentos e baixa resolução utilizada
tornando alguns pontos preenchidos mesmo vázios e outros vázios mesmo estando cheios
- Nós mapeados do número 1 ao 78 (arquivo: text > grafo.txt)
- É possível visualizar a divisão dos nos no arquivo: imgs > FGH.pgm