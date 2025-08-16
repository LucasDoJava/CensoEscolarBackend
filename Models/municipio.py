from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from Helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .instituicao import tb_instituicao

tb_municipio_fields = {
    "idmunicipio": flaskFields.Integer,
    "nome_municipio": flaskFields.String
}

class tb_municipio(db.Model):
    __tablename__ = "tb_municipio"

    idmunicipio: Mapped[int] = mapped_column('idmunicipio', Integer, primary_key=True)
    nome_municipio: Mapped[str] = mapped_column('nomemunicipio', String)

    instituicoes: Mapped[List[tb_instituicao]] = relationship(
    "tb_instituicao", 
    back_populates="municipio_rel",
    primaryjoin="tb_municipio.idmunicipio == tb_instituicao.codmunicipio"
    )

    def __init__(self, idmunicipio: int, nome_municipio: str):
        self.idmunicipio = idmunicipio
        self.nome_municipio = nome_municipio

    def __repr__(self):
        return f"tb_municipio(id={self.idmunicipio}, nome={self.nome_municipio})"