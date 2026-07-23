"""value_api — persistência, autenticação e orquestração.

A api NÃO calcula: monta a EntradaCalculo, chama o motor puro e persiste o
snapshot. Toda coluna monetária é NUMERIC (jamais DOUBLE PRECISION). Papéis e a
regra dos quatro olhos vivem aqui (PROMPT_VALUE.md §9).
"""
