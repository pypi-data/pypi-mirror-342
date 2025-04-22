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

import enum


# fmt: off
__all__ = (
    "DrugType",
    "IngredientType",
    "EffectType"
)
# fmt: on


class DrugType(enum.Enum):
    og_kush = "OG Kush"
    sour_diesel = "Sour Diesel"
    green_crack = "Green Crack"
    granddaddy_purple = "Granddaddy Purple"
    methamphetamine = "Methamphetamine"
    meth = methamphetamine
    cocaine = "Cocaine"


class IngredientType(enum.Enum):
    cuke = "Cuke"
    banana = "Banana"
    paracetamol = "Paracetamol"
    donut = "Donut"
    viagra = "Viagra"
    mouth_wash = "Mouth Wash"
    flu_medicine = "Flu Medicine"
    gasoline = "Gasoline"
    energy_drink = "Energy Drink"
    motor_oil = "Motor Oil"
    mega_bean = "Mega Bean"
    chili = "Chili"
    battery = "Battery"
    iodine = "Iodine"
    addy = "Addy"
    horse_semen = "Horse Semen"


class EffectType(enum.Enum):
    anti_gravity = "Anti-Gravity"
    athletic = "Athletic"
    balding = "Balding"
    bright_eyed = "Bright-Eyed"
    calming = "Calming"
    calorie_dense = "Calorie-Dense"
    cyclopean = "Cyclopean"
    disorienting = "Disorienting"
    electrifying = "Electrifying"
    energizing = "Energizing"
    euphoric = "Euphoric"
    explosive = "Explosive"
    focused = "Focused"
    foggy = "Foggy"
    gingeritis = "Gingeritis"
    glowing = "Glowing"
    jennerising = "Jennerising"
    laxative = "Laxative"
    lethal = "Lethal"
    long_faced = "Long Faced"
    munchies = "Munchies"
    paranoia = "Paranoia"
    refreshing = "Refreshing"
    schizophrenic = "Schizophrenic"
    sedating = "Sedating"
    seizure_inducing = "Seizure-Inducing"
    shrinking = "Shrinking"
    slippery = "Slippery"
    smelly = "Smelly"
    sneaky = "Sneaky"
    spicy = "Spicy"
    thought_provoking = "Thought-Provoking"
    toxic = "Toxic"
    tropic_thunder = "Tropic Thunder"
    zombifying = "Zombifying"
