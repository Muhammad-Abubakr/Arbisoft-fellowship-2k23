from shopping_cart import ShoppingCart
import pytest

def test_can_add_item_to_cart():
    cart = ShoppingCart(1)
    cart.add("apple")
    assert cart.size() == 1

def test_added_item_present_in_cart():
    cart = ShoppingCart(1)
    cart.add("apple")
    assert cart.get_items().pop() == "apple"
    
def test_adding_items_to_full_cart_should_fail():
    max = 1
    cart = ShoppingCart(max)

    for _ in range(max):
        cart.add("apple")

    with pytest.raises(OverflowError):
        cart.add("apple")

def test_can_get_total_price():
    max = 10
    cart = ShoppingCart(max)
    
    cart.add("apple")
    cart.add("orange")
        
    price_map = {"apple": 1.0, "orange": 2.0}
    
    assert cart.get_total_price(price_map) == 3.0