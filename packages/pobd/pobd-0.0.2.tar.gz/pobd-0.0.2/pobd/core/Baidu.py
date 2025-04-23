import requests
import base64
import os
from aip import AipOcr

base_dir = os.path.dirname(os.path.abspath(__file__))

class BaiduOCR:
    def __init__(self, app_id=None, api_key=None, secret_key=None):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None


    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_token(self):
        """获取 access_token"""
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.get(url, params=params)
        result = response.json()
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"获取access_token失败：{result}")

    def image_to_base64(self, img_path):
        """将图片转换为 base64 编码"""
        with open(img_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def social_security_card(self, img_path):
        """调用社保卡识别接口"""
        self.access_token = self.get_token()
        base64_image = self.image_to_base64(img_path)
        request_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/social_security_card?access_token={self.access_token}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "image": base64_image
        }
        response = requests.post(request_url, headers=headers, data=data)
        return response.json()

    def divorce_certificate(self, img_path):
        """调用离婚证识别接口"""
        self.access_token = self.get_token()
        base64_image = self.image_to_base64(img_path)
        request_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/divorce_certificate?access_token={self.access_token}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "image": base64_image
        }
        response = requests.post(request_url, headers=headers, data=data)
        return response.json()

    def marriage_certificate(self, img_path):
        """调用结婚证识别接口"""
        self.access_token = self.get_token()
        base64_image = self.image_to_base64(img_path)
        request_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/marriage_certificate?access_token={self.access_token}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "image": base64_image
        }
        response = requests.post(request_url, headers=headers, data=data)
        return response.json()


    def id_card(self, img_path):
        client = AipOcr(self.app_id, self.api_key, self.secret_key)
        image = self.get_file_content(img_path)

        idCardSide = "front"  # 正面

        # 调用身份证识别
        res_image = client.idcard(image, idCardSide)
        return res_image


    def id_card_mix(self, img_path):
        """调用身份证混贴识别接口"""
        self.access_token = self.get_token()
        base64_image = self.image_to_base64(img_path)
        request_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/multi_idcard?access_token={self.access_token}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "image": base64_image
        }
        response = requests.post(request_url, headers=headers, data=data)
        return response.json()


    def bank_card(self, img_path):
        """调用银行卡识别接口"""
        client = AipOcr(self.app_id, self.api_key, self.secret_key)
        image = self.get_file_content(img_path)

        res_image = client.bankcard(image)
        return res_image


if __name__ == '__main__':
    app_id = '118...63'
    api_key = 'B84Lf3...AtSqSxBQ'
    secret_key = '8dY2YhPv....20Cm9oXQjhtTp'
    ocr = BaiduOCR(app_id, api_key, secret_key)

    res = ocr.bank_card(r'D:\PycharmProjects\pobd\tests\test_files\ocr\BankCard\bankcard.jpg')
    print(res)