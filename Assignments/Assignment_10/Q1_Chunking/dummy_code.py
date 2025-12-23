class Animal:
    """
    A base class representing a generic animal.
    """
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        """
        Generic method for an animal sound (to be overridden by subclasses).
        """
        raise NotImplementedError("Subclass must implement abstract method")

    def __str__(self):
        """
        String representation of the Animal object.
        """
        return f"{self.name} is a {self.species}"

class Dog(Animal):
    """
    A class representing a dog, inheriting from Animal.
    """
    def __init__(self, name, age):
        super().__init__(name, species="Dog")
        self.age = age

    def speak(self):
        """
        Overrides the speak method to return a dog sound.
        """
        return f"{self.name} barks: Woof! Woof!"
    
    def fetch(self):
        """
        A unique method for dogs.
        """
        return f"{self.name} is fetching the ball."

class Cat(Animal):
    """
    A class representing a cat, inheriting from Animal.
    """
    def __init__(self, name, color):
        super().__init__(name, species="Cat")
        self.color = color

    def speak(self):
        """
        Overrides the speak method to return a cat sound.
        """
        return f"{self.name} meows: Meow!"

    def scratch(self):
        """
        A unique method for cats.
        """
        return f"{self.name} is scratching the couch!"

class Vet:
    """
    A class representing a veterinarian, using composition to interact with animals.
    """
    def check_animal(self, animal):
        """
        A method demonstrating polymorphism: it can take any object that
        has the speak method (duck typing).
        """
        print(f"Checking in {animal.name}.")
        print(f"Sound: {animal.speak()}")

# --- Example Usage ---

# Create instances of the different classes
my_dog = Dog(name="Buddy", age=3)
my_cat = Cat(name="Whiskers", color="gray")
animal_vet = Vet()

# Demonstrate methods and attributes
print(f"Dog info: {my_dog}")
print(my_dog.speak())
print(my_dog.fetch())

print("-" * 20)

print(f"Cat info: {my_cat}")
print(my_cat.speak())
print(my_cat.scratch())

print("-" * 20)

# Demonstrate polymorphism with the Vet class
animal_vet.check_animal(my_dog)
animal_vet.check_animal(my_cat)
