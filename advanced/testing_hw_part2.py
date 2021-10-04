from yandex_disc_for_test import get_files_list, create_folder, get_file_meta
import unittest


class TestHomework(unittest.TestCase):

	def test_get_files_list(self):
		result = get_files_list()
		self.assertEqual(200, result[1])

# Папка либо успешно создана (код 200) либо уже существует (код ошибки 409)
	def test_create_folder3(self):
		self.assertTrue(409 == create_folder("test_folder") or 200 == create_folder("test_folder"))

	def test_create_folder2(self):
		create_folder("test_folder")
		result = get_file_meta("test_folder")
		self.assertEqual(200, result[1])

	def test_get_file_meta(self):
		result = get_file_meta("Море.jpg")
		self.assertEqual(200, result[1])



