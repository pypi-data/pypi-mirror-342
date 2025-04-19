from mongodb_controller import client
from shining_pebbles import get_yesterday

DATABASE_NAME_RPA = 'database-rpa'
COLLECTION_NAME_MENU8186 = 'dataset-menu8186'

def get_pipeline_fund_codes_and_fund_names(date_ref=None):
    date_ref = date_ref or get_yesterday()
    return [
        {'$match': {'일자': date_ref}},
        {'$project': {'_id': 0, '펀드코드': 1, '펀드명': 1}}
    ]

def get_mapping_fund_names_mongodb(date_ref=None):
    date_ref = date_ref or get_yesterday()
    collection = client[DATABASE_NAME_RPA][COLLECTION_NAME_MENU8186]
    cursor = collection.aggregate(get_pipeline_fund_codes_and_fund_names(date_ref=date_ref))
    data = list(cursor)
    mapping_codes_and_names = {datum['펀드코드']: datum['펀드명'] for datum in data}
    return mapping_codes_and_names
