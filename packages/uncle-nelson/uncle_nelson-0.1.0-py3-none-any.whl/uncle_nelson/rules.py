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

from typing import NamedTuple, Dict, Optional

from .enums import IngredientType, EffectType, DrugType


class IngredientInfo(NamedTuple):
    base: EffectType
    interactions: Dict[EffectType, EffectType]
    cost: int


class EffectInfo(NamedTuple):
    multiplier: float


class DrugInfo(NamedTuple):
    base: Optional[EffectType]
    price: int


ingredients = {
    IngredientType.cuke: IngredientInfo(
        base=EffectType.energizing,
        interactions={
            EffectType.euphoric: EffectType.laxative,
            EffectType.foggy: EffectType.cyclopean,
            EffectType.gingeritis: EffectType.thought_provoking,
            EffectType.munchies: EffectType.athletic,
            EffectType.slippery: EffectType.munchies,
            EffectType.sneaky: EffectType.paranoia,
            EffectType.toxic: EffectType.euphoric,
        },
        cost=2,
    ),
    IngredientType.banana: IngredientInfo(
        base=EffectType.gingeritis,
        interactions={
            EffectType.calming: EffectType.sneaky,
            EffectType.cyclopean: EffectType.energizing,
            EffectType.disorienting: EffectType.focused,
            EffectType.energizing: EffectType.thought_provoking,
            EffectType.focused: EffectType.seizure_inducing,
            EffectType.long_faced: EffectType.refreshing,
            EffectType.paranoia: EffectType.jennerising,
            EffectType.smelly: EffectType.anti_gravity,
            EffectType.toxic: EffectType.smelly,
        },
        cost=2,
    ),
    IngredientType.paracetamol: IngredientInfo(
        base=EffectType.sneaky,
        interactions={
            EffectType.calming: EffectType.slippery,
            EffectType.electrifying: EffectType.athletic,
            EffectType.energizing: EffectType.paranoia,
            EffectType.focused: EffectType.gingeritis,
            EffectType.foggy: EffectType.calming,
            EffectType.glowing: EffectType.toxic,
            EffectType.munchies: EffectType.anti_gravity,
            EffectType.paranoia: EffectType.balding,
            EffectType.spicy: EffectType.bright_eyed,
            EffectType.toxic: EffectType.tropic_thunder,
        },
        cost=3,
    ),
    IngredientType.donut: IngredientInfo(
        base=EffectType.calorie_dense,
        interactions={
            EffectType.anti_gravity: EffectType.slippery,
            EffectType.balding: EffectType.sneaky,
            EffectType.calorie_dense: EffectType.explosive,
            EffectType.focused: EffectType.euphoric,
            EffectType.jennerising: EffectType.gingeritis,
            EffectType.munchies: EffectType.calming,
            EffectType.shrinking: EffectType.energizing,
        },
        cost=3,
    ),
    IngredientType.viagra: IngredientInfo(
        base=EffectType.tropic_thunder,
        interactions={
            EffectType.athletic: EffectType.sneaky,
            EffectType.disorienting: EffectType.toxic,
            EffectType.euphoric: EffectType.bright_eyed,
            EffectType.laxative: EffectType.calming,
            EffectType.shrinking: EffectType.gingeritis,
        },
        cost=4,
    ),
    IngredientType.mouth_wash: IngredientInfo(
        base=EffectType.balding,
        interactions={
            EffectType.calming: EffectType.anti_gravity,
            EffectType.calorie_dense: EffectType.sneaky,
            EffectType.explosive: EffectType.sedating,
            EffectType.focused: EffectType.jennerising,
        },
        cost=4,
    ),
    IngredientType.flu_medicine: IngredientInfo(
        base=EffectType.sedating,
        interactions={
            EffectType.athletic: EffectType.munchies,
            EffectType.calming: EffectType.bright_eyed,
            EffectType.cyclopean: EffectType.foggy,
            EffectType.electrifying: EffectType.refreshing,
            EffectType.euphoric: EffectType.toxic,
            EffectType.focused: EffectType.calming,
            EffectType.laxative: EffectType.euphoric,
            EffectType.munchies: EffectType.slippery,
            EffectType.shrinking: EffectType.paranoia,
            EffectType.thought_provoking: EffectType.gingeritis,
        },
        cost=5,
    ),
    IngredientType.gasoline: IngredientInfo(
        base=EffectType.toxic,
        interactions={
            EffectType.disorienting: EffectType.glowing,
            EffectType.electrifying: EffectType.disorienting,
            EffectType.energizing: EffectType.euphoric,
            EffectType.euphoric: EffectType.spicy,
            EffectType.gingeritis: EffectType.smelly,
            EffectType.jennerising: EffectType.sneaky,
            EffectType.laxative: EffectType.foggy,
            EffectType.munchies: EffectType.sedating,
            EffectType.paranoia: EffectType.calming,
            EffectType.shrinking: EffectType.focused,
            EffectType.sneaky: EffectType.tropic_thunder,
        },
        cost=5,
    ),
    IngredientType.energy_drink: IngredientInfo(
        base=EffectType.athletic,
        interactions={
            EffectType.disorienting: EffectType.electrifying,
            EffectType.euphoric: EffectType.energizing,
            EffectType.focused: EffectType.shrinking,
            EffectType.foggy: EffectType.laxative,
            EffectType.glowing: EffectType.disorienting,
            EffectType.schizophrenic: EffectType.balding,
            EffectType.sedating: EffectType.munchies,
            EffectType.spicy: EffectType.euphoric,
            EffectType.tropic_thunder: EffectType.sneaky,
        },
        cost=6,
    ),
    IngredientType.motor_oil: IngredientInfo(
        base=EffectType.slippery,
        interactions={
            EffectType.energizing: EffectType.munchies,
            EffectType.euphoric: EffectType.sedating,
            EffectType.foggy: EffectType.toxic,
            EffectType.munchies: EffectType.schizophrenic,
            EffectType.paranoia: EffectType.anti_gravity,
        },
        cost=6,
    ),
    IngredientType.mega_bean: IngredientInfo(
        base=EffectType.foggy,
        interactions={
            EffectType.athletic: EffectType.laxative,
            EffectType.calming: EffectType.glowing,
            EffectType.energizing: EffectType.cyclopean,
            EffectType.focused: EffectType.disorienting,
            EffectType.jennerising: EffectType.paranoia,
            EffectType.seizure_inducing: EffectType.focused,
            EffectType.shrinking: EffectType.electrifying,
            EffectType.slippery: EffectType.toxic,
            EffectType.sneaky: EffectType.calming,
            EffectType.thought_provoking: EffectType.energizing,
        },
        cost=7,
    ),
    IngredientType.chili: IngredientInfo(
        base=EffectType.spicy,
        interactions={
            EffectType.anti_gravity: EffectType.tropic_thunder,
            EffectType.athletic: EffectType.euphoric,
            EffectType.laxative: EffectType.long_faced,
            EffectType.munchies: EffectType.toxic,
            EffectType.shrinking: EffectType.refreshing,
            EffectType.sneaky: EffectType.bright_eyed,
        },
        cost=7,
    ),
    IngredientType.battery: IngredientInfo(
        base=EffectType.bright_eyed,
        interactions={
            EffectType.cyclopean: EffectType.glowing,
            EffectType.electrifying: EffectType.euphoric,
            EffectType.euphoric: EffectType.zombifying,
            EffectType.laxative: EffectType.calorie_dense,
            EffectType.munchies: EffectType.tropic_thunder,
            EffectType.shrinking: EffectType.munchies,
        },
        cost=8,
    ),
    IngredientType.iodine: IngredientInfo(
        base=EffectType.jennerising,
        interactions={
            EffectType.calming: EffectType.balding,
            EffectType.calorie_dense: EffectType.gingeritis,
            EffectType.euphoric: EffectType.seizure_inducing,
            EffectType.foggy: EffectType.paranoia,
            EffectType.refreshing: EffectType.thought_provoking,
            EffectType.toxic: EffectType.sneaky,
        },
        cost=8,
    ),
    IngredientType.addy: IngredientInfo(
        base=EffectType.thought_provoking,
        interactions={
            EffectType.explosive: EffectType.euphoric,
            EffectType.foggy: EffectType.energizing,
            EffectType.glowing: EffectType.refreshing,
            EffectType.long_faced: EffectType.electrifying,
            EffectType.sedating: EffectType.gingeritis,
        },
        cost=9,
    ),
    IngredientType.horse_semen: IngredientInfo(
        base=EffectType.long_faced,
        interactions={
            EffectType.anti_gravity: EffectType.calming,
            EffectType.gingeritis: EffectType.refreshing,
            EffectType.seizure_inducing: EffectType.energizing,
            EffectType.thought_provoking: EffectType.electrifying,
        },
        cost=9,
    ),
}


effects = {
    EffectType.anti_gravity: EffectInfo(multiplier=0.54),
    EffectType.athletic: EffectInfo(multiplier=0.32),
    EffectType.balding: EffectInfo(multiplier=0.30),
    EffectType.bright_eyed: EffectInfo(multiplier=0.40),
    EffectType.calming: EffectInfo(multiplier=0.10),
    EffectType.calorie_dense: EffectInfo(multiplier=0.28),
    EffectType.cyclopean: EffectInfo(multiplier=0.56),
    EffectType.disorienting: EffectInfo(multiplier=0.0),
    EffectType.electrifying: EffectInfo(multiplier=0.50),
    EffectType.energizing: EffectInfo(multiplier=0.22),
    EffectType.euphoric: EffectInfo(multiplier=0.18),
    EffectType.explosive: EffectInfo(multiplier=0.0),
    EffectType.focused: EffectInfo(multiplier=0.16),
    EffectType.foggy: EffectInfo(multiplier=0.36),
    EffectType.gingeritis: EffectInfo(multiplier=0.20),
    EffectType.glowing: EffectInfo(multiplier=0.48),
    EffectType.jennerising: EffectInfo(multiplier=0.42),
    EffectType.laxative: EffectInfo(multiplier=0.0),
    EffectType.long_faced: EffectInfo(multiplier=0.52),
    EffectType.munchies: EffectInfo(multiplier=0.12),
    EffectType.paranoia: EffectInfo(multiplier=0.0),
    EffectType.refreshing: EffectInfo(multiplier=0.14),
    EffectType.schizophrenic: EffectInfo(multiplier=0.0),
    EffectType.sedating: EffectInfo(multiplier=0.26),
    EffectType.seizure_inducing: EffectInfo(multiplier=0.0),
    EffectType.shrinking: EffectInfo(multiplier=0.60),
    EffectType.slippery: EffectInfo(multiplier=0.34),
    EffectType.smelly: EffectInfo(multiplier=0.0),
    EffectType.sneaky: EffectInfo(multiplier=0.24),
    EffectType.spicy: EffectInfo(multiplier=0.38),
    EffectType.thought_provoking: EffectInfo(multiplier=0.44),
    EffectType.toxic: EffectInfo(multiplier=0.0),
    EffectType.tropic_thunder: EffectInfo(multiplier=0.46),
    EffectType.zombifying: EffectInfo(multiplier=0.58),
}


drugs = {
    DrugType.og_kush: DrugInfo(price=39, base=EffectType.calming),
    DrugType.sour_diesel: DrugInfo(price=40, base=EffectType.refreshing),
    DrugType.green_crack: DrugInfo(price=43, base=EffectType.energizing),
    DrugType.granddaddy_purple: DrugInfo(price=44, base=EffectType.sedating),
    DrugType.methamphetamine: DrugInfo(price=70, base=None),
    DrugType.cocaine: DrugInfo(price=150, base=None),
}


def get_ingredient_info(ingredient: IngredientType) -> IngredientInfo:
    return ingredients[ingredient]


def get_effect_info(effect: EffectType) -> EffectInfo:
    return effects[effect]


def get_drug_info(drug: DrugType) -> DrugInfo:
    return drugs[drug]
