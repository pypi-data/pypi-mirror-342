import os

from pobd.core.Baidu import BaiduOCR
from pofile import get_files, mkdir
from poprogress import simple_progress
from loguru import logger

base_dir = os.path.dirname(os.path.abspath(__file__))



def extract_ocr_data(img_path, app_id=None, api_key=None, secret_key=None, ocr_func=None):
    """
    通用OCR识别提取方法
    :param img_path: 图片路径
    """
    vat_img_files = get_files(img_path)
    if vat_img_files is None:
        raise BaseException(f'{img_path}这个文件目录下，没有有效的文件，请确认后重新运行')

    baidu_ocr = BaiduOCR(app_id, api_key, secret_key)

    result_df = []
    for img in simple_progress(vat_img_files):
        ocr_result = ocr_func(baidu_ocr, img)
        result_df.append(ocr_result)

    return result_df


def social_security_card(img_path, api_key=None, secret_key=None):
    return extract_ocr_data(img_path=img_path,
                            api_key=api_key,
                            secret_key=secret_key,
                            ocr_func=lambda ocr, img: ocr.social_security_card(img))  # 控制调用百度的接口)

def divorce_certificate(img_path, api_key=None, secret_key=None):
    return extract_ocr_data(img_path=img_path,
                            api_key=api_key,
                            secret_key=secret_key,
                            ocr_func=lambda ocr, img: ocr.divorce_certificate(img))  # 控制调用百度的接口)

def marriage_certificate(img_path, api_key=None, secret_key=None):
    return extract_ocr_data(img_path=img_path,
                            api_key=api_key,
                            secret_key=secret_key,
                            ocr_func=lambda ocr, img: ocr.marriage_certificate(img))  # 控制调用百度的接口)

def id_card(img_path, app_id=None, api_key=None, secret_key=None):
    return extract_ocr_data(img_path=img_path,
                            app_id=app_id,
                            api_key=api_key,
                            secret_key=secret_key,
                            ocr_func=lambda ocr, img: ocr.id_card(img))  # 控制调用百度的接口)

def id_card_mix(img_path, api_key=None, secret_key=None):
    return extract_ocr_data(img_path=img_path,
                            api_key=api_key,
                            secret_key=secret_key,
                            ocr_func=lambda ocr, img: ocr.id_card_mix(img))  # 控制调用百度的接口)

def bank_card(img_path, app_id=None, api_key=None, secret_key=None):
    return extract_ocr_data(img_path=img_path,
                            app_id=app_id,
                            api_key=api_key,
                            secret_key=secret_key,
                            ocr_func=lambda ocr, img: ocr.bank_card(img))  # 控制调用百度的接口)