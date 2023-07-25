import logging

def factorial(num):
    if num <= 1:
        return 1
    
    return num * factorial(num-1)

logging.basicConfig(level=logging.DEBUG)
logging.info(factorial(5))
