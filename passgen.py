"""
Password Generator
------------------
A command-line tool that creates secure random passwords.

Run:  python password_generator.py
"""

import secrets
import string

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?"


def ask_yes_no(question):
    """Keep asking until the user answers y or n."""
    while True:
        answer = input(f"{question} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def ask_length():
    """Ask for a valid password length (minimum 4, maximum 128)."""
    while True:
        raw = input("Password length (4-128): ").strip()
        if raw.isdigit() and 4 <= int(raw) <= 128:
            return int(raw)
        print("Enter a whole number between 4 and 128.")


def generate_password(length, use_lower, use_upper, use_digits, use_symbols):
    """Build a password that contains at least one of each chosen type."""
    pools = []
    if use_lower:
        pools.append(LOWER)
    if use_upper:
        pools.append(UPPER)
    if use_digits:
        pools.append(DIGITS)
    if use_symbols:
        pools.append(SYMBOLS)

    if not pools:
        raise ValueError("Choose at least one character type.")

    # Guarantee one character from each selected pool
    password = [secrets.choice(pool) for pool in pools]

    # Fill the rest from all selected characters combined
    all_chars = "".join(pools)
    password += [secrets.choice(all_chars) for _ in range(length - len(password))]

    # Shuffle so the guaranteed characters aren't always at the start
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def rate_strength(password):
    """Give a simple strength rating based on length and variety."""
    score = 0
    score += len(password) >= 8
    score += len(password) >= 12
    score += len(password) >= 16
    score += any(c in LOWER for c in password)
    score += any(c in UPPER for c in password)
    score += any(c in DIGITS for c in password)
    score += any(c in SYMBOLS for c in password)

    if score <= 3:
        return "Weak"
    if score <= 5:
        return "Medium"
    return "Strong"


def save_to_file(passwords, filename="passwords.txt"):
    """Append generated passwords to a text file."""
    with open(filename, "a", encoding="utf-8") as f:
        for p in passwords:
            f.write(p + "\n")
    print(f"Saved to {filename}")


def main():
    print("=== Password Generator ===\n")

    while True:
        length = ask_length()
        use_lower = ask_yes_no("Include lowercase letters?")
        use_upper = ask_yes_no("Include uppercase letters?")
        use_digits = ask_yes_no("Include numbers?")
        use_symbols = ask_yes_no("Include symbols?")

        if not any([use_lower, use_upper, use_digits, use_symbols]):
            print("\nYou must choose at least one type. Try again.\n")
            continue

        count_raw = input("How many passwords? (default 1): ").strip()
        count = int(count_raw) if count_raw.isdigit() and int(count_raw) > 0 else 1

        passwords = [
            generate_password(length, use_lower, use_upper, use_digits, use_symbols)
            for _ in range(count)
        ]

        print()
        for p in passwords:
            print(f"{p}   [{rate_strength(p)}]")
        print()

        if ask_yes_no("Save to a file?"):
            save_to_file(passwords)

        if not ask_yes_no("\nGenerate more?"):
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
