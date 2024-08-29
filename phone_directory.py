class PhoneDirectory:
    def __init__(self, capacity=300):
        print("The maximum number of contacts you can save in your phone is", capacity, "\n")
        self.max = capacity                           # The maximum number of contacts can be saved is 300
        self.size = 0
        self.arr = [[] for _ in range(self.max)]      # This creates an array where mobile no. will be act as a key and other related information will be act as value
        self.name_to_number = {}                      # This creates a dictionary to store name as key and mob no. as value ( whenever we will need mob no. for accessing information in the array through required name, then we will search that number in this dictionary from name which will be a key value)

    def get_hash(self, mob_no):
        if 1000000000 <= mob_no <= 9999999999:        # 10-Digit Mobile Number for getting hash value which will be the index of the array where we need to store the contact details
            return mob_no % self.max
        raise ValueError("Enter a valid 10-digit mobile number\n") 

    def __setitem__(self, key, value):
        # Unpack the tuple
        if isinstance(key, int) and isinstance(value, tuple) and len(value) == 3:
            name, gender, place = value
            mob_no = key                                   
            if not isinstance(name, str) or not isinstance(gender, str) or not isinstance(place, str):
                raise ValueError("Name, gender, and place must be strings")
            if name is None or gender is None or place is None:
                raise ValueError("Name, gender, and place cannot be None")
            self._set_contact_by_number(mob_no, name, gender, place)
        else:
            raise TypeError("Key must be an integer mobile number and value must be a tuple (name, gender, place)")

    def _set_contact_by_number(self, mob_no, name, gender, place):
        if self.size >= self.max:
            raise ValueError("Maximum capacity reached. Please delete unwanted contacts before adding new ones.\n")

        # Update the name if it exists
        if name in self.name_to_number:
            print("The contact name already exists. Do you want to update the name? (1 for Yes, 0 for No)")
            a = int(input())
            if a:
                print("Enter the new contact name you wish to be saved:")
                new_name = input()
                if new_name in self.name_to_number:
                    print("The new name already exists. Please choose a different name.")
                    return
                self.name_to_number[new_name] = self.name_to_number.pop(name)
                name = new_name

        # Save or update contact
        h = self.get_hash(mob_no)
        for index, element in enumerate(self.arr[h]):
            if len(element) == 4 and element[0] == mob_no:
                print("Updating contact. Please wait...\n")
                del self.name_to_number[element[1]]
                self.arr[h][index] = (mob_no, name, gender, place)
                self.name_to_number[name] = mob_no
                print("Contact updated successfully\n")
                return

        # Add new contact
        print("Saving new contact...\n")
        self.arr[h].append((mob_no, name, gender, place))
        self.size += 1
        self.name_to_number[name] = mob_no
        print("Contact saved successfully\n")

    def __getitem__(self, key):
        if isinstance(key, int):  # Mobile number
            return self._get_contact_by_number(key)
        elif isinstance(key, str):  # Name
            return self._get_contact_by_name(key)
        else:
            raise TypeError("Key must be either a mobile number (int) or a name (str)")

    def _get_contact_by_number(self, mob_no):
        arr_index = self.get_hash(mob_no)
        for element in self.arr[arr_index]:
            if element[0] == mob_no:
                print("Here is your contact information:\n", element)
                return element
        raise KeyError(f"No contact found with mobile number '{mob_no}'")

    def _get_contact_by_name(self, name):
        mob_no = self.name_to_number.get(name)
        if mob_no:
            return self._get_contact_by_number(mob_no)
        else:
            raise KeyError(f"No contact found with the name '{name}'")

    def __delitem__(self, name):
        print("Deleting contact...\n")
        mob_no = self.name_to_number.pop(name, None)
        if mob_no is None:
            print("No contact found with the name\n")
            return

        arr_index = self.get_hash(mob_no)
        for index, element in enumerate(self.arr[arr_index]):
            if element[0] == mob_no: 
                del self.arr[arr_index][index]
                self.size -= 1
                print("Contact successfully deleted\n")
                return

        print("Contact not found in the directory\n")


# Testing the class
phone_directory = PhoneDirectory()

# Insert a new contact using subscript notation
phone_directory[1234567890] = ("John Doe", "Male", "New York")

# Insert another contact
phone_directory[9876543210] = ("Jane Smith", "Female", "Los Angeles")

phone_directory[1234509876] = ("Rohit Kumar", "Male", "Los Vegas")
phone_directory[1243658709] = ("Aditya Gupta", "Male", "San Fransisco")
phone_directory[1324857690] = ("Aadhar Goel", "Male", "Delhi") 

# Retrieve contact information by mobile number
print(phone_directory[1234567890])

# Retrieve contact information by name
print(phone_directory["John Doe"])

print(phone_directory[1234509876])


# Delete a contact by name
del phone_directory["John Doe"]

# Attempt to retrieve the deleted contact
try:
    print(phone_directory["John Doe"])
except KeyError as e:
    print(e)
