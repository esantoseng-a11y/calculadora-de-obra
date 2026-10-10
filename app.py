
from math import ceil
from dataclasses import dataclass, asdict
import json

@dataclass
class Entradas:
    area_construida: float = 60
    comprimento_paredes: float = 75
    pe_direito: float = 2.8
    banheiros: int = 3
    cozinhas: int = 1
    areas_servico: int = 1
    pontos_eletricos: int = 40
    perda: float = 0.08
    mao_obra: float = 0.80
    bdi: float = 0.10
    area_portas_janelas: float = 16.14

class Calculadora:
    def __init__(self,e): self.e=e

    def calcular(self):
        area_paredes=(self.e.comprimento_paredes*self.e.pe_direito)-self.e.area_portas_janelas
        concreto_fundacao=self.e.comprimento_paredes*0.17
        aco_fundacao=self.e.comprimento_paredes*8
        concreto_estrutura=self.e.area_construida*0.07
        aco_estrutura=self.e.area_construida*5.5
        tijolos=area_paredes*25
        pontos_agua=(self.e.banheiros*5)+(self.e.cozinhas*3)+(self.e.areas_servico*2)
        eletroduto=self.e.pontos_eletricos*6
        fio25=self.e.pontos_eletricos*14
        disjuntores=ceil(self.e.pontos_eletricos/8)

        materiais=(concreto_fundacao*800)+(aco_fundacao*9.5)+(concreto_estrutura*800)+(aco_estrutura*9.5)+(tijolos*1.2)
        materiais*=1+self.e.perda
        mao=materiais*self.e.mao_obra
        subtotal=materiais+mao
        total=subtotal+(subtotal*self.e.bdi)

        return {
            'area_paredes':round(area_paredes,2),
            'concreto_fundacao':round(concreto_fundacao,2),
            'aco_fundacao':round(aco_fundacao,2),
            'concreto_estrutura':round(concreto_estrutura,2),
            'aco_estrutura':round(aco_estrutura,2),
            'tijolos':round(tijolos,0),
            'pontos_agua':pontos_agua,
            'eletroduto':eletroduto,
            'fio_25mm':fio25,
            'disjuntores':disjuntores,
            'materiais':round(materiais,2),
            'mao_obra':round(mao,2),
            'total':round(total,2),
            'custo_m2':round(total/self.e.area_construida,2)
        }

if __name__=='__main__':
    e=Entradas()
    r=Calculadora(e).calcular()
    print(json.dumps(r,indent=2,ensure_ascii=False))
