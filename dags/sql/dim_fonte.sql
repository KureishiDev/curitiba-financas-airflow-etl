create table if not exists dim_fonte (
    id_fonte      serial primary key,
    cd_fonte      text,
    ds_fonte      text,
    chave_natural text unique
);

truncate table dim_fonte;

insert into dim_fonte (cd_fonte, ds_fonte, chave_natural)
select distinct
    cd_fonte,
    ds_fonte,
    coalesce(cd_fonte, '') || '|' || coalesce(ds_fonte, '') as chave_natural
from (
    select
        cd_fonte,
        ds_fonte
    from silver_despesas

    union

    select
        null::text as cd_fonte,
        ds_fonte
    from silver_receitas
) f
where coalesce(cd_fonte, '') <> '' or coalesce(ds_fonte, '') <> '';
