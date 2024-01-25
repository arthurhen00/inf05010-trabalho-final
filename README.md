# Otimização Combinatória - Trabalho Final (INF05010)

## Descrição do Projeto

Este trabalho tem como objetivo o desenvolvimento de uma formulação inteira e a implementação de uma meta-heurística para resolver um dos seguintes problemas de otimização combinatória: Bin Packing, Multidimensional 0-1 Knapsack ou Set Packing. O semestre correspondente é o 23/2, ministrado pelo Professor Henrique Becker.

## Ferramentas Necessárias  
### Julia 
Certifique-se de ter a linguagem de programação Julia instalada em seu sistema.  
1. Caso a linguagem Julia não esteja disponível: https://julialang.org/downloads/
2. Caso Julia esteja instalada mas o JuMP/GLPK não estejam instalados, execute a
seguinte linha no terminal Julia:
```
import Pkg; Pkg.add("JuMP"); Pkg.add("GLPK")
```

### Python  
Certifique-se de ter a linguagem de programação Python instalada em seu sistema.  
1. Caso a linguagem Python não esteja instalada: https://www.python.org/downloads/


## Como utilizar
O algoritmo leva como entrada 4 parâmetros, sendo eles:
- O caminho para o arquivo da instância;
- O fator de aleatoriedade (alpha) usado no GRASP, na fase de construção da soluçao, seleciona uma ds alpha melhores soluções de acordo com o critério guloso, aceita valores entre 1 e 100;
- O número máximo de iterações do GRASP (opcional: padräo );
- A quantidade de iterações da busca local
- A seed de aleatoriedade

Para executar o algoritmo execute o seguinte comando:
python (caminho para o script) (caminho para o arquivo da instância) [-a=alpha] [-i=max iterações do GRASP] [-s=seed] [-d=max iterações da busca local]

O comando: 
      python (caminho para o script) -h 
indica quais argumentos o script recebe.


## Relatório: 
O entregável relatório/experimentos consiste em:  
- [ ] Descrição clara e completa da formulação inteira empregada.  
- [ ] Descrição clara e completa da meta-heurística desenvolvida:  
  - [ ] Escolha de representação do problema.  
  - [ ] Construção da solução inicial.  
  - [ ] Principais estruturas de dados  
  - [ ] Vizinhança e a estratégia de escolha de vizinhos (quando aplicável).  
  - [ ] Processo de recombinação e factibilização (quando aplicável).  
  - [ ] Parâmetros do método (valores usados nos experimentos).  
  - [ ] Critério de parada (NAO pode ser tempo).  
- [ ] Tabela dos resultados de 10 execuções da meta-heurística sobre cada uma das instâncias (i.e., cada linha representa um par de uma instância e de uma semente de aleatoriedade, a qual é diferente para cada execução, OU uma tabela com cabeçalho + 10 linhas para cada instância) com as seguintes colunas:  
  - [ ] Valor da solução inicial da meta-heurística: Si.  
  - [ ] Valor da melhor solução encontrada pela meta-heurítica: Sh.  
  - [ ] Tempo de execução da meta-heurística (segundos): H T (s).  
  - [ ] Valor da solução encontrada pela formulação: Sf.  
  - [ ] Caso termine por limite de tempo, o limite superior: Uf.  
  - [ ] Tempo de execução da formulação (segundos): F T (s).  
     

https://docs.google.com/document/d/12v9l1n3OciCzPK5jhdePC-mQr0RAK0PfQZrxRTS1UK4/edit?usp=sharing
