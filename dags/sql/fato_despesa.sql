create table if not exists fato_despesa (
    id_fato_despesa   serial primary key,
    id_tempo          integer not null,
    id_orgao          integer,
    id_fonte          integer,
    cd_unidade        text,
    cd_funcao         text,
    cd_programa       text,
    cd_acao           text,
    vl_empenhado      numeric(16,2),
    vl_liquidado      numeric(16,2),
    vl_pago           numeric(16,2),
    constraint fk_fato_despesa_tempo
        foreign key (id_tempo) references dim_tempo (id_tempo),
    constraint fk_fato_despesa_orgao
        foreign key (id_orgao) references dim_orgao (id_orgao),
    constraint fk_fato_despesa_fonte
        foreign key (id_fonte) references dim_fonte (id_fonte)
);

truncate table fato_despesa;

insert into fato_despesa (
    id_tempo,
    id_orgao,
    id_fonte,
    cd_unidade,
    cd_funcao,
    cd_programa,
    cd_acao,
    vl_empenhado,
    vl_liquidado,
    vl_pago
)
select
    t.id_tempo,
    o.id_orgao,
    f.id_fonte,
    sd.cd_unidade,
    sd.cd_funcao,
    sd.cd_programa,
    sd.cd_acao,
    sum(sd.vl_empenhado)  as vl_empenhado,
    sum(sd.vl_liquidado)  as vl_liquidado,
    sum(sd.vl_pago)       as vl_pago
from silver_despesas sd
join dim_tempo t
    on t.data_calend = sd.dt_empenho
left join dim_orgao o
    on o.cd_orgao = sd.cd_orgao
left join dim_fonte f
    on f.chave_natural = coalesce(sd.cd_fonte, '') || '|' || coalesce(sd.ds_fonte, '')
group by
    t.id_tempo,
    o.id_orgao,
    f.id_fonte,
    sd.cd_unidade,
    sd.cd_funcao,
    sd.cd_programa,
    sd.cd_acao;
