from mongodb_controller import client
from .menu8186_retriever.menu8186_connector import collection_menu8186 as COLLECTION_MENU8186
from .menu8186_retriever.menu8186_pipelines import create_pipeline_fund_codes_and_fund_names, create_pipeline_fund_codes_and_inception_dates
from .general_utils import get_latest_date_in_collection

def get_latest_date_in_menu8186():
    return get_latest_date_in_collection(COLLECTION_MENU8186, '일자')

def get_mapping_fund_names_mongodb(date_ref=None):
    date_ref = date_ref or get_latest_date_in_menu8186()
    cursor = COLLECTION_MENU8186.aggregate(create_pipeline_fund_codes_and_fund_names(date_ref=date_ref))
    data = list(cursor)
    mapping_codes_and_names = {datum['펀드코드']: datum['펀드명'] for datum in data}
    return mapping_codes_and_names

def get_mapping_fund_inception_dates_mongodb(date_ref=None):
    date_ref = date_ref or get_latest_date_in_menu8186()
    cursor = COLLECTION_MENU8186.aggregate(create_pipeline_fund_codes_and_inception_dates(date_ref=date_ref))
    data = list(cursor)
    mapping_codes_and_dates = {datum['펀드코드']: datum['설정일'] for datum in data}
    return mapping_codes_and_dates
