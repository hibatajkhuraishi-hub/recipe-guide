from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.recipes import recipes


app = FastAPI(title="Recipe Guide")


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("app/static/index.html")


# --------------------------------------------------
# RECIPE NAME MATCHING
# --------------------------------------------------

def normalize_name(name):
    """
    Converts the user's input into a consistent format.
    Example:
    "  GULAB   JAMUN  " -> "gulab jamun"
    """

    return " ".join(
        name.strip().lower().split()
    )


def find_recipe(sweet_name):
    """
    Finds a recipe using:
    1. Exact match
    2. Case-insensitive match
    3. Partial word match
    """

    search_name = normalize_name(sweet_name)

    if not search_name:
        return None, None

    # Exact normalized match
    for name in recipes:

        if normalize_name(name) == search_name:
            return name, recipes[name]

    # Partial match
    for name in recipes:

        normalized_name = normalize_name(name)

        if (
            search_name in normalized_name
            or normalized_name in search_name
        ):
            return name, recipes[name]

    # Match individual words
    search_words = search_name.split()

    for name in recipes:

        normalized_name = normalize_name(name)
        recipe_words = normalized_name.split()

        for word in search_words:

            if len(word) >= 3 and word in recipe_words:
                return name, recipes[name]

    return None, None


# --------------------------------------------------
# SOURCE COMPARISON
# --------------------------------------------------

def compare_lists(source_details, key):

    if not source_details:
        return []

    counts = {}

    for source in source_details:

        items = source.get(key, [])

        for item in items:

            item = item.strip().lower()

            if item:
                counts[item] = counts.get(item, 0) + 1

    common_items = []

    for item, count in counts.items():

        if count >= 2:
            common_items.append(item)

    return common_items


def compare_sources(recipe):

    source_details = recipe.get(
        "source_details",
        []
    )

    source_count = len(source_details)

    if source_count == 0:

        return {
            "source_count": 0,
            "agreement_score": 0,
            "agreement": [],
            "differences": [],
            "selection_reasons": [
                "No source information is available."
            ]
        }

    if source_count == 1:

        return {
            "source_count": 1,
            "agreement_score": 20,
            "agreement": [
                "Only one source is available, so cross-source agreement cannot be established."
            ],
            "differences": [],
            "selection_reasons": [
                "The available source was used because no second independent source is currently available.",
                "Confidence is lower because the method could not be compared across multiple sources."
            ]
        }

    common_ingredients = compare_lists(
        source_details,
        "ingredient_support"
    )

    common_methods = compare_lists(
        source_details,
        "method_support"
    )

    common_guidance = compare_lists(
        source_details,
        "cooking_guidance"
    )

    ingredient_strength = min(
        len(common_ingredients) / 4,
        1
    )

    method_strength = min(
        len(common_methods) / 4,
        1
    )

    guidance_strength = min(
        len(common_guidance) / 3,
        1
    )

    agreement_strength = (
        ingredient_strength * 0.4
        + method_strength * 0.4
        + guidance_strength * 0.2
    )

    agreement_score = round(
        agreement_strength * 40
    )

    agreement = []

    for item in common_ingredients:

        agreement.append(
            "Multiple sources support the ingredient: "
            + item
        )

    for item in common_methods:

        agreement.append(
            "Multiple sources support the method: "
            + item
        )

    for item in common_guidance:

        agreement.append(
            "Multiple sources support the cooking guidance: "
            + item
        )

    differences = []

    for source in source_details:

        source_ingredients = [
            item.strip().lower()
            for item in source.get(
                "ingredient_support",
                []
            )
        ]

        source_methods = [
            item.strip().lower()
            for item in source.get(
                "method_support",
                []
            )
        ]

        unique_ingredients = [
            item
            for item in source_ingredients
            if item not in common_ingredients
        ]

        unique_methods = [
            item
            for item in source_methods
            if item not in common_methods
        ]

        differences.append({
            "source": source.get(
                "source",
                "Unknown source"
            ),
            "unique_ingredients": unique_ingredients,
            "unique_method_points": unique_methods
        })

    selection_reasons = [
        "Information supported by multiple sources receives higher priority.",
        "Common ingredients and cooking steps are treated as stronger evidence.",
        "Detailed cooking guidance is retained when it improves the method.",
        "Differences between sources remain visible instead of being hidden."
    ]

    return {
        "source_count": source_count,
        "agreement_score": agreement_score,
        "agreement": agreement,
        "differences": differences,
        "selection_reasons": selection_reasons
    }


# --------------------------------------------------
# SOURCE SELECTION ENGINE
# --------------------------------------------------

def select_best_method(recipe):

    source_details = recipe.get(
        "source_details",
        []
    )

    if not source_details:

        return {
            "selected_method": [],
            "selection_score": 0,
            "reason": "No source method is available.",
            "source_scores": []
        }

    method_scores = []

    common_methods = compare_lists(
        source_details,
        "method_support"
    )

    common_guidance = compare_lists(
        source_details,
        "cooking_guidance"
    )

    for source in source_details:

        methods = source.get(
            "method_support",
            []
        )

        guidance = source.get(
            "cooking_guidance",
            []
        )

        score = 0

        # Method completeness
        score += min(
            len(methods) * 5,
            30
        )

        # Cooking guidance
        score += min(
            len(guidance) * 5,
            20
        )

        # Agreement on method
        for method in methods:

            normalized_method = (
                method.strip().lower()
            )

            if normalized_method in common_methods:

                score += 5

        # Agreement on cooking guidance
        for item in guidance:

            normalized_item = (
                item.strip().lower()
            )

            if normalized_item in common_guidance:

                score += 3

        method_scores.append({
            "source": source.get(
                "source",
                "Unknown source"
            ),
            "method": methods,
            "score": score
        })

    method_scores.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    best_source = method_scores[0]

    return {
        "selected_method": best_source["method"],
        "selected_source": best_source["source"],
        "selection_score": min(
            best_source["score"],
            100
        ),
        "reason": (
            "This source method received the highest score "
            "because it provides detailed cooking steps and "
            "has stronger support from the available evidence."
        ),
        "source_scores": method_scores
    }


# --------------------------------------------------
# RECOMMENDATION SCORE
# --------------------------------------------------

def calculate_score(recipe):

    source_comparison = compare_sources(recipe)

    score = source_comparison[
        "agreement_score"
    ]

    reasons = []

    ingredients = recipe.get(
        "ingredients",
        []
    )

    steps = recipe.get(
        "steps",
        []
    )

    taste_data = recipe.get(
        "taste_and_fragrance",
        {}
    )

    cooking_effects = taste_data.get(
        "cooking_effects",
        []
    )

    # Ingredient completeness: 25 points

    if len(ingredients) >= 5:

        score += 25

        reasons.append(
            "The recipe provides a sufficiently detailed ingredient list."
        )

    elif len(ingredients) > 0:

        score += 15

        reasons.append(
            "The recipe contains ingredients, but the list is limited."
        )

    else:

        reasons.append(
            "The recipe does not provide enough ingredient information."
        )

    # Method completeness: 20 points

    if len(steps) >= 5:

        score += 20

        reasons.append(
            "The cooking method contains detailed preparation steps."
        )

    elif len(steps) > 0:

        score += 10

        reasons.append(
            "The recipe contains cooking steps, but the method is less detailed."
        )

    else:

        reasons.append(
            "The recipe does not provide enough cooking instructions."
        )

    # Cooking guidance: 15 points

    if len(cooking_effects) >= 2:

        score += 15

        reasons.append(
            "The recipe explains how cooking choices affect the final result."
        )

    elif len(cooking_effects) > 0:

        score += 8

        reasons.append(
            "Some cooking effects are explained."
        )

    else:

        reasons.append(
            "The recipe does not provide enough cooking-effect guidance."
        )

    # Source confidence

    if source_comparison[
        "agreement_score"
    ] >= 35:

        reasons.append(
            "The recipe has strong agreement across the available sources."
        )

    elif source_comparison[
        "agreement_score"
    ] >= 25:

        reasons.append(
            "The recipe has moderate agreement across the available sources."
        )

    elif source_comparison[
        "source_count"
    ] == 1:

        reasons.append(
            "Only one source is available, so cross-source confidence is lower."
        )

    else:

        reasons.append(
            "Source agreement is limited, so the recommendation should be treated with caution."
        )

    return min(score, 100), reasons


# --------------------------------------------------
# GUARDRAILS
# --------------------------------------------------

def check_guardrails(recipe):

    warnings = []

    ingredients = recipe.get(
        "ingredients",
        []
    )

    steps = recipe.get(
        "steps",
        []
    )

    sources = recipe.get(
        "sources",
        []
    )

    decision = recipe.get(
        "decision",
        ""
    )

    taste_data = recipe.get(
        "taste_and_fragrance",
        {}
    )

    # Basic recipe checks

    if not ingredients:

        warnings.append(
            "The recipe does not contain an ingredient list."
        )

    if not steps:

        warnings.append(
            "The recipe does not contain cooking instructions."
        )

    if not sources:

        warnings.append(
            "No source information is available."
        )

    if not decision:

        warnings.append(
            "No decision explanation is available."
        )

    # Taste and fragrance checks

    if not taste_data.get("taste"):

        warnings.append(
            "Taste effects are not sufficiently described."
        )

    if not taste_data.get("fragrance"):

        warnings.append(
            "Fragrance effects are not sufficiently described."
        )

    if not taste_data.get("cooking_effects"):

        warnings.append(
            "Cooking effects are not sufficiently described."
        )

    # Source confidence check

    source_details = recipe.get(
        "source_details",
        []
    )

    if len(source_details) == 1:

        warnings.append(
            "Only one source is available, so cross-source confidence is lower."
        )

    # Final evidence score check

    score, _ = calculate_score(recipe)

    if score < 50:

        warnings.append(
            "The evidence score is low. The recommendation should not be treated as highly confident."
        )

    return warnings


# --------------------------------------------------
# RECIPE API
# --------------------------------------------------

@app.get("/recipe/{sweet_name}")
def get_recipe(sweet_name: str):

    recipe_name, recipe = find_recipe(
        sweet_name
    )

    if recipe is None:

        return {
            "message": "Recipe not found",
            "guardrail_warnings": [
                "The requested sweet is not available in the current recipe database."
            ]
        }

    score, reasons = calculate_score(
        recipe
    )

    source_comparison = compare_sources(
        recipe
    )

    best_method = select_best_method(
        recipe
    )

    guardrail_warnings = check_guardrails(
        recipe
    )

    return {
        "sweet": recipe_name,
        "recipe": recipe,
        "decision_score": score,
        "decision_reasons": reasons,
        "source_comparison": source_comparison,
        "best_method_selection": best_method,
        "guardrail_warnings": guardrail_warnings
    }