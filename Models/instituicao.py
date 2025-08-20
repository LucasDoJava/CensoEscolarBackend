from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from Helpers.database import db
from flask_restful import fields as flaskFields
from typing import TYPE_CHECKING

from marshmallow import Schema, fields, validate, ValidationError
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .municipio import tb_municipio
    from .mesorregiao import tb_mesorregiao
    from .microrregiao import tb_microrregiao
    from .uf import tb_uf

tb_instituicao_fields = {
    "regiao": flaskFields.String,
    "codregiao": flaskFields.Integer,
    "sigla": flaskFields.String,
    "uf_nome": flaskFields.String,
    "coduf": flaskFields.Integer,
    "municipio_nome": flaskFields.String,
    "codmunicipio": flaskFields.Integer,
    "mesorregiao_nome": flaskFields.String,
    "codmesorregiao": flaskFields.Integer,
    "microrregiao_nome": flaskFields.String,
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

    sigla: Mapped[str] = mapped_column("uf", String) 
    uf_nome: Mapped[str] = mapped_column("nomeestado", String)
    coduf: Mapped[int] = mapped_column(ForeignKey('tb_uf.coduf'))

    municipio_nome: Mapped[str] = mapped_column("municipio", String)
    codmunicipio: Mapped[int] = mapped_column(ForeignKey('tb_municipio.codmunicipio'))

    mesorregiao_nome: Mapped[str] = mapped_column("mesorregiao", String)
    codmesorregiao: Mapped[int] = mapped_column(ForeignKey('tb_mesorregiao.codmesorregiao'))

    microrregiao_nome: Mapped[str] = mapped_column("microrregiao", String)
    codmicrorregiao: Mapped[int] = mapped_column(ForeignKey('tb_microrregiao.codmicrorregiao'))

    entidade: Mapped[str] = mapped_column(String)
    matriculas_base: Mapped[int] = mapped_column(Integer)
    ano: Mapped[int] = mapped_column(Integer)
    created: Mapped[datetime] = mapped_column(DateTime, server_default=db.func.now())

    # relacionamentos
    municipio: Mapped[tb_municipio] = relationship("tb_municipio", back_populates="instituicoes")
    uf: Mapped[tb_uf] = relationship("tb_uf", back_populates="instituicoes")
    mesorregiao: Mapped[tb_mesorregiao] = relationship("tb_mesorregiao", back_populates="instituicoes")
    microrregiao: Mapped[tb_microrregiao] = relationship("tb_microrregiao", back_populates="instituicoes")

    def __init__(self, regiao: str, codregiao: int, sigla: str, uf_nome, coduf: int, 
                 municipio_nome: str, codmunicipio: int, mesorregiao_nome: str, codmesorregiao: int,
                 microrregiao_nome: str, codmicrorregiao: int, entidade: str, 
                 codentidade: int, matriculas_base: int, ano: int):
        self.regiao = regiao
        self.codregiao = codregiao
        self.sigla = sigla
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

class InstituicaoEnsinoSchema(Schema): 
    regiao = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=20),
        error_messages={
            "required": "Nome da Região é obrigatório.",
            "null": "Nome da Região não pode ser nulo.",
            "validator_failed": "O nome da Região deve ter entre 3 e 20 caracteres."
        }
    )
    codregiao = fields.Int(
        required=True,
        validate=validate.Range(
            min=1, max=5, error="O codigo de região deve estar entre 1 e 5"),
        error_messages={
            "required": "Código da Região é obrigatório.",
            "null": "Código da Região não pode ser nulo."
        }
    )
    sigla = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=2),
        error_messages={
            "required": "Sigla é obrigatória.",
            "null": "Sigla não pode ser nulo.",
            "validator_failed": "A Sigla deve ter 2 caracteres."
        }
    )

    uf_nome = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=50),
        error_messages={
            "required": "Nome da uf é obrigatória.",
            "null": "Nome Uf não pode ser nulo.",
            "validator_failed": "Uf deve ter no min 4 e no max 50 caracteres ."
        }
    )

    UFS_VALIDAS = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24,
                   25, 26, 27, 28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 52, 53]
    coduf = fields.Int(
        required=True,
        validate=validate.OneOf(UFS_VALIDAS, error=f"Código de estado inválido. Valores aceitos: {UFS_VALIDAS}"),
        error_messages={
            "required": "Código do Estado é obrigatório.",
            "null": "Código do Estado não pode ser nulo."
        }
    )
    municipio_nome = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=150),
        error_messages={
            "required": "Município é obrigatório.",
            "null": "Município não pode ser nulo.",
            "validator_failed": "O Município deve ter entre 3 e 150 caracteres."
        }
    )
    def tamanho_cod_municipio(value):
        if len(str(value)) != 7:
            raise ValidationError("O código do município deve ter 7 dígitos.")
    codmunicipio = fields.Int(
        required=True,
        validate=tamanho_cod_municipio,
        error_messages={
            "required": "Código do Município é obrigatório.",
            "null": "Código do Município não pode ser nulo."
        }
    )
    mesorregiao_nome = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=100),
        error_messages={
            "required": "Mesorregião é obrigatória.",
            "null": "Mesorregião não pode ser nula.",
            "validator_failed": "A Mesorregião deve ter entre 3 e 100 caracteres."
        }
    )
    codmesorregiao = fields.Int(
        required=True,
        # validate=tamanho_cod_municipio,
        error_messages={
            "required": "Código de Messorregião é obrigatório.",
            "null": "Código de Messorregião não pode ser nulo."
        }
    )
    microrregiao_nome = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=100),
        error_messages={
            "required": "Microrregião é obrigatória.",
            "null": "Microrregião não pode ser nula.",
            "validator_failed": "A Microrregião deve ter entre 3 e 100 caracteres."
        }
    )
    codmicrorregiao = fields.Int(
        required=True,
      
        error_messages={
            "required": "Código de Microrregiao é obrigatório.",
            "null": "Código de Microrregiao não pode ser nulo."
        }
    )
    entidade = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=100),
        error_messages={
            "required": "Entidade é obrigatória.",
            "null": "Entidade não pode ser nula.",
            "validator_failed": "A Entidade deve ter entre 3 e 100 caracteres."
        }
    )
    codentidade = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="O valor deve ser um número inteiro positivo."),
        error_messages={
            "required": "Codigo de entidade é obrigatório.",
            "null": "Codigo de entidade não pode ser nulo."
        }
    )
    matriculas_base = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="O valor deve ser um número inteiro positivo."),
        error_messages={
            "required": "Quantidade de Matriculados é obrigatória.",
            "null": "Quantidade de Matriculados não pode ser nula."
        }
    )
    ano = fields.Int(
        required=True,
        validate=validate.Range(min=1995, max=datetime.now(
        ).year - 1, error=f"O ano deve estar entre 1995 e {datetime.now().year - 1}."),
        error_messages={
            "required": "O ano do censo é obrigatório.",
            "null": "O ano do censo não pode ser nulo."
        }
    )