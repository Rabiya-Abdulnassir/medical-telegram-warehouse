
  
    

  create  table "telegram_db"."analytics"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    select
    message_id,

    c.channel_id,
    d.date_id,

    message_text,
    length(message_text) as message_length,

    views,
    forwards,
    has_media

from "telegram_db"."analytics"."stg_telegram_messages" s

left join "telegram_db"."analytics"."dim_channels" c
    on s.channel = c.channel_name

left join "telegram_db"."analytics"."dim_dates" d
    on s.message_date::date = d.full_date
  );
  