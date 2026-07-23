"""Modelo de dados (esqueleto) — PROMPT_VALUE.md §8.

Colunas monetárias usam NUMERIC (SQLAlchemy `Numeric`), NUNCA DOUBLE PRECISION.
Dados pessoais (CPF, RG, endereço) são cifrados em repouso e mascarados por padrão
na interface — não entram no cálculo e não aparecem aqui como texto puro.

Este é o esqueleto da Fase 4: as tabelas do §8 com seus campos essenciais. Migrações
(Alembic) e relacionamentos completos entram na Fase 4.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# Precisão monetária padrão do projeto. 2 casas na apresentação; guardamos margem
# para fatores. Valores sempre Decimal, nunca float.
Dinheiro = Numeric(18, 2)
Fator = Numeric(28, 12)


class Processo(Base):
    __tablename__ = "processo"
    id: Mapped[int] = mapped_column(primary_key=True)
    numero_cnj: Mapped[str] = mapped_column(String(25), unique=True)
    comarca: Mapped[str] = mapped_column(String(120))
    ente_devedor: Mapped[str] = mapped_column(String(200))
    esfera: Mapped[str] = mapped_column(String(20))  # municipal, na v1
    teto_rpv: Mapped[Decimal | None] = mapped_column(Dinheiro, nullable=True)


class Titulo(Base):
    __tablename__ = "titulo"
    id: Mapped[int] = mapped_column(primary_key=True)
    processo_id: Mapped[int] = mapped_column(ForeignKey("processo.id"))
    tipo: Mapped[str] = mapped_column(String(30))  # sentenca | acordao
    data_transito: Mapped[date | None] = mapped_column(nullable=True)
    hash_pdf: Mapped[str] = mapped_column(String(64))
    dispositivo_json: Mapped[str] = mapped_column(Text)


class Exequente(Base):
    __tablename__ = "exequente"
    id: Mapped[int] = mapped_column(primary_key=True)
    processo_id: Mapped[int] = mapped_column(ForeignKey("processo.id"))
    matricula: Mapped[str] = mapped_column(String(40))
    data_admissao: Mapped[date]
    data_efetivacao: Mapped[date | None] = mapped_column(nullable=True)
    regime: Mapped[str] = mapped_column(String(40))
    # CPF/RG/endereço: colunas cifradas, definidas na Fase 4 com o esquema de cifragem.


class Marco(Base):
    __tablename__ = "marco"
    id: Mapped[int] = mapped_column(primary_key=True)
    processo_id: Mapped[int] = mapped_column(ForeignKey("processo.id"))
    tipo: Mapped[str] = mapped_column(String(20))  # ajuizamento|citacao|transito|requisitorio
    data: Mapped[date]
    fonte_doc: Mapped[str] = mapped_column(String(200))


class Verba(Base):
    __tablename__ = "verba"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo_id: Mapped[int] = mapped_column(ForeignKey("titulo.id"))
    tipo: Mapped[str] = mapped_column(String(40))  # "pasep" na v1
    base_legal: Mapped[str] = mapped_column(String(300))
    parametros_json: Mapped[str] = mapped_column(Text)


class Parcela(Base):
    __tablename__ = "parcela"
    id: Mapped[int] = mapped_column(primary_key=True)
    verba_id: Mapped[int] = mapped_column(ForeignKey("verba.id"))
    competencia: Mapped[date]
    valor_originario: Mapped[Decimal] = mapped_column(Dinheiro)
    origem_do_valor: Mapped[str] = mapped_column(String(200))
    vencimento: Mapped[date]


class RegimeTemporal(Base):
    __tablename__ = "regime_temporal"
    id: Mapped[int] = mapped_column(primary_key=True)
    norma: Mapped[str] = mapped_column(String(200))
    escopo: Mapped[str] = mapped_column(String(80))
    vigencia_ini: Mapped[date | None] = mapped_column(nullable=True)
    vigencia_fim: Mapped[date | None] = mapped_column(nullable=True)
    regra_correcao: Mapped[str] = mapped_column(String(60))
    regra_juros: Mapped[str] = mapped_column(String(60))
    versao_tabela: Mapped[int]
    status: Mapped[str] = mapped_column(String(20))


class SerieIndice(Base):
    """Append-only. Revisão de índice cria versão nova, jamais sobrescreve."""

    __tablename__ = "serie_indice"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(60))
    competencia: Mapped[date]
    valor: Mapped[Decimal] = mapped_column(Fator)
    fonte: Mapped[str] = mapped_column(String(40))
    versao: Mapped[str] = mapped_column(String(40))
    hash: Mapped[str] = mapped_column(String(64))
    data_coleta: Mapped[datetime]


class ExecucaoCalculo(Base):
    """Snapshot congelado da emissão. Recalcular reproduz byte a byte."""

    __tablename__ = "execucao_calculo"
    id: Mapped[int] = mapped_column(primary_key=True)
    snapshot_json: Mapped[str] = mapped_column(Text)
    versao_motor: Mapped[str] = mapped_column(String(20))
    versoes_series: Mapped[str] = mapped_column(Text)  # json {nome: versao}
    hash_entrada: Mapped[str] = mapped_column(String(64))
    hash_saida: Mapped[str] = mapped_column(String(64))
    emitido_por: Mapped[str] = mapped_column(String(80))
    revisado_por: Mapped[str] = mapped_column(String(80))  # quatro olhos: != emitido_por
    emitido_em: Mapped[datetime]


class LinhaMemorial(Base):
    """Trilha de auditoria por célula: dispositivo, norma, série."""

    __tablename__ = "linha_memorial"
    id: Mapped[int] = mapped_column(primary_key=True)
    execucao_id: Mapped[int] = mapped_column(ForeignKey("execucao_calculo.id"))
    parcela_id: Mapped[int] = mapped_column(ForeignKey("parcela.id"))
    etapa: Mapped[str] = mapped_column(String(40))
    fator: Mapped[Decimal] = mapped_column(Fator)
    valor: Mapped[Decimal] = mapped_column(Dinheiro)
    ref_dispositivo: Mapped[str] = mapped_column(String(300))
    ref_norma: Mapped[str] = mapped_column(String(300))
    ref_serie: Mapped[str] = mapped_column(String(120))


class Desfecho(Base):
    """Faz o corpus de validação crescer sozinho. Toda impugnação vira regressão."""

    __tablename__ = "desfecho"
    id: Mapped[int] = mapped_column(primary_key=True)
    execucao_id: Mapped[int] = mapped_column(ForeignKey("execucao_calculo.id"))
    status: Mapped[str] = mapped_column(String(20))  # homologado|impugnado|pago
    fundamento_impugnacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[date]
