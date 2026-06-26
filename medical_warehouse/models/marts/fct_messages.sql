select
    message_id,

    c.channel_id,
    d.date_id,

    message_text,
    length(message_text) as message_length,

    views,
    forwards,
    has_media

from {{ ref('stg_telegram_messages') }} s

left join {{ ref('dim_channels') }} c
    on s.channel = c.channel_name

left join {{ ref('dim_dates') }} d
    on s.message_date::date = d.full_date