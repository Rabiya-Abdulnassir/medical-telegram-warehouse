from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import get_db

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API for Telegram Medical Data Warehouse",
    version="1.0"
)


# ============================================================
# HOME
# ============================================================
@app.get("/")
def home():
    return {
        "message": "Medical Telegram Warehouse API",
        "documentation": "/docs"
    }


# ============================================================
# Endpoint 1
# Top Products
# GET /api/reports/top-products?limit=10
# ============================================================
@app.get("/api/reports/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)):

    query = text("""
        SELECT
            lower(word) AS product,
            COUNT(*) AS mentions
        FROM (
            SELECT regexp_split_to_table(message_text,'\\s+') AS word
            FROM analytics.fct_messages
        ) words
        WHERE length(word) > 3
        GROUP BY word
        ORDER BY mentions DESC
        LIMIT :limit
    """)

    result = db.execute(query, {"limit": limit})

    return [dict(row._mapping) for row in result]


# ============================================================
# Endpoint 2
# Channel Activity
# GET /api/channels/{channel_name}/activity
# ============================================================
@app.get("/api/channels/{channel_name}/activity")
def channel_activity(channel_name: str,
                     db: Session = Depends(get_db)):

    query = text("""
        SELECT
            c.channel_name,
            COUNT(*) AS total_posts,
            AVG(f.view_count) AS average_views,
            SUM(f.forward_count) AS total_forwards,
            MIN(d.full_date) AS first_post,
            MAX(d.full_date) AS last_post
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c
            ON f.channel_id = c.channel_id
        JOIN analytics.dim_dates d
            ON f.date_id = d.date_id
        WHERE LOWER(c.channel_name)=LOWER(:channel)
        GROUP BY c.channel_name
    """)

    result = db.execute(query, {"channel": channel_name}).fetchone()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Channel not found."
        )

    return dict(result._mapping)


# ============================================================
# Endpoint 3
# Search Messages
# GET /api/search/messages?query=paracetamol&limit=20
# ============================================================
@app.get("/api/search/messages")
def search_messages(query: str,
                    limit: int = 20,
                    db: Session = Depends(get_db)):

    sql = text("""
        SELECT
            message_id,
            channel_name,
            full_date,
            message_text,
            view_count
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c
            ON f.channel_id = c.channel_id
        JOIN analytics.dim_dates d
            ON f.date_id = d.date_id
        WHERE LOWER(message_text)
              LIKE LOWER(:keyword)
        ORDER BY full_date DESC
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "keyword": f"%{query}%",
            "limit": limit
        }
    )

    return [dict(row._mapping) for row in result]


# ============================================================
# Endpoint 4
# Visual Content Report
# GET /api/reports/visual-content
# ============================================================
@app.get("/api/reports/visual-content")
def visual_content(db: Session = Depends(get_db)):

    query = text("""
        SELECT
            c.channel_name,
            COUNT(*) AS total_posts,
            SUM(
                CASE
                    WHEN has_image THEN 1
                    ELSE 0
                END
            ) AS image_posts,
            ROUND(
                AVG(
                    CASE
                        WHEN has_image THEN 1
                        ELSE 0
                    END
                ) * 100,
                2
            ) AS image_percentage
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c
            ON f.channel_id=c.channel_id
        GROUP BY c.channel_name
        ORDER BY image_posts DESC
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]