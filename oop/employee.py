import logging

logger = logging.getLogger('Employee')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('employee.log')
logger.addHandler(handler)


class Employee:
    # Class Variables
    raise_amount = 1.05
    
    # Constructor 
    def __init__(self, first, last, pay) -> None:
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f'{first}.{last}@company.com'

    # Behaviors / Methods
    def fullname(self) -> str:
        return f'{self.first} {self.last}'


class Developer(Employee):
    pass


class Manager(Employee):
    pass



if __name__ == '__main__':
    emp_1 = Employee('ali', 'zafar', 500000)
    emp_2 = Employee('asim', 'azhar', 90000)

    logger.info(emp_1.fullname())
    logger.info(emp_2.fullname())