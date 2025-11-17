SELECT
    s.name AS store,
    sa.store_id AS store_id,
    sa.category AS app_category,
    agml.installs AS installs,
    agml.rating_count AS rating_count
FROM
    store_apps sa
LEFT JOIN stores s ON sa.store = s.id
LEFT JOIN app_global_metrics_latest agml ON sa.id = agml.store_app
WHERE 
-- store app names are null when recently added and not yet crawled
sa.name IS NOT NULL
AND sa.crawl_result = 1
;
