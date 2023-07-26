from typing import List

class ShoppingCart:
    def __init__(self, max_size: int) -> None:
        """Initializes an items list of strings and a max_size for it

        Args:
            max_size (int): maximum size, number of items in the list
        """
        self.items: List[str] = list()
        self.max_size = max_size

    def add(self, item: str) -> None:
        """Add item to the ShoppingCart

        Args:
            item (str): item to be added to the shopping cart
        """
        if self.size() >= self.max_size:
            raise OverflowError("The cart has reached it's maximum capacity\
                Cannot add more items.")
        
        self.items.append(item.strip())

    def size(self) -> int:
        """Returns the number of items in the shopping cart

        Returns:
            int: number of items in the shopping cart
        """
        return len(self.items)

    def get_items(self) -> List[str]:
        """Returns a list of actual items in the shopping cart

        Returns:
            List[str]: list of items in the shopping cart
        """
        return self.items

    def get_total_price(self, price_map) -> int:
        """Calculates and returns the total price of the items in the
        cart

        Args:
            price_map (Dict[str:int]): price map, that maps each item
            to it's corresponding price

        Returns:
            int: total price of the items in the shopping cart
        """
        total_price = 0
        
        for item in self.items:
            if item in price_map:
                total_price += price_map.get(item)

        return total_price
