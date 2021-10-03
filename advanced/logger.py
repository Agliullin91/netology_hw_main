import logging


def logger_v1(old_function):

	def new_function(*args, **kwargs):
		logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'mylog.log')
		result = old_function(*args, **kwargs)
		logging.info(f'|function name:{old_function.__name__}| arguments:{args}, {kwargs}| result:{result}|')
		return result

	return new_function


def logger_path(path):
	def logger(old_function):

		def new_function(*args, **kwargs):
			logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = path)
			result = old_function(*args, **kwargs)
			logging.info(f'|function name:{old_function.__name__}| arguments:{args}, {kwargs}| result:{result}|')
			return result

		return new_function
	return logger


@logger_path('C:/netology_hw/advanced/mylog.log')
def my_sum(a, b, c):
	result = a + b + c
	return result


if __name__ == '__main__':
	my_sum(4, 8, 3)
