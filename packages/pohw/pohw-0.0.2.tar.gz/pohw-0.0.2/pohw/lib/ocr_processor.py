# -*- coding: UTF-8 -*-
from pohw.core.OCR import OCR
from pohw.lib.enums.FileTypeEnum import FileTypeEnum
from pohw.lib.CommonUtils import get_file_type, img2base64


def get_ocr(ak, sk):
    """
    初始化OCR对象
    Args:
        ak: Access Key Id
        sk: Secret Access Key

    Returns: OCR对象

    """
    ocr = OCR()
    ocr.set_config(ak, sk)
    return ocr


def do_api(OCR_NAME, file_path, file_url, ak, sk):
    """
    通用api处理
    Args:
        OCR_NAME: OCR_NAME
        file_path: 本地文件路径
        file_url: 线上文件url
        ak: Access Key Id
        sk: Secret Access Key

    Returns: 最终获取结果数据

    """
    ocr = get_ocr(ak, sk)
    if not hasattr(ocr, OCR_NAME):
        raise BaseException('该功能未实现!')
    method = getattr(ocr, OCR_NAME)
    if file_url:
        return method(None, file_url)

    if file_path:
        img_type = get_file_type(file_path)
        if img_type == FileTypeEnum.OTHER:
            raise Exception("文件类型不符合!")
    if img_type == FileTypeEnum.PDF:
        raise Exception("该类型不支持!")
    else:
        ImageBase64 = img2base64(file_path)
        return method(ImageBase64, None)
