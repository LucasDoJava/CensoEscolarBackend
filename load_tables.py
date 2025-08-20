import os
import pandas as pd
from sqlalchemy.orm import Session
from Helpers.database import db
from Models.instituicao import tb_instituicao
from Models.uf import tb_uf
from Models.mesorregiao import tb_mesorregiao
from Models.microrregiao import tb_microrregiao
from Models.municipio import tb_municipio
from app import app  

DATA_DIR = r"C:\Users\Lucas\Documents\DadosCensoEscolar"

def safe_int(value, default=0):
    try:
        if pd.isna(value) or value == '':
            return default
        return int(float(value))  
    except (ValueError, TypeError):
        return default

def load_tables():
    with app.app_context():
        session: Session = db.session


        
        ufs = {}
        mesorregioes = {}
        microrregioes = {}
        municipios = {}

        
        for arquivo in os.listdir(DATA_DIR):
            if arquivo.endswith(".csv"):
                caminho = os.path.join(DATA_DIR, arquivo)
                print(f"Coletando dados de referência de {caminho}...")

                df = pd.read_csv(caminho, encoding="latin1", sep=";", low_memory=False)

                for _, row in df.iterrows():
                    try:
                        
                        coduf = row.get('CO_UF', row.get('coduf', 0))
                        uf_sigla = row.get('SG_UF', row.get('uf', ''))
                        uf_nome = row.get('NO_UF', row.get('nomeestado', ''))

                        if coduf and uf_sigla and uf_nome:
                            uf_key = (coduf, uf_sigla, uf_nome)
                            if uf_key not in ufs:
                                ufs[uf_key] = tb_uf(
                                    coduf=int(coduf),
                                    uf=str(uf_sigla),
                                    nomeestado=str(uf_nome)
                                )

                        
                        codmeso = row.get('CO_MESORREGIAO', row.get('codmesorregiao', 0))
                        meso_nome = row.get('NO_MESORREGIAO', row.get('mesorregiao', ''))
                        if codmeso and meso_nome:
                            meso_key = (codmeso, meso_nome)
                            if meso_key not in mesorregioes:
                                mesorregioes[meso_key] = tb_mesorregiao(
                                    codmesorregiao=int(codmeso),
                                    mesorregiao=str(meso_nome)
                                )

                        
                        codmicro = row.get('CO_MICRORREGIAO', row.get('codmicrorregiao', 0))
                        micro_nome = row.get('NO_MICRORREGIAO', row.get('microrregiao', ''))
                        if codmicro and micro_nome:
                            micro_key = (codmicro, micro_nome)
                            if micro_key not in microrregioes:
                                microrregioes[micro_key] = tb_microrregiao(
                                    codmicrorregiao=int(codmicro),
                                    microrregiao=str(micro_nome)
                                )

                        
                        codmunicipio = row.get('CO_MUNICIPIO', row.get('codmunicipio', 0))
                        municipio_nome = row.get('NO_MUNICIPIO', row.get('municipio', ''))
                        if codmunicipio and municipio_nome:
                            municipio_key = (codmunicipio, municipio_nome)
                            if municipio_key not in municipios:
                                municipios[municipio_key] = tb_municipio(
                                    idmunicipio=int(codmunicipio),
                                    nome_municipio=str(municipio_nome)
                                )

                    except Exception as e:
                        print(f"Erro ao processar linha: {e}")
                        continue

        
        print("Inserindo UFs...")
        for uf in ufs.values():
            session.merge(uf)

        print("Inserindo mesorregiões...")
        for meso in mesorregioes.values():
            session.merge(meso)

        print("Inserindo microrregiões...")
        for micro in microrregioes.values():
            session.merge(micro)

        print("Inserindo municípios...")
        for municipio in municipios.values():
            session.merge(municipio)

        session.commit()
        print("Dados de referência inseridos com sucesso!")

        
        for arquivo in os.listdir(DATA_DIR):
            if arquivo.endswith(".csv"):
                caminho = os.path.join(DATA_DIR, arquivo)
                print(f"Carregando instituições de {caminho}...")

                df = pd.read_csv(caminho, encoding="latin1", sep=";", low_memory=False)

                for _, row in df.iterrows():
                    try:
                        inst = tb_instituicao(
                            regiao=str(row.get('NO_REGIAO', row.get('regiao', ''))),
                            codregiao=safe_int(row.get('CO_REGIAO', row.get('codregiao', 0))),
                            uf_nome=str(row.get('SG_UF', row.get('uf', ''))),
                            coduf=safe_int(row.get('CO_UF', row.get('coduf', 0))),
                            municipio_nome=str(row.get('NO_MUNICIPIO', row.get('municipio', ''))),
                            codmunicipio=safe_int(row.get('CO_MUNICIPIO', row.get('codmunicipio', 0))),
                            mesorregiao_nome=str(row.get('NO_MESORREGIAO', row.get('mesorregiao', ''))),
                            codmesorregiao=safe_int(row.get('CO_MESORREGIAO', row.get('codmesorregiao', 0))),
                            microrregiao_nome=str(row.get('NO_MICRORREGIAO', row.get('microrregiao', ''))),
                            codmicrorregiao=safe_int(row.get('CO_MICRORREGIAO', row.get('codmicrorregiao', 0))),
                            entidade=str(row.get('NO_ENTIDADE', row.get('entidade', ''))),
                            codentidade=safe_int(row.get('CO_ENTIDADE', row.get('codentidade', 0))),
                            matriculas_base=safe_int(row.get('QT_MAT_BAS', row.get('matriculas_base', 0))),
                            ano=safe_int(row.get('NU_ANO_CENSO', row.get('ano', 0)))
                        )
                        session.merge(inst)
                    except Exception as e:
                        print(f"Erro ao criar instituição: {e}")
                        continue

                session.commit()
                print(f"Instituições de {arquivo} carregadas com sucesso!")

if __name__ == "__main__":
    load_tables()
