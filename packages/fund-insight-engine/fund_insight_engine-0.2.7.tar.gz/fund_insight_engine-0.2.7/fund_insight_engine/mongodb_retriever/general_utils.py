from .general_pipelines import create_pipeline_for_latest_date

def get_latest_date_in_collection(collection, key_for_date):
    cursor = collection.aggregate(create_pipeline_for_latest_date(key_for_date))
    latest_date = list(cursor)[-1][key_for_date]
    return latest_date