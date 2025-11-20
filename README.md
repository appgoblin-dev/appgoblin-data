# Free Mobile App Store Data Dumps from AppGoblin

Free Data Dumps from [AppGoblin](https://appgoblin.info). AppGoblin is a resource for free android and ios app intelligence. AppGoblin has the biggest free dashboard to browse mobile apps and the SDKs they use for advertising, product analytics and other open source libraries. AppGoblin also has live advertising information for which apps are currently advertising.

## Data files

Due to 100mb limits, files are compressed and do not contain 'all' the data. If you don't see data you're looking for, feel free to ask.

- `live_store_apps.tsv.xz`: Apps that are currently live on the Google Play and Apple App Store. This TSV includes names and categories.
- `store_apps.tsv.xz`: All Appgoblin's known 4m+ Android and iOS app store ids. Many of which are no longer live on the app stores.
- `store_apps_metrics.tsv.xz`: All live apps with metrics such as installs, rating, review count from AppGoblin.

## Column Descriptions

### Basic App Info

- `store`: The app store (e.g., "google" for Google Play Store)
- `store_id`: Unique identifier/package name for the app
- `app_name`: Display name of the app
- `app_category`: Category of the app (e.g., tools, video_players)

### Developer Info

- `developer_id`: Unique identifier for the developer
- `developer_name`: Name of the developer/company

### Metrics

- `review_count`: Number of written reviews
- `rating_count`: Total number of ratings
- `installs`: Number of installations

### App Properties

- `free`: Boolean indicating if the app is free
- `price`: Price of the app (0 for free apps)
- `minimum_android`: Required Android version
- `ad_supported`: Boolean indicating if app contains ads
- `in_app_purchases`: Boolean indicating if app has IAPs
- `editors_choice`: Boolean indicating if selected as editor's choice

### Timestamps

- `store_last_updated`: When the app was last updated in the store
- `release_date`: Initial release date
- `appgoblin_created_at`: When the app was first added to AppGoblin
- `appgoblin_updated_at`: When the app was last updated in AppGoblin
- `last_crawl_result`: Status of the most recent data crawl

## Companies data

### Column Descriptions

- `store_id`: Unique identifier/package name for the app
- `app_category`: Category of the app (e.g., game_action, tools)
- `company_domain`: Primary web domain of the company
- `company_name`: Name of the company
- `parent_company_name`: Parent company or holding company name
- `tag_source`: Source of the company data (app_ads_direct, app_ads_reseller, or sdk)

The data comes from three tag_sources:

- app_ads_direct: Direct advertising relationships
- app_ads_reseller: Indirect advertising through resellers
- sdk: Software Development Kits integrated in the app

| store_id        | app_category | company_domain | company_name | parent_company_name | tag_source       |
| --------------- | ------------ | -------------- | ------------ | ------------------- | ---------------- |
| com.example.app | game_action  | yandex.com     | Yandex       | Yandex              | app_ads_direct   |
| com.example.app | game_action  | yandex.com     | Yandex       | Yandex              | app_ads_reseller |
| com.example.app | game_action  | ironsrc.com    | ironSource   | Unity Ads           | app_ads_direct   |
| com.example.app | game_action  | yahoo.com      | Yahoo!       | Yahoo!              | app_ads_direct   |
| com.example.app | game_action  | yahoo.com      | Yahoo!       | Yahoo!              | app_ads_reseller |
| com.example.app | game_action  | verve.com      | Verve Group  | Verve Group         | app_ads_reseller |
