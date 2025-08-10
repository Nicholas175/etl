from prefect import flow, task
from extract import extract_weather_data
from transform import transform_weather_data
from load import load_to_staging_weather

@task
def task_extract():
    df = extract_weather_data(
        lat=51.9,
        lon=8.4,
        start_date="2025-07-01",
        end_date="2025-07-31"
    )
    print(f"Extracted {len(df)} rows")
    return df

@task
def task_transform(df):
    meta_info = {
        "city": "Gütersloh",
        "lat": 51.9,
        "lon": 8.4,
        "source": "open-meteo"
    }
    return transform_weather_data(df, meta_info)

@task
def task_load(df):
    load_to_staging_weather(df)

@flow
def weather_etl_flow():
    raw = task_extract()
    transformed = task_transform(raw)
    task_load(transformed)

if __name__ == "__main__":
    weather_etl_flow()
