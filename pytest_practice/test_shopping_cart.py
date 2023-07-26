from shopping_cart import ShoppingCart
from item_database import ItemDatabase
import pytest

@pytest.fixture
def cart() -> ShoppingCart:
    # configuration for ShoppingCart class
    return ShoppingCart(5)

def test_can_add_item_to_cart(cart: ShoppingCart):
    cart.add("apple")
    assert cart.size() == 1

def test_added_item_present_in_cart(cart: ShoppingCart):
    old_size = cart.size()
    cart.add("apple")
    new_size = cart.size()
    assert old_size < new_size
    assert cart.get_items().pop() == "apple"
    
def test_adding_items_to_full_cart_should_fail(cart: ShoppingCart):
    for _ in range(cart.max_size):
        cart.add("apple")

    with pytest.raises(OverflowError):
        cart.add("apple")

def test_can_get_total_price(cart: ShoppingCart): 
    cart.add("apple")
    cart.add("orange")
    
    item_database = ItemDatabase()
    # price_map = {"apple": 1.0, "orange": 2.0}
    
    assert cart.get_total_price(item_database) == 3.0
    
    
# Some important notes
# If want to check if our function raises the exception, if we don't want
# it to do something on some arguments
# 
# ``` python
#   
# with pytest.raises(Exception):
#       Write here the code that should raise 'Exception'
# ```

# If want to run individual test from a file we can do
# $ pytest filename::tset_func_name

# If want to print the print statements written in the test to the console
# $ pytest -s 

# If want to run a single test file
# $ pytest test_file

# === Fixtures ===
# providing baseline for the test functions

# === Mocking ===
# Testing an unimplemented function based on what output it should give
# given a specific input