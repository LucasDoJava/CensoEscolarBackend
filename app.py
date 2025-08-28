from Helpers.app import app, api
from Helpers.database import db
from flask_cors import CORS

from Models import uf, mesorregiao, microrregiao, municipio, instituicao

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

# Resources
from Resources.UfResource import UfsResouce
from Resources.InstituicaoResource import InstituicoesResouce
from Resources.MesorregiaoResource import MesorregioesResouce
from Resources.MicrorregiaoResource import MicrorregioesResouce
from Resources.MunicipioResource import MunicipiosResouce
from Resources.MatriculaResource import (
    MatriculasPorUFResource,
    MatriculasPorRegiaoResource
)

# Rotas
api.add_resource(UfsResouce, "/ufs")

api.add_resource(
    InstituicoesResouce,
    "/instituicoes",            
    "/instituicoes/<int:ano>",  
)

api.add_resource(MesorregioesResouce, "/mesorregioes")
api.add_resource(MicrorregioesResouce, "/microrregioes")
api.add_resource(MunicipiosResouce, "/municipios")


                  
api.add_resource(MatriculasPorUFResource, "/matriculas/uf/<int:ano>")    
api.add_resource(MatriculasPorRegiaoResource, "/matriculas/regiao/<int:ano>")  