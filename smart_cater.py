from dataclasses import dataclass
from typing import List, Set, Callable


@dataclass(frozen=True)
class Meal:
    name: str
    ingredients: List[str]
    categories: Set[str]


def normalize(text: str) -> str:
    return text.strip().lower()


def search_meals(meals: List[Meal], query: str, matcher: Callable[[Meal, str], bool]) -> List[Meal]:
    q = normalize(query)
    return [meal for meal in meals if matcher(meal, q)]


def match_by_name(meal: Meal, q: str) -> bool:
    return q in normalize(meal.name)


def match_by_ingredient(meal: Meal, q: str) -> bool:
    return any(q in normalize(ing) for ing in meal.ingredients)


def match_by_category(meal: Meal, q: str) -> bool:
    return q in {normalize(c) for c in meal.categories}


def print_results(results: List[Meal]) -> None:
    if not results:
        print("\nNo meals found.\n")
        return

    print(f"\nFound {len(results)} meal(s):")
    for meal in results:
        cats = ", ".join(sorted(meal.categories))
        ings = ", ".join(meal.ingredients)
        print(f"- {meal.name} [{cats}]")
        print(f"  Ingredients: {ings}")
    print("")


def build_sample_meals() -> List[Meal]:
    # Sample data for the demo (in-memory, no database)
    return [
        Meal(
            name="Vegan Chili",
            ingredients=["beans", "tomato", "onion", "garlic", "chili powder"],
            categories={"vegan", "gluten-free"}
        ),
        Meal(
            name="Quick Pasta",
            ingredients=["pasta", "tomato sauce", "olive oil", "basil", "parmesan"],
            categories={"quick meals", "vegetarian"}
        ),
        Meal(
            name="Chicken Curry",
            ingredients=["chicken", "coconut milk", "curry paste", "onion", "rice"],
            categories={"high protein"}
        ),
        Meal(
            name="Gluten-Free Pancakes",
            ingredients=["gluten-free flour", "milk", "egg", "baking powder", "maple syrup"],
            categories={"gluten-free", "quick meals"}
        ),
        Meal(
            name="Greek Salad",
            ingredients=["cucumber", "tomato", "feta", "olive oil", "olives"],
            categories={"vegetarian", "quick meals"}
        ),
    ]


def main() -> None:
    meals = build_sample_meals()

    actions = {
        "1": ("Search by meal name", match_by_name),
        "2": ("Search by ingredient", match_by_ingredient),
        "3": ("Search by category", match_by_category),
        "4": ("Exit", None),
    }

    print("SmartCater Prototype (Search Feature)")
    print("-----------------------------------")

    while True:
        print("\nChoose an option:")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")

        choice = input("> ").strip()

        if choice == "4":
            print("Bye!")
            break

        if choice not in actions or actions[choice][1] is None:
            print("Invalid choice. Try again.")
            continue

        query = input("Enter your search term: ").strip()
        matcher = actions[choice][1]
        results = search_meals(meals, query, matcher)
        print_results(results)


if __name__ == "__main__":
    main()
