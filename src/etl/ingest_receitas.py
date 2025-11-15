from pathlib import Path
import pandas as pd

from db_config import get_engine


BASE_DIR = Path(__file__).resolve().parents[2]
RECEITAS_DIR = BASE_DIR / "data" / "raw" / "receitas"


def limpar_receitas(df: pd.DataFrame) -> pd.DataFrame:
    # normaliza nomes das colunas
    df.columns = [c.strip().lower() for c in df.columns]

    # remove linhas lixo com traços, se existirem
    mask_lixo = df.apply(
        lambda row: row.astype(str).str.contains("-----").any(),
        axis=1
    )
    df = df[~mask_lixo].copy()

    colunas_validas = [
        "cd_receita",
        "cd_categoria",
        "descricao_categoria",
        "cd_origem",
        "descricao_origem",
        "cd_especie",
        "descricao_especie",
        "cd_rubrica",
        "descricao_rubrica",
        "cd_alinea",
        "descricao_alinea",
        "cd_subalinea",
        "descricao_subalinea",
        "cd_exercicio",
        "dt_apropriacao",
        "tp_receita_orc",
        "cd_empresa",
        "nm_empresa",
        "vl_receita",
        "ds_fonte",
    ]

    # mantém só as colunas que existem no CSV e na tabela
    colunas_presentes = [c for c in colunas_validas if c in df.columns]
    df = df[colunas_presentes].copy()

    # datas
    if "dt_apropriacao" in df.columns:
        df["dt_apropriacao"] = pd.to_datetime(
            df["dt_apropriacao"],
            dayfirst=True,
            errors="coerce",
        )

    # valores numéricos (tira ponto de milhar, troca vírgula por ponto)
    if "vl_receita" in df.columns:
        df["vl_receita"] = (
            df["vl_receita"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        df["vl_receita"] = pd.to_numeric(df["vl_receita"], errors="coerce")

    return df


def ingest_receitas_csv():
    engine = get_engine()

    arquivos = list(RECEITAS_DIR.glob("*.csv"))
    if not arquivos:
        print(f"Nenhum CSV encontrado em {RECEITAS_DIR}")
        return

    print(f"Encontrados {len(arquivos)} arquivos de receitas")

    with engine.begin() as conn:
        for caminho in arquivos:
            print(f"Ingerindo arquivo: {caminho.name}")
            df = pd.read_csv(
            caminho,
            sep=";",
            dtype=str,
            encoding="latin1",   # importante por causa dos acentos
            on_bad_lines="skip"  # se tiver alguma linha muito zoada, ele pula
)

            df = limpar_receitas(df)

            df.to_sql(
                "stg_receitas",
                con=conn,
                if_exists="append",
                index=False,
            )

    print("Ingestão de receitas finalizada com sucesso")


if __name__ == "__main__":
    ingest_receitas_csv()
