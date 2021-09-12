from accounting.application.db.people import get_employees
from accounting.application.salary import calculate_salary
import datetime

if __name__ == '__main__':
    get_employees('Harry Potter')
    print()
    calculate_salary('Harry Potter', 1000)
    print(datetime.date.today())