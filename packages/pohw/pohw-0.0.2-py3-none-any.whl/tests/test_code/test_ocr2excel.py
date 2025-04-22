import os
import unittest

from pohw.api.ocr2excel import *


class Ocr2Excel(unittest.TestCase):

    def setUp(self) -> None:
        self.CLOUD_SDK_AK = os.getenv("CLOUD_SDK_AK", None)
        self.CLOUD_SDK_SK = os.getenv("CLOUD_SDK_SK", None)

    def test_HouseholdRegister2Excel(self):
        HouseholdRegister2Excel(input_path='../test_files/HouseholdRegister/img.png',
                                output_path='../test_files/HouseholdRegister',
                                ak=self.CLOUD_SDK_AK,
                                sk=self.CLOUD_SDK_SK)
        self.assertTrue(os.path.exists('../test_files/HouseholdRegister/HouseholdRegister2Excel.xlsx'))
        os.remove('../test_files/HouseholdRegister/HouseholdRegister2Excel.xlsx')
        HouseholdRegister2Excel(
            file_url='https://p8.itc.cn/q_70/images01/20230704/3dcd14733b3640c49aa1bdabc2c0c9fd.jpeg',
            output_path='../test_files/HouseholdRegister',
            ak=self.CLOUD_SDK_AK,
            sk=self.CLOUD_SDK_SK)
        self.assertTrue(os.path.exists('../test_files/HouseholdRegister/HouseholdRegister2Excel.xlsx'))
        os.remove('../test_files/HouseholdRegister/HouseholdRegister2Excel.xlsx')

    def test_BankReceipt2excel(self):
        BankReceipt2excel(input_path='../test_files/BankReceipt/img.png',
                          output_path='../test_files/BankReceipt',
                          ak=self.CLOUD_SDK_AK,
                          sk=self.CLOUD_SDK_SK)
        self.assertTrue(os.path.exists('../test_files/BankReceipt/BankReceipt2excel.xlsx'))
        os.remove('../test_files/BankReceipt/BankReceipt2excel.xlsx')
        BankReceipt2excel(
            file_url='https://mediabluk.cnr.cn/img/cnr/CNRCDP/2023/0915/71eda66458ed6169472706395670338310.jpg?'
                     'auth=0be74649338d3fbae5029003e45d60f6',
            output_path='../test_files/BankReceipt',
            ak=self.CLOUD_SDK_AK,
            sk=self.CLOUD_SDK_SK)
        self.assertTrue(os.path.exists('../test_files/BankReceipt/BankReceipt2excel.xlsx'))
        os.remove('../test_files/BankReceipt/BankReceipt2excel.xlsx')
