import sys

from pohw.lib.ocr_processor import do_api


def HouseholdRegister(file_path=None, file_url=None, sk=None, ak=None):
    return do_api(OCR_NAME=str(sys._getframe().f_code.co_name),
                  file_path=file_path,
                  file_url=file_url,
                  sk=sk, ak=ak)


def SmartDocumentRecognizer(file_path=None, file_url=None, sk=None, ak=None):
    return do_api(OCR_NAME=str(sys._getframe().f_code.co_name),
                  file_path=file_path,
                  file_url=file_url,
                  sk=sk, ak=ak)


def BankReceipt(file_path=None, file_url=None, sk=None, ak=None):
    return do_api(OCR_NAME=str(sys._getframe().f_code.co_name),
                  file_path=file_path,
                  file_url=file_url,
                  sk=sk, ak=ak)