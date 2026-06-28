with base as (
    select distinct message_date::date as date_day
    from "telegram_db"."analytics"."stg_telegram_messages"
)

select
    row_number() over () as date_id,
    date_day as full_date,

    extract(day from date_day) as day,
    extract(month from date_day) as month,
    extract(year from date_day) as year,
    extract(week from date_day) as week,

    to_char(date_day, 'Day') as day_name,

    case
        when extract(dow from date_day) in (0,6) then true
        else false
    end as is_weekend

from base