create table if not exists fato_receita (
    id_fato_receita  serial primary key,
    id_tempo         integer not null,
    id_fonte         integer,
    cd_empresa       text,
    nm_empresa       text,
    tp_receita_orc   text,
    vl_receita_total numeric(16,2),
    constraint fk_fato_receita_tempo
        foreign key (id_tempo) references dim_tempo (id_tempo),
    constraint fk_fato_receita_fonte
        foreign key (id_fonte) references dim_fonte (id_fonte)
);

truncate table fato_receita;

insert into fato_receita (
    id_tempo,
    id_fonte,
    cd_empresa,
    nm_empresa,
    tp_receita_orc,
    vl_receita_total
)
select
    t.id_tempo,
    f.id_fonte,
    sr.cd_empresa,
    sr.nm_empresa,
    sr.tp_receita_orc,
    sum(sr.vl_receita) as vl_receita_total
from silver_receitas sr
join dim_tempo t
    on t.data_calend = sr.dt_apropriacao
left join dim_fonte f
    on f.chave_natural = coalesce(null, '') || '|' || coalesce(sr.ds_fonte, '')
group by
    t.id_tempo,
    f.id_fonte,
    sr.cd_empresa,
    sr.nm_empresa,
    sr.tp_receita_orc;
