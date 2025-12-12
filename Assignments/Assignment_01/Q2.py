# Count Even and Odd Numbers

# Take a list of numbers as input (comma-separated).

# Count how many are even and how many are odd.


numbers = [1,23,15,11,34,56,25,43,61,33,49,77,82,92]

print(f"Numbers list: {numbers}")

print(f"Total numbers in list are: {len(numbers)}")

even = []
odd = []
e_count = 0
o_count = 0
for num in numbers:
    if num % 2 == 0:             # Filters even numbers
        e_count = e_count+1        # increase count of even numbers
        even.append(num)        # append number to list of even numbers
    else:                           # Filters odd numbers
        o_count = o_count+1         # increase count of odd numbers
        odd.append(num)           # append num to list of odd numbers
           
print(f"Total odd numbers: {o_count}")       # prints count of odd numbers
print(odd)                                     # prints odd numbers list
print(f"\nTotal even numbers: {e_count}")   # prints count of even numbers
print(even)                                 # prints list of even numbers