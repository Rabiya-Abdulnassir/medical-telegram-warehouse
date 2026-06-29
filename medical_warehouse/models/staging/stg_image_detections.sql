select
    cast(message_id as bigint) as message_id,
    channel,
    detected_class,
    cast(confidence_score as numeric) as confidence_score,
    image_category

from {{ source('raw', 'image_detections') }}