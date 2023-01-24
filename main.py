import httpx
import traceback
from math import floor


def get_flip_items():
    req = httpx.get("https://api.rbxflip.com/roblox/shop")
    assert req.status_code == 200
    return req.json()


def get_valued_items():
    # [item_name, acronym, rap, value, default_value, demand, trend, projected, hyped, rare]
    # grabs itemdetails from rolimons and filters out non-valued items, projected, and non-stable items
    req = httpx.get("https://www.rolimons.com/itemapi/itemdetails")
    assert req.status_code in (200, 304)
    data = req.json()["items"]
    return [
        int(item[0])
        for item in data.items()
        if (item[1][3] != -1 and item[1][8] == -1 and item[1][6] == 2)
    ]  # valued, not projected, stable


def get_target():
    while True:
        try:
            target = int(input("Please input the target robux amount A/T: "))
        except TypeError:
            print("That is not a valid number. Please enter an integer.")
            continue
        return at_to_bt(target)


def at_to_bt(after_tax: int):
    return floor(after_tax / 0.7)


def bt_to_at(before_tax: int):
    return floor(before_tax * 0.7)


def main():

    while True:
        target = get_target()
        flip_items = get_flip_items()
        valued_items = get_valued_items()

        # removes non-valued, projected, and non-stable items from flip_items
        for item in flip_items:
            if item["id"] not in valued_items:
                flip_items.remove(item)

        flip_items = sorted(flip_items, key=lambda x: x["rate"])

        # get item with rap closest to target but not less than target
        for item in flip_items:
            if item["userAsset"]["asset"]["rap"] >= target:
                found = item
                break

        print(
            "Best item found: "
            + found["userAsset"]["asset"]["name"]
            + " for $"
            + str(round(found["price"], 2))
            + " at $"
            + str(found["rate"])
            + "/1kR$"
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        input("The program has crashed with the above error.")
