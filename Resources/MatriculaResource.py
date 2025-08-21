from flask import request, abort
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from Helpers.database import db
from Helpers.Logging import logger, log_exception
from Models.instituicao import tb_instituicao


class MatriculasPorUFResource(Resource):
    def get(self, ano):
        logger.info(f"Get - Matrículas por UF no ano {ano}")

        try:
            resultados = db.session.execute(
                db.select(
                    tb_instituicao.sigla,
                    func.sum(tb_instituicao.matriculas_base).label("total_matriculas")
                )
                .filter_by(ano=ano)
                .group_by(tb_instituicao.sigla)
                .order_by(tb_instituicao.sigla)
            ).all()

            dados = [
                {"uf": sigla, "total_matriculas": int(total or 0)}
                for sigla, total in resultados
            ]

            logger.info(f"Matrículas por UF no ano {ano} retornadas com sucesso.")
            return {"ano": ano, "dados": dados}, 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao consultar matrículas por UF.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao consultar matrículas por UF")
            abort(500, description="Ocorreu um erro inesperado.")


class MatriculasPorRegiaoResource(Resource):
    def get(self, ano):
        logger.info(f"Get - Matrículas por Região no ano {ano}")

        try:
            resultados = db.session.execute(
                db.select(
                    tb_instituicao.regiao,
                    func.sum(tb_instituicao.matriculas_base).label("total_matriculas")
                )
                .filter_by(ano=ano)
                .group_by(tb_instituicao.regiao)
                .order_by(tb_instituicao.regiao)
            ).all()

            dados = [
                {"regiao": regiao, "total_matriculas": int(total or 0)}
                for regiao, total in resultados
            ]

            logger.info(f"Matrículas por Região no ano {ano} retornadas com sucesso.")
            return {"ano": ano, "dados": dados}, 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao consultar matrículas por Região.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao consultar matrículas por Região")
            abort(500, description="Ocorreu um erro inesperado.")
