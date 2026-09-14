from unittest.mock import Mock
import pytest
from praktikum.burger import Burger
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

class TestBurger:

    def test_set_buns(self):
        burger = Burger()
        bun = Mock()
        burger.set_buns(bun)
        assert burger.bun == bun

    def test_add_ingredient(self):
        burger = Burger()
        ingredient = Mock()
        burger.add_ingredient(ingredient)
        assert burger.ingredients == [ingredient]

    def test_remove_ingredient(self):
        burger = Burger()
        first = Mock()
        second = Mock()
        burger.ingredients = [first, second]
        burger.remove_ingredient(0)
        assert burger.ingredients == [second]

    def test_move_ingredient(self):
        burger = Burger()
        first = Mock()
        second = Mock()
        third = Mock()
        burger.ingredients = [first, second, third]
        burger.move_ingredient(2, 0)
        assert burger.ingredients == [third, first, second]

    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected",
        [
            (100, [], 200),
            (100, [50], 250),
            (200, [100, 300], 800),
        ],
    )
    def test_get_price(self, bun_price, ingredient_prices, expected):
        burger = Burger()
        bun = Mock()
        bun.get_price.return_value = bun_price
        burger.set_buns(bun)

        for price in ingredient_prices:
            ingredient = Mock()
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected

    @pytest.mark.parametrize(
        "ingredient_type, ingredient_name",
        [
            (INGREDIENT_TYPE_SAUCE, "hot sauce"),
            (INGREDIENT_TYPE_FILLING, "cutlet"),
        ],
    )
    def test_get_receipt(self, ingredient_type, ingredient_name):
        burger = Burger()
        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        burger.set_buns(bun)

        ingredient = Mock()
        ingredient.get_type.return_value = ingredient_type
        ingredient.get_name.return_value = ingredient_name
        ingredient.get_price.return_value = 100
        burger.add_ingredient(ingredient)
        receipt = burger.get_receipt()

        assert "(==== black bun ====)" in receipt
        assert f"= {ingredient_type.lower()} {ingredient_name} =" in receipt
        assert "Price: 300" in receipt