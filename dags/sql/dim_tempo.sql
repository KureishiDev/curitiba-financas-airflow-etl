create table if not exists dim_tempo (
    id_tempo     serial primary key,
    data_calend  date unique,
    ano          integer,
    mes          integer,
    dia          integer
);

truncate table dim_tempo;

insert into dim_tempo (data_calend, ano, mes, dia)
select distinct
    d as data_calend,
    extract(year from d)::integer as ano,
    extract(month from d)::integer as mes,
    extract(day from d)::integer as dia
from (
    select dt_apropriacao as d from silver_receitas
    union
    select dt_empenho as d from silver_despesas
) datas
where d is not null;
