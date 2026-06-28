select *
from "telegram_db"."analytics"."stg_telegram_messages"
where message_date > now()