from Helpers.app import app, api
from Helpers.database import db
from Helpers.CORS import cors
from flask_cors import CORS

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

from Models import uf, mesorregiao, microrregiao, municipio, instituicao

from Resources.InstituicaoResource import InstituicoesResouce, NovaInstituicaoResouce, InstituicaoResouce
from Resources.UfResource import UfsResouce, UfResource
from Resources.MesorregiaoResource import MesorregioesResouce, MesorregiaoResource
from Resources.MicrorregiaoResource import MicrorregioesResouce, MicrorregiaoResource
from Resources.MunicipioResource import MunicipiosResouce, MunicipioResource

from Resources.MatriculaResource import MatriculasPorRegiaoResource, MatriculasPorUFResource


api.add_resource(UfsResouce, '/ufs')
api.add_resource(UfResource, '/uf/<int:coduf>')

api.add_resource(MesorregioesResouce, '/mesorregioes')
api.add_resource(MesorregiaoResource, '/mesorregiao/<int:codmesorregiao>')

api.add_resource(MicrorregioesResouce, '/microrregioes')
api.add_resource(MicrorregiaoResource, '/microrregiao/<int:codmicrorregiao>')

api.add_resource(MunicipiosResouce, '/municipios')
api.add_resource(MunicipioResource, '/municipio/<int:codmunicipio>')

api.add_resource(NovaInstituicaoResouce, '/instituicoes')
api.add_resource(InstituicoesResouce, '/instituicoes/<int:ano>')
api.add_resource(InstituicaoResouce, '/instituicoes/<int:ano>/<int:codentidade>')

api.add_resource(MatriculasPorUFResource, "/instituicoes/<int:ano>/matriculas/uf")
api.add_resource(MatriculasPorRegiaoResource, "/instituicoes/<int:ano>/matriculas/regiao")
