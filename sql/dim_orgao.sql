create table if not exists dim_orgao (
    id_orgao      serial primary key,
    cd_orgao      text unique,
    ds_orgao      text,
    sigla_orgao   text
);

truncate table dim_orgao;

insert into dim_orgao (cd_orgao, ds_orgao, sigla_orgao)
select distinct
    cd_orgao,
    ds_orgao,
    sigla_orgao
from silver_despesas
where cd_orgao is not null and cd_orgao <> '';
