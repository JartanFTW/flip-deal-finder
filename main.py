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


def display_result(items):
    # prints out best items in blocks of 5, with the option to view more or exit
    print("Best listings found:")
    for i in range(0, len(items), 5):
        for item in items[i : i + 5]:
            print(
                item["userAsset"]["asset"]["name"]
                + " for $"
                + str(round(item["price"], 2))
                + " at $"
                + str(item["rate"])
                + "/1kR$ for "
                + str(bt_to_at(item["userAsset"]["asset"]["rap"]))
                + " A/T"
            )
        if i + 5 < len(items):
            while True:
                try:
                    choice = int(
                        input("Would you like to see more? (1 = yes, 2 = no): ")
                    )
                except TypeError:
                    print("That is not a valid number. Please enter an integer.")
                    continue
                if choice == 1:
                    break
                elif choice == 2:
                    return
                else:
                    print("That is not a valid choice. Please enter 1 or 2.")
                    continue


def at_to_bt(after_tax: int):
    return floor(after_tax / 0.7)


def bt_to_at(before_tax: int):
    return floor(before_tax * 0.7)


def difference(x, y):
    return abs(x - y)


def main():

    while True:
        target = get_target()
        flip_items = get_flip_items()
        valued_items = get_valued_items()

        print(f"Target: {target} B/T {bt_to_at(target)} A/T")

        # removes non-valued, projected, and non-stable items from flip_items
        for item in flip_items.copy():
            if item["userAsset"]["asset"]["assetId"] not in valued_items:
                flip_items.remove(item)

        # remove duplicate items with higher rate than lowest of that item
        lowest_items = {}
        for item in flip_items:
            if item["userAsset"]["asset"]["name"] not in lowest_items.keys():
                lowest_items[item["userAsset"]["asset"]["name"]] = item
            elif (
                item["rate"] < lowest_items[item["userAsset"]["asset"]["name"]]["rate"]
            ):
                lowest_items[item["userAsset"]["asset"]["name"]] = item

        # sort by difference between item rap and target rap
        lowest_items = [x for x in lowest_items.values()]
        result = sorted(
            lowest_items,
            key=lambda x: difference(x["userAsset"]["asset"]["rap"], target),
        )

        display_result(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        input("The program has crashed with the above error.")
