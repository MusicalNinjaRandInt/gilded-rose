#! /usr/bin/env python


from collections import OrderedDict


class Item:
    def __init__(self, name, sell_in, quality):  # noqa: ANN001, ANN204
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):  # noqa: ANN204
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)  # noqa: UP031


def qnotnegative(s: int, q: int) -> tuple[int, int]:
    return (s, max(q, 0))


def maxq(s: int, q: int) -> tuple[int, int]:
    return (s, min(q, GildedRose.MAX_QUALITY))


def decrement_s(s: int, q: int) -> tuple[int, int]:
    return (s - 1, q)


def calculate_backstagepass(s: int, q: int) -> tuple[int, int]:
    s, q = decrement_s(s, q)  # Update sell_in first, so we know how old it is now
    rules = OrderedDict(
        {
            10: 1,
            5: 2,
            -1: 3,
            None: None,  # fixed at zero quality
        },
    )
    return generic_calculator(s, q, rules)


def calculate_conjured(s: int, q: int) -> tuple[int, int]:
    s, q = decrement_s(s, q)
    rules = OrderedDict(
        {
            0: -2,
            None: -4,
        },
    )
    return generic_calculator(s, q, rules)


def calculate_brie(s: int, q: int) -> tuple[int, int]:
    s, q = decrement_s(s, q)
    rules = OrderedDict(
        {
            0: 1,
            None: 2,
        },
    )
    return generic_calculator(s, q, rules)


def default_calculator(s: int, q: int) -> tuple[int, int]:
    s, q = decrement_s(s, q)
    rules = OrderedDict(
        {
            0: -1,
            None: -2,
        },
    )
    return generic_calculator(s, q, rules)


def generic_calculator(s: int, q: int, rules: OrderedDict[int, int]) -> tuple[int, int]:
    for s_threshold, q_increment in rules.items():
        if s_threshold is None or s > s_threshold:
            try:
                q += q_increment
            except TypeError:  # q_increment is None
                q = 0
            return (s, q)
    missing_default = "No match found in {rules}, try adding a None entry at the end"
    raise ValueError(missing_default)


class GildedRose:
    MAX_QUALITY = 50

    def __init__(self, items: Item):
        self.items = items

    def update_quality(self) -> None:
        specific_calculators = {
            "Conjured": calculate_conjured,
            "Sulfuras": lambda s, q: (s, q),
            "Aged Brie": calculate_brie,
            "Backstage pass": calculate_backstagepass,
        }

        for item in self.items:
            for itemtype, calculator in specific_calculators.items():
                if item.name.startswith(itemtype):
                    item.sell_in, item.quality = calculator(item.sell_in, item.quality)
                    break
            else:
                item.sell_in, item.quality = default_calculator(item.sell_in, item.quality)

            item.sell_in, item.quality = qnotnegative(item.sell_in, item.quality)
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in, item.quality = maxq(item.sell_in, item.quality)

    def __eq__(self, _other: object) -> bool:
        try:
            equal = [
                all(
                    [
                        myitem.name == otheritem.name,
                        myitem.sell_in == otheritem.sell_in,
                        myitem.quality == otheritem.quality,
                    ],
                )
                for myitem, otheritem in zip(self.items, _other.items)
            ]
        except AttributeError:
            return False
        return all(equal)


if __name__ == "__main__":
    print("OMGHAI!")
    app = GildedRose(
        items=[
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            Item(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(
                name="Backstage passes to a TAFKAL80ETC concert",
                sell_in=15,
                quality=20,
            ),
            Item(name="Conjured Mana Cake", sell_in=3, quality=6),
        ],
    )

    app.update_quality()
    input()
