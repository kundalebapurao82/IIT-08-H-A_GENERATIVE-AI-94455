# Write a python program that takes a sentence from the user and prints

sentence = input("Enter sentence: ")
print(f"You entered sentence: ", sentence)


# Number of characters
count = 0
for ch in sentence:
    count = count+1
print(f"Number of characters in the sentence '{sentence}'Su are: ",count)


# Number of words
words = sentence.split()
print("No. of words in sentence are: ", len(words))


# Number of vowels
vowels = ['a','e','i','o','u']
v_count = 0
sentence_lower = sentence.lower()
for ch in sentence_lower:
    if ch in vowels:
        v_count = v_count +1

print(f"Number of vowels in sentence are: {v_count}")


