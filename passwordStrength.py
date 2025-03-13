import sys
import math
import requests
import hashlib
import tty
import termios

# Function to check if a password is leaked using HaveIBeenPwned API
def check_pwned(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code == 200:
        hashes = (line.split(":") for line in response.text.splitlines())
        if any(suffix == hash_val for hash_val, _ in hashes):
            return True  # Password found in breaches
    return False

# Function to calculate password entropy
def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in "`!@#$%^&*()-=;',./~_+:<>?" for c in password):
        charset_size += 32  # Special characters

    entropy = math.log2(charset_size ** len(password))
    return entropy

# Function to take masked password input (show * while typing)
def masked_input(prompt="Enter Password: "):
    print(prompt, end="", flush=True)
    password = ""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            char = sys.stdin.read(1)
            if char == "\n" or char == "\r":  # Enter key
                break
            elif char == "\x7f":  # Backspace key
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write("\b \b")  # Remove last `*`
                    sys.stdout.flush()
            else:
                password += char
                sys.stdout.write("*")  # Display `*`
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print()  # Move to new line after input
    return password

# Function to check password strength
def analyze_password(password):
    n = len(password)

    # Check password length
    if n < 8:
        return "Password is too short! Must be at least 8 characters."
    elif n > 64:
        return "Password is too long! Must be under 64 characters."

    # Check if the password has been leaked
    if check_pwned(password):
        return "This password has been found in data breaches. Do not use it!"

    # Check for character types
    hasLower = any(c.islower() for c in password)
    hasUpper = any(c.isupper() for c in password)
    hasDigit = any(c.isdigit() for c in password)
    hasSpecial = any(c in "`!@#$%^&*()-=;',./~_+:<>?" for c in password)

    # Calculate entropy
    entropy = calculate_entropy(password)

    # Determine password strength
    if hasLower and hasUpper and hasDigit and hasSpecial and entropy > 60:
        return "Strong Password (High Entropy)"
    elif (hasLower or hasUpper) and hasDigit and entropy > 45:
        return "Moderate Password (Consider adding more complexity)"
    else:
        return "Weak Password (Easily guessable)"

# Loop until the user enters a strong password
while True:
    password_input = masked_input("Enter your password: ")
    strength_result = analyze_password(password_input)

    print(strength_result)  # Show password strength result

    if "Strong" in strength_result:
        print("Password accepted!")
        break  # Exit loop if the password is strong
    else:
        print("Please try again with a stronger password.\n")
