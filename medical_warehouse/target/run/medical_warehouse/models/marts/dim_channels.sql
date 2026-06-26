
  
    

  create  table "telegram_db"."analytics"."dim_channels__dbt_tmp"
  
  
    as
  
  (
    with base as (
    select distinct channel
    from "telegram_db"."analytics"."stg_telegram_messages"
)

select
    row_number() over () as channel_id,
    channel as channel_name,

    case
        when channel ilike '%chemed%' then 'Medical'
        when channel ilike '%lobelia%' then 'Cosmetics'
        when channel ilike '%tikvah%' then 'Pharmaceutical'
        else 'Other'
    end as channel_type

from base
  );
  