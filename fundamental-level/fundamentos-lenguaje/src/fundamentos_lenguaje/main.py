import json
import os


class Main:

    def __init__(self):
        self.bands = self.load_bands()

    def load_bands(self):
        try:
            bands_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "bands.json"
            )
            with open(bands_path, "r", encoding="utf-8") as f:
                return json.load(f)["bands"]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_bands(self):
        try:
            bands_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "bands.json"
            )
            with open(bands_path, "w", encoding="utf-8") as f:
                json.dump({"bands": self.bands}, f, indent=4)
        except IOError:
            print("Error saving bands.")

    def get_band_by_id(self, band_id):
        for band in self.bands:
            if band["id"] == band_id:
                return band
        return None

    def add_band(self, name, genre, country):
        new_id = max(band["id"] for band in self.bands) + 1
        new_band = {"id": new_id, "name": name, "genre": genre, "country": country}
        self.bands.append(new_band)
        self.save_bands()

    def run(self):
        """Show a menu, ask for show all bands, find a band by id, add a new band or exit."""
        while True:
            print("\nMenu:")
            print("1. Show all bands")
            print("2. Find a band by ID")
            print("3. Add a new band")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                for band in self.bands:
                    print(
                        f"{band['id']}: {band['name']} ({band['genre']}, {band['country']})"
                    )
            elif choice == "2":
                band_id = int(input("Enter the band ID: "))
                band = self.get_band_by_id(band_id)
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
                self.add_band(name, genre, country)
                print("Band added successfully.")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    Main().run()
