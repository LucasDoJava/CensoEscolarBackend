from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from Helpers.database import db
from flask_restful import fields as flaskFields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .municipio import tb_municipio
    from .mesorregiao import tb_mesorregiao
    from .microrregiao import tb_microrregiao
    from .uf import tb_uf

tb_instituicao_fields = {
    "regiao": flaskFields.String,
    "codregiao": flaskFields.Integer,
    "uf": flaskFields.String,
    "coduf": flaskFields.Integer,
    "municipio": flaskFields.String,
    "codmunicipio": flaskFields.Integer,
    "mesorregiao": flaskFields.String,
    "codmesorregiao": flaskFields.Integer,
    "microrregiao": flaskFields.String,
    "codmicrorregiao": flaskFields.Integer,
    "entidade": flaskFields.String,
    "codentidade": flaskFields.Integer,
    "matriculas_base": flaskFields.Integer,
    "ano": flaskFields.Integer,
    "created": flaskFields.DateTime(dt_format='iso8601')
}

class tb_instituicao(db.Model):
    __tablename__ = "tb_instituicao"

    codentidade: Mapped[int] = mapped_column(Integer, primary_key=True)
    regiao: Mapped[str] = mapped_column(String)
    codregiao: Mapped[int] = mapped_column(Integer) 

    uf_nome: Mapped[str] = mapped_column("uf", String)  # sigla da UF
    coduf: Mapped[int] = mapped_column(ForeignKey('tb_uf.coduf'))

    municipio_nome: Mapped[str] = mapped_column("municipio", String)
    codmunicipio: Mapped[int] = mapped_column(ForeignKey('tb_municipio.idmunicipio'))

    mesorregiao_nome: Mapped[str] = mapped_column("mesorregiao", String)
    codmesorregiao: Mapped[int] = mapped_column(ForeignKey('tb_mesorregiao.codmesorregiao'))

    microrregiao_nome: Mapped[str] = mapped_column("microrregiao", String)
    codmicrorregiao: Mapped[int] = mapped_column(ForeignKey('tb_microrregiao.codmicrorregiao'))

    entidade: Mapped[str] = mapped_column(String)
    matriculas_base: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=db.func.now())

    # relacionamentos
    municipio_rel: Mapped[tb_municipio] = relationship("tb_municipio", back_populates="instituicoes")
    uf_rel: Mapped[tb_uf] = relationship("tb_uf", back_populates="instituicoes")
    mesorregiao_rel: Mapped[tb_mesorregiao] = relationship("tb_mesorregiao", back_populates="instituicoes")
    microrregiao_rel: Mapped[tb_microrregiao] = relationship("tb_microrregiao", back_populates="instituicoes")

    def __init__(self, regiao: str, codregiao: int, uf_nome: str, coduf: int, 
                 municipio_nome: str, codmunicipio: int, mesorregiao_nome: str, codmesorregiao: int,
                 microrregiao_nome: str, codmicrorregiao: int, entidade: str, 
                 codentidade: int, matriculas_base: int, ano: int):
        self.regiao = regiao
        self.codregiao = codregiao
        self.uf_nome = uf_nome
        self.coduf = coduf
        self.municipio_nome = municipio_nome
        self.codmunicipio = codmunicipio
        self.mesorregiao_nome = mesorregiao_nome
        self.codmesorregiao = codmesorregiao
        self.microrregiao_nome = microrregiao_nome
        self.codmicrorregiao = codmicrorregiao
        self.entidade = entidade
        self.codentidade = codentidade
        self.matriculas_base = matriculas_base
        self.ano = ano

    def __repr__(self):
        return f"tb_instituicao(cod={self.codentidade}, entidade={self.entidade})"
