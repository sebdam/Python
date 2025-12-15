import unittest
from number_translator_functions import *

from enums import NumberFormat

class TestsNumberTranslator(unittest.TestCase):
    def test_translate_hexToDec(self):
        self.assertEqual(translate("0x0", "d"), "0", "0x0 must be translate to 0")
        self.assertEqual(translate("0x9", "d"), "9", "0x9 must be translate to 9")
        self.assertEqual(translate("0xF", "d"), "15", "0xF must be translate to 15")
        self.assertEqual(translate("0x10", "d"), "16", "0x10 must be translate to 16")
        with self.assertRaises(Exception):
            translate("0xG", "d")
        with self.assertRaises(Exception):
            translate("0xg", "d")

    def test_translate_binToDec(self):
        self.assertEqual(translate("0b0", "d"), "0", "0b0 must be translate to 0")
        self.assertEqual(translate("0b1", "d"), "1", "0b1 must be translate to 1")
        self.assertEqual(translate("0b10", "d"), "2", "0b10 must be translate to 2")
        self.assertEqual(translate("0b11", "d"), "3", "0b11 must be translate to 3")
        self.assertEqual(translate("0b100", "d"), "4", "0b100 must be translate to 4")
        with self.assertRaises(Exception):
            translate("0b2", "d")
        with self.assertRaises(Exception):
            translate("0ba", "d")

    def test_translate_ternaireToDec(self):
        self.assertEqual(translate("0t0", "d"), "0", "0t0 must be translate to 0")
        self.assertEqual(translate("0t2", "d"), "2", "0t2 must be translate to 2")
        self.assertEqual(translate("0t10", "d"), "3", "0t10 must be translate to 3")
        self.assertEqual(translate("t12", "d"), "5", "t12 must be translate to 5")
        with self.assertRaises(Exception):
            translate("0t3", "d")
        with self.assertRaises(Exception):
            translate("t3", "d")

    def test_translate_octToDec(self):
        self.assertEqual(translate("0o0", "d"), "0", "0o0 must be translate to 0")
        self.assertEqual(translate("0o1", "d"), "1", "0o1 must be translate to 1")
        self.assertEqual(translate("0o7", "d"), "7", "0o7 must be translate to 7")
        self.assertEqual(translate("0o10", "d"), "8", "0o10 must be translate to 8")
        self.assertEqual(translate("0o17", "d"), "15", "0o17 must be translate to 15")
        self.assertEqual(translate("0o20", "d"), "16", "0o20 must be translate to 16")
        with self.assertRaises(Exception):
            translate("0oa", "d")
        with self.assertRaises(Exception):
            translate("0o8", "d")

    def test_translate_decToDec(self):
        self.assertEqual(translate("0d0", "d"), "0", "0d0 must be translate to 0")
        self.assertEqual(translate("1", "d"), "1", "1 must be translate to 1")
        self.assertEqual(translate("0D7", "d"), "7", "0D7 must be translate to 7")
        self.assertEqual(translate("10", "d"), "10", "10 must be translate to 10")
        with self.assertRaises(Exception):
            translate("0da", "d")
        with self.assertRaises(Exception):
            translate("A", "d")

    def test_convert_over_than_base10_to_dec(self):
        self.assertEqual(convert_over_than_base10_to_dec('A'),'10',"A must be translate to 10")
        self.assertEqual(convert_over_than_base10_to_dec('B'),'11',"B must be translate to 11")
        self.assertEqual(convert_over_than_base10_to_dec('C'),'12',"C must be translate to 12")
        self.assertEqual(convert_over_than_base10_to_dec('D'),'13',"D must be translate to 13")
        self.assertEqual(convert_over_than_base10_to_dec('E'),'14',"E must be translate to 14")
        self.assertEqual(convert_over_than_base10_to_dec('F'),'15',"F must be translate to 15")
        self.assertEqual(convert_over_than_base10_to_dec('G'),'16',"G must be translate to 16")
        self.assertEqual(convert_over_than_base10_to_dec('H'),'17',"H must be translate to 17")

    def test_read_number(self):
        self.assertEqual(read_number('123456'),'123456','123456 must be read 123456')
        self.assertEqual(read_number('D123456'),'123456','D123456 must be read 123456')
        self.assertEqual(read_number('d123456'),'123456','d123456 must be read 123456')
        self.assertEqual(read_number('0x123456'),'123456','0x123456 must be read 123456')
        self.assertEqual(read_number('0X123456'),'123456','0X123456 must be read 123456')

    def test_read_number_format(self):
        self.assertEqual(read_number_format('b'),NumberFormat.binaire,' muste compute NumberFormat.binaire')
        self.assertEqual(read_number_format('B'),NumberFormat.binaire,' muste compute NumberFormat.binaire')
        self.assertEqual(read_number_format('0b'),NumberFormat.binaire,' muste compute NumberFormat.binaire')
        self.assertEqual(read_number_format('t'),NumberFormat.ternaire,' muste compute NumberFormat.ternaire')
        self.assertEqual(read_number_format('T'),NumberFormat.ternaire,' muste compute NumberFormat.ternaire')
        self.assertEqual(read_number_format('0t'),NumberFormat.ternaire,' muste compute NumberFormat.ternaire')
        self.assertEqual(read_number_format('q'),NumberFormat.base4,' muste compute NumberFormat.base4')
        self.assertEqual(read_number_format('Q'),NumberFormat.base4,' muste compute NumberFormat.base4')
        self.assertEqual(read_number_format('0q'),NumberFormat.base4,' muste compute NumberFormat.base4')

    def test_valide_nombre(self):
        with self.assertRaises(Exception):
            valide_nombre("-1", 10)
        with self.assertRaises(Exception):
            valide_nombre("10", 10)
        with self.assertRaises(Exception):
            valide_nombre("9", 9)
        with self.assertRaises(Exception):
            valide_nombre("3", 3)
