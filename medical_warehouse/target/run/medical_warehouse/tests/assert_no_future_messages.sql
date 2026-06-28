
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select *
from "telegram_db"."analytics"."stg_telegram_messages"
where message_date > now()
  
  
      
    ) dbt_internal_test