from enum import Enum
from functools import reduce
from types import MappingProxyType
from typing import Final, Mapping, final


@final
class Category(str, Enum):
    """Possible categories for products."""

    BREAD = "bread"
    MILK = "milk"
    FRUITS_BERRIES = "fruits_berries"
    GRAINS = "grains"
    MEAT = "meat"
    CONFECTIONERY = "confectionery"
    VEGETABLES = "vegetables"
    DRINKS = "drinks"
    OTHER = "other"


@final
class CategoryGroup(str, Enum):
    """Possible groups of categories."""

    FOOD = "food"
    HEALTH_AND_CARE = "health_and_care"
    TRANSPORTATION = "transportation"
    CLOTHING = "clothing"
    HOME = "home"
    RESTAURANTS = "restaurants"
    TELECOMMUNICATIONS = "telecommunications"
    UTILITY_BILLS = "utility_bills"
    STUDYING = "studying"
    OTHER = "other"


CATEGORY_NESTING: Final = MappingProxyType({
    CategoryGroup.FOOD: {
        Category.BREAD,
        Category.MILK,
        Category.FRUITS_BERRIES,
        Category.GRAINS,
        Category.MEAT,
        Category.CONFECTIONERY,
        Category.VEGETABLES,
        Category.DRINKS,
        Category.OTHER,
    },
    CategoryGroup.HEALTH_AND_CARE: set(),
    CategoryGroup.TRANSPORTATION: set(),
    CategoryGroup.CLOTHING: set(),
    CategoryGroup.HOME: set(),
    CategoryGroup.RESTAURANTS: set(),
    CategoryGroup.TELECOMMUNICATIONS: set(),
    CategoryGroup.UTILITY_BILLS: set(),
    CategoryGroup.STUDYING: set(),
    CategoryGroup.OTHER: set(),
})

GROUP_OF: Final[Mapping[Category, CategoryGroup]] = MappingProxyType(
    reduce(
        lambda base, add: base | add,  # type: ignore
        (
            dict.fromkeys(CATEGORY_NESTING[cat_group], cat_group)
            for cat_group in CategoryGroup
        ),
        {}
    )
)
