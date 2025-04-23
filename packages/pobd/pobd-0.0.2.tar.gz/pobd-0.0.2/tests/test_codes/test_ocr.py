import os
import unittest

from pobd.api.ocr import *

base_dir = os.path.dirname(os.path.abspath(__file__))


class Ocr(unittest.TestCase):
    """
    test for ocr.py
    """
    def setUp(self):
        # 百度
        self.app_id = os.getenv("app_id", None)
        self.api_key = os.getenv("api_key", None)
        self.secret_key = os.getenv("secret_key", None)



    # 识别社保卡原始数据
    def test_social_security_card(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr','Social', 'img.png'))
        r = social_security_card(img_path=input_file,
                                 api_key=self.api_key,
                                 secret_key=self.secret_key, )
        logger.info(r)
        # 添加断言
        self.assertIsNotNone(r, "识别结果为空")


    # 识别离婚证原始数据
    def test_divorce_certificate(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Divorce', 'divorce.png'))
        r = divorce_certificate(img_path=input_file,
                                     api_key=self.api_key,
                                     secret_key=self.secret_key, )
        logger.info(r)

        self.assertIsNotNone(r, "识别结果为空")


    # 识别结婚证原始数据
    def test_marriage_certificate(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr','Marriage', 'marriage.png'))
        r = divorce_certificate(img_path=input_file,
                                     api_key=self.api_key,
                                     secret_key=self.secret_key, )
        logger.info(r)

        self.assertIsNotNone(r, "识别结果为空")


    # 识别身份证原始数据
    def test_id_card(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Id_card', 'id_card.jpg'))

        r = id_card(img_path=input_file, app_id=self.app_id, api_key=self.api_key, secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)


    # 识别身份证混贴原始数据
    def test_id_card_mix(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'Id_card_mix', 'id_card_mix.png'))

        r = id_card_mix(img_path=input_file, api_key=self.api_key, secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)


    # 识别银行卡原始数据
    def test_bank_card(self):
        input_file = os.path.abspath(os.path.join(base_dir, '..', '..', 'tests', 'test_files', 'ocr', 'BankCard', 'bankcard.jpg'))

        r = bank_card(img_path=input_file,  app_id=self.app_id, api_key=self.api_key, secret_key=self.secret_key, )
        logger.info(r)

        self.assertTrue(r)