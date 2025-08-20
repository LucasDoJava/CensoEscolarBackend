from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from Helpers.database import db
from flask_restful import fields as flaskFields

if TYPE_CHECKING:
    from .instituicao import tb_instituicao

tb_mesorregiao_fields = {
    "codmesorregiao": flaskFields.Integer,
    "mesorregiao": flaskFields.String
}

class tb_mesorregiao(db.Model):
    __tablename__ = "tb_mesorregiao"

    codmesorregiao: Mapped[int] = mapped_column('codmesorregiao', Integer, primary_key=True)
    mesorregiao: Mapped[str] = mapped_column('mesorregiao', String)
    
    instituicoes: Mapped[List[tb_instituicao]] = relationship("tb_instituicao", back_populates="mesorregiao_rel", cascade="all, delete-orphan"
    )

    def __init__(self, codmesorregiao: int, mesorregiao: str):
        self.codmesorregiao = codmesorregiao
        self.mesorregiao = mesorregiao

    def __repr__(self):
        return f"tb_mesorregiao(cod={self.codmesorregiao}, nome={self.mesorregiao})"
    
    