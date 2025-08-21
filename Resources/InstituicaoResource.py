from flask import request, abort
from flask_restful import Resource, marshal

from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from Helpers.database import db
from Helpers.Logging import logger, log_exception 

from Models.instituicao import tb_instituicao_fields, tb_instituicao, InstituicaoEnsinoSchema


class InstituicoesResouce(Resource):
    def get(self, ano):
        logger.info("Get - Instituições por ano")

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        sigla = request.args.get('sigla')  # <- UF opcional (ex.: AM, SP, PB)

        try:
            # monta a query base por ano
            query = db.select(tb_instituicao).filter_by(ano=ano)

            # aplica filtro por UF, se enviado
            if sigla:
                query = query.filter_by(sigla=sigla)

            instituicoes = (
                db.session.execute(
                    query.offset((page - 1) * per_page).limit(per_page)
                )
                .scalars()
                .all()
            )

            logger.info(f"Instituições do ano {ano} retornadas com sucesso")
            return marshal(instituicoes, tb_instituicao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao listar instituições.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao listar instituições")
            abort(500, description="Ocorreu um erro inesperado.")


class NovaInstituicaoResouce(Resource):
    def post(self):
        logger.info("Post - Instituição")
        instituicao_schema = InstituicaoEnsinoSchema()
        instituicao_data = request.get_json()

        try:
            validated_data = instituicao_schema.load(instituicao_data)
            nova_instituicao = tb_instituicao(**validated_data)

            db.session.add(nova_instituicao)
            db.session.commit()

            logger.info(f"Nova instituição com codigo {nova_instituicao.codentidade} cadastrada com sucesso")
            return marshal(nova_instituicao, tb_instituicao_fields), 201
        
        except ValidationError as err:
            logger.warning(f"Erro(s) na validação ao inserir nova instituição: \n\t{err.messages}")
            return {"mensagem": "Falha na validação dos dados. Verifique os campos e tente novamente.", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir nova instituição.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir nova instituição")
            abort(500, description="Ocorreu um erro inesperado.")


class InstituicaoResouce(Resource):
    def get(self, ano, codentidade):
        logger.info(f"Get - Instituição por ano {ano} e código de entidade: {codentidade}")

        try:
            instituicao = db.session.execute(
                db.select(tb_instituicao)
                .filter_by(ano=ano, codentidade=codentidade)
            ).scalar_one_or_none()

            if instituicao is None:
                logger.warning(f"Instituição com ano {ano} e código {codentidade} não encontrada.")
                return {"mensagem": "Instituição não encontrada."}, 404

            logger.info(f"Instituição com ano {ano} e codigo {codentidade} retornada com sucesso")            
            return marshal(instituicao, tb_instituicao_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar instituição por ano e código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar instituição")
            abort(500, description="Ocorreu um erro inesperado.")
        
    def put(self, ano, codentidade):
        logger.info(f"Put - Tentativa de atualizar instituição com ano {ano} e código: {codentidade}")
        instituicao_schema = InstituicaoEnsinoSchema()
        instituicao_data = request.get_json()

        try:
            instituicao = db.session.execute(
                db.select(tb_instituicao)
                .filter_by(ano=ano, codentidade=codentidade)
            ).scalar_one_or_none()

            if instituicao is None:
                logger.warning(f"Instituição com ano {ano} e código {codentidade} não encontrada para atualizar.")
                return {"mensagem": "Instituição não encontrada."}, 404

            validated_data = instituicao_schema.load(instituicao_data, partial=True)

            for key, value in validated_data.items():
                setattr(instituicao, key, value)

            db.session.commit()

            logger.info(f"Instituição com ano {ano} e código {codentidade} atualizada com sucesso.")
            return {"mensagem": "Instituição atualizada com sucesso."}, 200
        
        except ValidationError as err:
            logger.warning(f"Erro de validação ao atualizar instituição com código {codentidade} do ano {ano}\n\t{err.messages}")
            return {"mensagem": "Falha na validação dos dados. Verifique os campos e tente novamente.", "detalhes": err.messages}, 422
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar instituição.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar instituição")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, ano, codentidade):
        logger.info(f"Delete - Tentativa de deleção da instituição com código: {codentidade}")

        try:
            instituicao = db.session.execute(
                db.select(tb_instituicao)
                .filter_by(ano=ano, codentidade=codentidade)
            ).scalar_one_or_none()

            if instituicao is None:
                logger.warning(f"Instituição com ano {ano} e código {codentidade} não encontrada para deleção.")
                return {"mensagem": "Instituição não encontrada."}, 404
            
            db.session.delete(instituicao)
            db.session.commit()

            logger.info(f"Instituição com ano {ano} e código {codentidade} removida com sucesso.")
            return {"mensagem": "Instituição removida com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar instituição.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar instituição")
            abort(500, description="Ocorreu um erro inesperado.")
