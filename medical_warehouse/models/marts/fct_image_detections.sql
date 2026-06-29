select
    y.message_id,

    m.channel_id,
    m.date_id,

    y.detected_class,
    y.confidence_score,
    y.image_category

from {{ ref('stg_image_detections') }} y

left join {{ ref('fct_messages') }} m
    on y.message_id = m.message_id