import os
import unittest

from pobd.api.ocr2excel import *

base_dir = os.path.dirname(os.path.abspath(__file__))


class Ocr2Excel(unittest.TestCase):
    """
    test for ocr2excel.py
    """

    def setUp(self):
        # 百度
        self.app_id = os.getenv("app_id", None)
        self.api_key = os.getenv("api_key", None)
        self.secret_key = os.getenv("secret_key", None)


    # 单个识别社保卡
    def test_social_security_card(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Social','img.png'))
        output_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Social'))

        # 单个识别社保卡
        r = social_security_card(img_path=input_file,
                                 output_path=output_file,
                                 api_key=self.api_key,
                                 secret_key=self.secret_key, )
        logger.info(r)

        # 添加断言
        self.assertTrue(r)



    # 识别离婚证
    def test_divorce_certificate(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Divorce', 'divorce.png'))
        output_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Divorce', 'divorce_certificate.xlsx'))

        r = divorce_certificate(img_path=input_file,
                                output_excel_path=output_file,
                                api_key=self.api_key,
                                secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)



    # 识别结婚证
    def test_marriage_certificate(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr','Marriage', 'marriage.png'))
        output_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Marriage','marriage_certificate.xlsx'))

        r = divorce_certificate(img_path=input_file,
                                output_excel_path=output_file,
                                api_key=self.api_key,
                                secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)



    # (批量)识别身份证
    def test_id_card(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Id_card'))  # , 'id_card.jpg'
        output_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Id_card', 'id_card.xlsx'))

        r = id_card(img_path=input_file, output_excel_path=output_file,
                                         app_id=self.app_id,
                                         api_key=self.api_key,
                                         secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)



    # 识别身份证混贴
    def test_id_card_mix(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Id_card_mix', 'id_card_mix.png'))
        output_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Id_card_mix', 'id_card_mix.xlsx'))

        r = id_card_mix(img_path=input_file, output_excel_path=output_file,
                                         api_key=self.api_key,
                                         secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)

    # 识别银行卡
    def test_bank_card(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'BankCard', 'bankcard.jpg'))
        output_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'BankCard', 'bankcard.xlsx'))

        r = bank_card(img_path=input_file, output_excel_path=output_file,
                                         app_id=self.app_id,
                                         api_key=self.api_key,
                                         secret_key=self.secret_key, )

        self.assertTrue(r)
