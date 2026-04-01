import json
import os

BANDS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "bands.json")


def load_bands():
    try:
        with open(BANDS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)["bands"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_bands(bands):
    try:
        with open(BANDS_PATH, "w", encoding="utf-8") as f:
            json.dump({"bands": bands}, f, indent=4)
    except IOError:
        print("Error saving bands.")


def get_band_by_id(bands, band_id):
    for band in bands:
        if band["id"] == band_id:
            return band
    return None


def add_band(bands, name, genre, country):
    new_id = max((band["id"] for band in bands), default=0) + 1
    bands.append({"id": new_id, "name": name, "genre": genre, "country": country})
    save_bands(bands)


if __name__ == "__main__":
    bands = load_bands()
    while True:
        print("\nMenu:")
        print("1. Show all bands")
        print("2. Find a band by ID")
        print("3. Add a new band")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            for band in bands:
                print(
                    f"{band['id']}: {band['name']} ({band['genre']}, {band['country']})"
                )
        elif choice == "2":
            band_id = int(input("Enter the band ID: "))
            band = get_band_by_id(bands, band_id)
            if band:
                print(
                    f"{band['id']}: {band['name']} ({band['genre']}, {band['country']})"
                )
            else:
                print("Band not found.")
        elif choice == "3":
            name = input("Enter the band's name: ")
            genre = input("Enter the band's genre: ")
            country = input("Enter the band's country: ")
            add_band(bands, name, genre, country)
            print("Band added successfully.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
