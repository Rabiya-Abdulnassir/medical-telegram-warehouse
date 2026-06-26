
  create view "telegram_db"."analytics"."stg_telegram_messages__dbt_tmp"
    
    
  as (
    SELECT
    message_id,
    channel,
    message_date,
    message_text,
    views,
    forwards,
    has_media,
    LENGTH(message_text) AS message_length
FROM raw.telegram_messages
WHERE message_text IS NOT NULL
  );