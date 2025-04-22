from pofile import get_files, mkdir
from pathlib import Path
from poprogress import simple_progress
from pohw.api.ocr import HouseholdRegister, BankReceipt
from loguru import logger

import pandas as pd
import json


def HouseholdRegister2Excel(input_path=None, output_path=None, output_excel='HouseholdRegister2Excel.xlsx',
                            file_url=None, ak=None, sk=None):
    """
    户口本识别
    :param input_path: 户口本存放位置
    :param output_path: 输出文件目录
    :param output_excel: 输出文件名，默认为HouseholdRegister2Excel.xlsx
    :param file_url: 户口本在线文件地址
    :param ak: 华为云账号Access Key
    :param sk: 华为云账号Secret Access Key
    :return:
    """
    if input_path is None and file_url is None:
        raise BaseException(f'参数异常,请检查后重新运行!')
    file_paths = [file_url] if input_path is None else get_files(input_path)
    if file_paths is None or len(file_paths) == 0:
        raise BaseException(f'未识别到有效文件,请检查后重新运行.')
    output_path = output_path or './'
    mkdir(Path(output_path).absolute())  # 如果不存在，则创建输出目录
    if output_excel.endswith('.xlsx') or output_excel.endswith('xls'):  # 如果指定的输出excel结尾不正确，则报错退出
        abs_output_excel = Path(output_path).absolute() / output_excel
    else:
        raise BaseException(
            f'输出结果名：output_excel参数，必须以xls或者xlsx结尾，您的输入:{output_excel}有误，请修改后重新运行')
    res_df = []
    try:
        for item in simple_progress(file_paths):
            api_res = HouseholdRegister(file_path=str(item), file_url=file_url, sk=sk, ak=ak)
            api_res_json = json.loads(str(api_res))
            results = api_res_json.get('result')
            if results is None:
                raise BaseException('调用接口异常！')
            for result in results:
                contents = result.get('content')
                if contents is not None:
                    res_df.append(contents)
    except Exception as e:
        logger.error(e)
    biz_def = pd.DataFrame(res_df)
    # 将结果数据框保存到Excel文件
    biz_def.to_excel(str(abs_output_excel), index=None)


def BankReceipt2excel(input_path=None, output_path=None, output_excel='BankReceipt2excel.xlsx',
                      file_url=None, ak=None, sk=None):
    """
    户口本识别
    :param input_path: 银行回单存放位置
    :param output_path: 输出文件目录
    :param output_excel: 输出文件名，默认为BankReceipt2excel.xlsx
    :param file_url: 银行回单在线文件地址
    :param ak: 华为云账号Access Key
    :param sk: 华为云账号Secret Access Key
    :return:
    """
    if input_path is None and file_url is None:
        raise BaseException(f'参数异常,请检查后重新运行!')
    file_paths = [file_url] if input_path is None else get_files(input_path)
    if file_paths is None or len(file_paths) == 0:
        raise BaseException(f'未识别到有效文件,请检查后重新运行.')
    output_path = output_path or './'
    mkdir(Path(output_path).absolute())  # 如果不存在，则创建输出目录
    if output_excel.endswith('.xlsx') or output_excel.endswith('xls'):  # 如果指定的输出excel结尾不正确，则报错退出
        abs_output_excel = Path(output_path).absolute() / output_excel
    else:
        raise BaseException(
            f'输出结果名：output_excel参数，必须以xls或者xlsx结尾，您的输入:{output_excel}有误，请修改后重新运行')
    res_df = []
    try:
        for item in simple_progress(file_paths):
            api_res = BankReceipt(file_path=str(item), file_url=file_url, sk=sk, ak=ak)
            api_res_json = json.loads(str(api_res))
            results = api_res_json.get('result')
            if results is None:
                raise BaseException('调用接口异常！')

            bank_receipt_list = results.get('bank_receipt_list')
            if bank_receipt_list is None:
                logger.error("无识别到数据!")
            else:
                for list_item in bank_receipt_list:
                    kv_pair_list = list_item.get('kv_pair_list')
                    row_res = {}
                    for item in kv_pair_list:
                        row_res[item['key']] = item['value']
                    res_df.append(row_res)
    except Exception as e:
        logger.error(e)
    biz_def = pd.DataFrame(res_df)
    # 将结果数据框保存到Excel文件
    biz_def.to_excel(str(abs_output_excel), index=None)
