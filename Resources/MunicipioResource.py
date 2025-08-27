from flask import request, abort
from flask_restful import Resource, marshal
from sqlalchemy.exc import SQLAlchemyError

from Helpers.database import db
from Helpers.Logging import logger, log_exception 
from Helpers.app import cache  

from Models.municipio import tb_municipio_fields, tb_municipio

class MunicipiosResouce(Resource):
    @cache.cached(timeout=3600, query_string=True) 
    def get(self):
        logger.info(f"Get - Todos os municipios")

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))

        try:
            municipios = db.session.execute(
                db.select(tb_municipio)
                .offset((page - 1) * per_page)
                .limit(per_page)
            ).scalars().all()

            logger.info(f"Municipios retornados com sucesso")
            return marshal(municipios, tb_municipio_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar municipios.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar municipios")
            abort(500, description="Ocorreu um erro inesperado.")

    def post(self):
        logger.info("Post - Municipio")
        municipio_data = request.get_json()

        try:
            novo_municipio = tb_municipio(**municipio_data)

            db.session.add(novo_municipio)
            db.session.commit()

            
            cache.delete_memoized(MunicipiosResouce.get)
            logger.info(f"Cache invalidado após inserção de novo municipio")

            logger.info(f"Novo municipio com codigo {novo_municipio.codmunicipio} cadastrado com sucesso")
            return marshal(novo_municipio, tb_municipio_fields), 201
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao inserir novo municipio.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao inserir novo municipio")
            abort(500, description="Ocorreu um erro inesperado.")

class MunicipioResource(Resource):
    @cache.cached(timeout=3600, query_string=True)  
    def get(self, codmunicipio):
        logger.info(f"Get - Municipio por código: {codmunicipio}")

        try:
            municipio = db.session.execute(
                db.select(tb_municipio)
                .filter_by(codmunicipio=codmunicipio)
            ).scalar_one_or_none()

            if municipio is None:
                logger.warning(f"Municipio com código {codmunicipio} não encontrado.")
                return {"mensagem": "Municipio não encontrado."}, 404

            logger.info(f"Municipio com código {codmunicipio} retornado com sucesso")            
            return marshal(municipio, tb_municipio_fields), 200

        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao buscar municipio por código.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao buscar municipio")
            abort(500, description="Ocorreu um erro inesperado.")

    def put(self, codmunicipio):
        logger.info(f"Put - Tentativa de atualizar municipio com código: {codmunicipio}")
        municipio_data = request.get_json()

        try:
            municipio = db.session.execute(
                db.select(tb_municipio)
                .filter_by(codmunicipio=codmunicipio)
            ).scalar_one_or_none()

            if municipio is None:
                logger.warning(f"Municipio com código {codmunicipio} não encontrado para atualizar.")
                return {"mensagem": "Municipio não encontrado."}, 404

            for key, value in municipio_data.items():
                setattr(municipio, key, value)

            db.session.commit()

            
            cache.delete_memoized(MunicipiosResouce.get)
            cache.delete_memoized(MunicipioResource.get, codmunicipio)
            logger.info(f"Caches invalidados após atualização do municipio {codmunicipio}")

            logger.info(f"Municipio com código {codmunicipio} atualizado com sucesso.")
            return {"mensagem": "Municipio atualizado com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao atualizar municipio.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception(f"Erro inesperado ao atualizar municipio")
            abort(500, description="Ocorreu um erro inesperado.")

    def delete(self, codmunicipio):
        logger.info(f"Delete - Tentativa de deleção municipio com código: {codmunicipio}")

        try:
            municipio = db.session.execute(
                db.select(tb_municipio)
                .filter_by(codmunicipio=codmunicipio)
            ).scalar_one_or_none()

            if municipio is None:
                logger.warning(f"Municipio com código {codmunicipio} não encontrado para deleção.")
                return {"mensagem": "Municipio não encontrado."}, 404
            
            db.session.delete(municipio)
            db.session.commit()

           
            cache.delete_memoized(MunicipiosResouce.get)
            cache.delete_memoized(MunicipioResource.get, codmunicipio)
            logger.info(f"Caches invalidados após deleção do municipio {codmunicipio}")

            logger.info(f"Municipio com código {codmunicipio} removido com sucesso.")
            return {"mensagem": "Municipio removido com sucesso."}, 200
        
        except SQLAlchemyError:
            log_exception("Exception SQLAlchemy ao deletar municipio.")
            db.session.rollback()
            abort(500, description="Problema com o banco de dados.")
        except Exception:
            log_exception("Erro inesperado ao deletar municipio")
            abort(500, description="Ocorreu um erro inesperado.")