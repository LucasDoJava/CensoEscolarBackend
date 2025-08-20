from helpers.app import app, api
from helpers.CORS import cors

from resources.InstituicaoResouce import InstituicoesResouce, NovaInstituicaoResouce, InstituicaoResouce

from resources.UfResource import UfsResouce, UfResource
from resources.MesorregiaoResource import MesorregioesResouce, MesorregiaoResource
from resources.MicrorregiaoResouce import MicrorregioesResouce, MicrorregiaoResource
from resources.MunicipioResource import MunicipiosResouce, MunicipioResource

cors.init_app(app)

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