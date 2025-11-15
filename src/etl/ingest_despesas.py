from pathlib import Path
import pandas as pd

from db_config import get_engine

BASE_DIR = Path(__file__).resolve().parents[2]
DESPESAS_DIR = BASE_DIR / "data" / "raw" / "despesas"


def limpar_despesas(df: pd.DataFrame) -> pd.DataFrame:
    # normaliza nomes das colunas
    df.columns = [c.strip().lower() for c in df.columns]

    # remove linhas lixo com ----- se existirem
    mask_lixo = df.apply(
        lambda row: row.astype(str).str.contains("-----").any(),
        axis=1
    )
    df = df[~mask_lixo].copy()

    colunas_validas = [
        "ano_empenho",
        "dt_empenho",
        "empresa",
        "sigla_empresa",
        "cd_orgao",
        "ds_orgao",
        "sigla_orgao",
        "cd_unidade",
        "ds_unidade",
        "sigla_unidade",
        "cd_funcao",
        "ds_funcao",
        "cd_subfuncao",
        "ds_subfuncao",
        "cd_programa",
        "ds_programa",
        "cd_acao",
        "ds_acao",
        "cd_categoria_despesa",
        "ds_categoria_despesa",
        "cd_grupo_despesa",
        "ds_grupo_despesa",
        "cd_modalidade_despesa",
        "ds_modalidade_despesa",
        "cd_elemento_despesa",
        "ds_elemento_despesa",
        "cd_subelemento_despesa",
        "ds_subelemento_despesa",
        "cd_fonte",
        "ds_fonte",
        "fornecedor",
        "cpf_cnpj",
        "nr_empenho",
        "licitacao",
        "orcado_inicial_empenho",
        "orcado_atual_empenho",
        "vl_empenhado",
        "protocolosup",
        "dt_transacao",
        "nr_parcela",
        "transacao",
        "vl_liquidado",
        "vl_pago_devolvido",
        "vl_emp_anulado",
        "vl_pago",
        "vl_consignado"
    ]

    colunas_presentes = [c for c in colunas_validas if c in df.columns]
    df = df[colunas_presentes].copy()

    # datas
    for col in ["dt_empenho", "dt_transacao"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # colunas numéricas com vírgula
    colunas_numericas = [
        "orcado_inicial_empenho",
        "orcado_atual_empenho",
        "vl_empenhado",
        "vl_liquidado",
        "vl_pago_devolvido",
        "vl_emp_anulado",
        "vl_pago",
        "vl_consignado",
    ]

    for col in colunas_numericas:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def ingest_despesas_csv():
    engine = get_engine()

    arquivos = list(DESPESAS_DIR.glob("*.csv"))
    if not arquivos:
        print(f"Nenhum CSV encontrado em {DESPESAS_DIR}")
        return

    print(f"Encontrados {len(arquivos)} arquivos de despesas")

    with engine.begin() as conn:
        for caminho in arquivos:
            print(f"Ingerindo arquivo: {caminho.name}")

            df = pd.read_csv(
                caminho,
                sep=";",
                dtype=str,
                encoding="latin1",
                on_bad_lines="skip"
            )

            df = limpar_despesas(df)

            df.to_sql(
                "stg_despesas",
                con=conn,
                if_exists="append",
                index=False
            )

    print("Ingestão de despesas finalizada com sucesso")


if __name__ == "__main__":
    ingest_despesas_csv()
