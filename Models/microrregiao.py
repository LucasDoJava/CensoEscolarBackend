from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from Helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .instituicao import tb_instituicao

tb_microrregiao_fields = {
    "codmicrorregiao": flaskFields.Integer,
    "microrregiao": flaskFields.String
}

class tb_microrregiao(db.Model):
    __tablename__ = "tb_microrregiao"

    codmicrorregiao: Mapped[int] = mapped_column('codmicrorregiao', Integer, primary_key=True)
    microrregiao: Mapped[str] = mapped_column('microrregiao', String)

    
    instituicoes: Mapped[tb_instituicao] = relationship("tb_instituicao", back_populates="microrregiao_rel")

    def __init__(self, codmicrorregiao: int, microrregiao: str):
        self.codmicrorregiao = codmicrorregiao
        self.microrregiao = microrregiao

    def __repr__(self):
        return f"tb_microrregiao(cod={self.codmicrorregiao}, nome={self.microrregiao})"