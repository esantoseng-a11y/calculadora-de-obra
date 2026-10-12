import os
from math import ceil
from flask import Flask, request, jsonify

app = Flask(__name__)

class Entradas:
    def __init__(
        self,
        area_construida=60,
        comprimento_paredes=75,
        pe_direito=2.8,
        banheiros=3,
        cozinhas=1,
        areas_servico=1,
        pontos_eletricos=40,
        perda=0.08,
        mao_obra=0.80,
        bdi=0.10,
        area_portas_janelas=16.14,
    ):
        self.area_construida = area_construida
        self.comprimento_paredes = comprimento_paredes
        self.pe_direito = pe_direito
        self.banheiros = banheiros
        self.cozinhas = cozinhas
        self.areas_servico = areas_servico
        self.pontos_eletricos = pontos_eletricos
        self.perda = perda
        self.mao_obra = mao_obra
        self.bdi = bdi
        self.area_portas_janelas = area_portas_janelas


def calcular(e):
    area_paredes = (e.comprimento_paredes * e.pe_direito) - e.area_portas_janelas
    concreto_fundacao = e.comprimento_paredes * 0.17
    aco_fundacao = e.comprimento_paredes * 8
    concreto_estrutura = e.area_construida * 0.07
    aco_estrutura = e.area_construida * 5.5
    tijolos = area_paredes * 25
    pontos_agua = (e.banheiros * 5) + (e.cozinhas * 3) + (e.areas_servico * 2)
    eletroduto = e.pontos_eletricos * 6
    fio25 = e.pontos_eletricos * 14
    disjuntores = ceil(e.pontos_eletricos / 8)

    materiais = (
        (concreto_fundacao * 800)
        + (aco_fundacao * 9.5)
        + (concreto_estrutura * 800)
        + (aco_estrutura * 9.5)
        + (tijolos * 1.2)
    )
    materiais *= 1 + e.perda

    mao = materiais * e.mao_obra
    subtotal = materiais + mao
    total = subtotal + (subtotal * e.bdi)

    return {
        "area_paredes": round(area_paredes, 2),
        "concreto_fundacao": round(concreto_fundacao, 2),
        "aco_fundacao": round(aco_fundacao, 2),
        "concreto_estrutura": round(concreto_estrutura, 2),
        "aco_estrutura": round(aco_estrutura, 2),
        "tijolos": round(tijolos, 0),
        "pontos_agua": pontos_agua,
        "eletroduto": eletroduto,
        "fio_25mm": fio25,
        "disjuntores": disjuntores,
        "materiais": round(materiais, 2),
        "mao_obra": round(mao, 2),
        "total": round(total, 2),
        "custo_m2": round(total / e.area_construida, 2),
    }


@app.route("/")
def index():
    return {
        "status": "ok",
        "message": "API da calculadora de obra funcionando",
        "endpoint": "/calcular"
    }


@app.route("/calcular", methods=["POST"])
def calcular_api():
    dados = request.get_json(silent=True) or {}

    e = Entradas(
        area_construida=dados.get("area_construida", 60),
        comprimento_paredes=dados.get("comprimento_paredes", 75),
        pe_direito=dados.get("pe_direito", 2.8),
        banheiros=dados.get("banheiros", 3),
        cozinhas=dados.get("cozinhas", 1),
        areas_servico=dados.get("areas_servico", 1),
        pontos_eletricos=dados.get("pontos_eletricos", 40),
        perda=dados.get("perda", 0.08),
        mao_obra=dados.get("mao_obra", 0.80),
        bdi=dados.get("bdi", 0.10),
        area_portas_janelas=dados.get("area_portas_janelas", 16.14),
    )

    return jsonify(calcular(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))