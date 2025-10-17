# This is a cypher.
# Define a function that will encode input.
def encode_message(message):
    encoded_message = ""
    for char in message:
        if char.isalpha(): # Check ifcharacter is a letter.
            ascii_offset = 65 if char.isupper() else 97 \
                # ASCII value of 'A' or 'a'.
            encoded_char = chr((ord(char) - ascii_offset + 15) \
                                % 26 + ascii_offset)
            encoded_message += encoded_char
        else:
            encoded_message += char # Leave non-letter characters unchanged.
    return encoded_message

# Ask user for input.
user_input = input("Enter a message to encode: ")

# Encode the user input.
encoded_message = encode_message(user_input)

# Print the encoded message.
print("Encoded message:", encoded_message)