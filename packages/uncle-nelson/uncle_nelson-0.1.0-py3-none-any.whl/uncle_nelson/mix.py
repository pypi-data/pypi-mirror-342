"""
MIT License

Copyright (c) 2025-present codeofandrin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import NamedTuple, List

from .enums import DrugType, EffectType, IngredientType
from .rules import get_ingredient_info, get_effect_info, get_drug_info


# fmt: off
__all__ = (
    "calculate_mix",
)
# fmt: on


class Mix(NamedTuple):
    drug: DrugType
    ingredients: List[IngredientType]
    effects: List[EffectType]
    price: int
    cost: int


def calculate_mix(drug: DrugType, ingredients: List[IngredientType]) -> Mix:
    """



    Parameters
    -----------
    drug: :class:`.DrugType`
        The type of drug to mix.
    ingredients: List[:class:`.IngredientType`]
        A list of ingredients to mix with the drug.

        .. note ::

            The ingredients are mixed one by one, so the order matters.

            .. code-block:: python3

                mix = calculate_mix(..., [IngredientType.cuke, IngredientType.banana])

            will not end in the same result as

            .. code-block:: python3

                mix = calculate_mix(..., [IngredientType.banana, IngredientType.cuke])



    Returns
    -------
    :class:`.Mix`
        The calculated mix.
    """

    total_effects: List[EffectType] = []
    cost = 0

    drug_info = get_drug_info(drug)
    if drug_info.base is not None:
        total_effects.append(drug_info.base)

    for ingredient in ingredients:
        ingredient_info = get_ingredient_info(ingredient)
        base = ingredient_info.base
        interactions = ingredient_info.interactions
        cost += ingredient_info.cost

        for old_effect, new_effect in interactions.items():
            if new_effect in total_effects:
                # if the new effect already in total effects, keep old effect
                continue

            if old_effect in total_effects:
                i = total_effects.index(old_effect)
                total_effects[i] = new_effect

        if base not in total_effects and len(total_effects) < 8:
            total_effects.append(base)

    multiplier = 0
    for effect in total_effects:
        effect_info = get_effect_info(effect)
        multiplier += effect_info.multiplier

    price = round(drug_info.price * (1 + multiplier))

    return Mix(drug=drug, ingredients=ingredients, effects=total_effects, price=price, cost=cost)
