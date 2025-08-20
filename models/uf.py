from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .instituicao import tb_instituicao

tb_uf_fields = {
    "coduf": flaskFields.Integer,
    "uf": flaskFields.String,
    "nomeestado": flaskFields.String,
}

class tb_uf(db.Model):
    __tablename__ = "tb_uf"

    coduf: Mapped[int] = mapped_column('coduf', Integer, primary_key=True)
    uf: Mapped[str] = mapped_column('uf', String)
    nomeestado: Mapped[str] = mapped_column('nomeestado', String)

    
    instituicoes: Mapped[List[tb_instituicao]] = relationship(
        "tb_instituicao", 
        back_populates="uf",
        cascade="all, delete-orphan"
    )

    def __init__(self, coduf: int, uf: str, nomeestado: str):
        self.coduf = coduf
        self.uf = uf
        self.nomeestado = nomeestado

    def __repr__(self):
        return f"tb_uf(cod={self.coduf}, nome={self.nomeestado})"