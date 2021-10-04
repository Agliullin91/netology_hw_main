from bookshelf_app import documents, directories, get_doc_num_list, people, shelf, add, delete, add_shelf
import unittest
from unittest.mock import patch


class TestHomework(unittest.TestCase):

	def test_get_doc_num_list(self):
		doc_num_list = []
		for item in documents:
			doc_num_list.append(item['number'])
		self.assertEqual(get_doc_num_list(), doc_num_list)

	@patch('builtins.input', lambda *args: '11-2')
	def test_people(self):
		self.assertEqual(people(), 'Геннадий Покемонов')

	@patch('builtins.input', lambda *args: '11-2')
	def test_shelf(self):
		self.assertIn('1', shelf())

	@patch('builtins.input', side_effect=['999-547', 'passport', 'Gennadiy Golovkin', '3'])
	def test_add(self, mock_input):
		result = add()
		self.assertTrue('3' in result)

	@patch('builtins.input', side_effect=['10006'])
	def test_delete(self, mock_input):
		result = delete()
		self.assertTrue('10006' in result)

	@patch('builtins.input', lambda *args: '4')
	def test_add_shelf(self):
		self.assertIn('4', add_shelf().keys())

	@patch('builtins.input', lambda *args: '4')
	def test_add_shelf2(self):
		add_shelf()
		self.assertTrue('4' in directories.keys())