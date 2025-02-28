#ASCII Table Set
FIRST_CHAR_CODE = ord("A")
LAST_CHAR_CODE = ord("Z")
CHAR_RANGE = LAST_CHAR_CODE - FIRST_CHAR_CODE + 1

#function to encrypt a message using the Caesar cipher method
def caesar_shift(message, shift):
    """
    Encrypts a message using the Caesar cipher with a specified shift.

    Parameters:
    message (str): The message to be encrypted.
    shift (int): The number of positions to shift the characters.

    Returns:
    None: The encrypted message is printed to the console.
    """
    # Initialize the result variable to store the encrypted message
    result = ""

    # Iterate through each character in the message, converting it to uppercase
    for char in message.upper():
        if char.isalpha(): # Check if the character is an alphabet letter
            # Convert character to ASCII value
            char_code = ord(char)
            
            new_char_code = char_code + shift
            
            if new_char_code > LAST_CHAR_CODE:
                new_char_code -= CHAR_RANGE 

            if new_char_code < FIRST_CHAR_CODE:
                new_char_code += CHAR_RANGE

            new_char = chr(new_char_code)

            result = result + new_char
        else:
            result += char

    print(result)
 
user_message = input("Message to Encrypt: ")
user_shift_key = int(input("Shift Key (integer): "))
caesar_shift(user_message, user_shift_key)