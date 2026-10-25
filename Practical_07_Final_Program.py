"""Practical 07: Recursive factorials and combinatorial chemistry."""


def _validate_non_negative_integer(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")


def factorial(n: int) -> int:
    """Return n! using recursion, with 0! = 1 as a base case."""
    _validate_non_negative_integer(n, "n")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def factorial_trace(n: int) -> int:
    """Print recursive factorial calls as their results return."""
    _validate_non_negative_integer(n, "n")
    if n == 0 or n == 1:
        print(f"factorial({n}) = 1")
        return 1

    result = n * factorial_trace(n - 1)
    print(f"factorial({n}) = {result}")
    return result


def factorial_iterative(n: int) -> int:
    """Return n! using a loop for the optional comparison activity."""
    _validate_non_negative_integer(n, "n")
    result = 1
    for number in range(2, n + 1):
        result *= number
    return result


def combination(n: int, r: int) -> int:
    """Return the number of ways to select r items from n using factorials."""
    _validate_non_negative_integer(n, "n")
    _validate_non_negative_integer(r, "r")
    if r > n:
        raise ValueError("r cannot be greater than n.")
    return factorial(n) // (factorial(r) * factorial(n - r))


def read_non_negative_integer(prompt: str) -> int:
    """Keep asking until the user enters a non-negative whole number."""
    while True:
        user_input = input(prompt).strip()
        try:
            value = int(user_input)
        except ValueError:
            print("Please enter a whole number; decimals and text are not accepted.")
            continue

        if value < 0:
            print("Please enter a non-negative integer.")
            continue
        return value


def show_factorial() -> None:
    n = read_non_negative_integer("Enter a non-negative integer n: ")
    try:
        print(f"{n}! = {factorial(n)}")
        show_trace = input("Show the recursive call trace? (y/n): ").strip().lower()
        if show_trace == "y":
            print("Recursive calls and return values:")
            factorial_trace(n)
    except RecursionError:
        print("This value is too large for the recursive implementation.")


def show_combination() -> None:
    n = read_non_negative_integer("Enter the total number of items (n): ")
    r = read_non_negative_integer("Enter the number of items to choose (r): ")
    try:
        result = combination(n, r)
    except ValueError as error:
        print(f"Invalid combination: {error}")
        return
    except RecursionError:
        print("These values are too large for the recursive implementation.")
        return

    print(f"C({n}, {r}) = {result}")
    print("This is the number of selections when order does not matter.")


def show_chemistry_examples() -> None:
    print("\nCombinatorial chemistry examples")
    for n, r in ((5, 2), (6, 3), (8, 3)):
        print(f"C({n}, {r}) = {combination(n, r)}")

    print("\nScreening example")
    print("Number of candidate chemicals = 8")
    print("Number selected for a trial = 3")
    print(f"Number of possible selections = {combination(8, 3)}")
    print("Each selection is a different set; the order of selection does not matter.")


def compare_factorial_methods() -> None:
    n = read_non_negative_integer("Enter a non-negative integer n: ")
    try:
        recursive_result = factorial(n)
    except RecursionError:
        print("This value is too large for the recursive implementation.")
        return

    iterative_result = factorial_iterative(n)
    print(f"Recursive factorial: {recursive_result}")
    print(f"Iterative factorial: {iterative_result}")
    print(f"Results match: {recursive_result == iterative_result}")


def main() -> None:
    print("COMBINATORIAL CHEMISTRY CALCULATOR")
    while True:
        print("\n1. Calculate a factorial")
        print("2. Calculate a combination")
        print("3. Show chemistry examples")
        print("4. Compare recursive and iterative factorial")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            show_factorial()
        elif choice == "2":
            show_combination()
        elif choice == "3":
            show_chemistry_examples()
        elif choice == "4":
            compare_factorial_methods()
        elif choice == "5":
            print("Program finished.")
            break
        else:
            print("Please choose 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
