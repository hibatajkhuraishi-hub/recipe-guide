🍬 Recipe Guide

A simple and explainable recipe recommendation web application that provides ingredients, cooking methods, source comparison, taste and fragrance guidance, and guardrail checks for traditional sweets.

📌 Overview

Recipe Guide allows a user to enter the name of a sweet and receive a complete recipe.

Instead of only displaying a recipe, the application also explains:

- 🥣 Ingredients required
- 👩‍🍳 Step-by-step cooking method
- 📚 Sources used for the recipe
- 🔍 Comparison between available sources
- ⭐ Evidence-based decision score
- 🏆 Selected best cooking method
- 👅 Factors that affect taste
- 🌸 Factors that affect fragrance
- ⚙️ Cooking effects and their impact on the final result
- 🛡️ Guardrail warnings when important information or evidence is missing

The project uses a rule-based and evidence-grounded approach so that the application's decisions are understandable and transparent.

---

✨ Key Features

🍯 Recipe Search

Users can search for sweets such as:

- Gulab Jamun
- Rasgulla
- Jalebi
- Kaju Katli
- Gajar Halwa
- Rasmalai
- Motichoor Ladoo
- Besan Ladoo
- Soan Papdi
- Mysore Pak

The search supports:

- Exact names
- Different capitalization
- Extra spaces
- Partial recipe names
- Individual word matching

For example:

gulab jamun
GULAB JAMUN
  Gulab   Jamun
gulab

can all be matched to the available recipe.

---

🧠 Explainable Recipe Selection

The application does not simply return a recipe.

It compares available source information and calculates a decision score.

The scoring system considers:

Factor| Maximum Score
Source agreement| 40
Ingredient completeness| 25
Cooking method completeness| 20
Cooking guidance| 15
Total| 100

These weights are design choices created for this assignment to make the recommendation process transparent.

---

🔍 Source Comparison

When multiple sources are available, the backend compares information such as:

- Ingredients
- Cooking methods
- Cooking guidance

Information supported by multiple sources receives higher priority.

The application also keeps source differences visible rather than hiding them.

For example, the system can identify:

Multiple sources support the ingredient: cardamom

Multiple sources support the method: fry

Multiple sources support the cooking guidance: cook on low heat

This makes the reasoning behind the recommendation easier to understand.

---

🏆 Best Method Selection

The application evaluates the cooking method from each available source.

A source receives points based on:

- Number of cooking steps
- Completeness of the method
- Cooking guidance
- Agreement with other sources

The source with the strongest score is selected as the recommended method.

The application also displays the scores of the other available source methods.

This allows the user to understand why a particular method was selected.

---

👅 Taste & Fragrance Analysis

The application explains parameters that can affect the final result.

These include:

Taste

Examples include:

- Sweetness
- Richness
- Texture
- Spice balance

Fragrance

Examples include:

- Cardamom
- Saffron
- Rose
- Ghee
- Roasting aroma

Cooking Effects

The application also explains how cooking decisions can change the final recipe.

Examples:

- Cooking temperature
- Frying time
- Roasting
- Sugar syrup consistency
- Cooking time
- Ingredient proportions

---

🛡️ Guardrails

The application includes basic guardrails to prevent unsupported or incomplete recommendations.

The backend checks whether:

- Ingredients are available
- Cooking steps are available
- Source information is available
- A decision explanation exists
- Taste information is available
- Fragrance information is available
- Cooking effects are described

The application also identifies situations where only one source is available and lowers confidence accordingly.

If the evidence score is low, the application displays a warning instead of presenting the recommendation as highly confident.

---

🏗️ Architecture

The application follows a simple three-layer architecture:

                    USER
                      │
                      ▼
              ┌───────────────┐
              │   Frontend    │
              │  index.html   │
              └───────┬───────┘
                      │
                 HTTP GET
                      │
                      ▼
              ┌───────────────┐
              │    FastAPI    │
              │    main.py    │
              └───────┬───────┘
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
       Recipe       Source       Guardrail
       Lookup     Comparison      Checks
          │           │            │
          └───────────┼────────────┘
                      ▼
                Decision Score
                      │
                      ▼
              Best Method Selection
                      │
                      ▼
                  JSON Response
                      │
                      ▼
              ┌───────────────┐
              │   Frontend    │
              │ Displays Data │
              └───────────────┘

---

📂 Project Structure

recipe-guide/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── recipes.py
│   │
│   └── static/
│       └── index.html
│
└── README.md

"main.py"

The backend application.

It handles:

- FastAPI setup
- Recipe searching
- Input normalization
- Source comparison
- Evidence scoring
- Best method selection
- Guardrail checks
- API responses

"recipes.py"

Contains the recipe dataset.

Each recipe contains information such as:

ingredients
steps
sources
source_details
decision
taste_and_fragrance

The "source_details" section provides structured evidence that allows the backend to compare sources.

"index.html"

The frontend interface.

It contains:

- HTML structure
- CSS styling
- JavaScript functionality
- Search interface
- Recipe display
- Decision score display
- Source comparison display
- Guardrail display

---

🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- HTML5
- CSS3
- JavaScript
- Git
- GitHub

---

🔄 Application Flow

The basic processing flow is:

User enters sweet name
        ↓
Frontend sends request
        ↓
FastAPI receives request
        ↓
Input is normalized
        ↓
Recipe is located
        ↓
Sources are compared
        ↓
Evidence score is calculated
        ↓
Best cooking method is selected
        ↓
Guardrails are checked
        ↓
JSON response is returned
        ↓
Frontend displays the result

In short:

Receive → Find → Compare → Score → Select → Check → Return

---

🚀 How to Run Locally

1. Clone the repository

git clone https://github.com/hibatajkhuraishi-hub/recipe-guide.git

2. Open the project

cd recipe-guide

3. Install dependencies

pip install fastapi uvicorn

4. Start the FastAPI server

uvicorn app.main:app --reload

5. Open the application

Open your browser and visit:

http://127.0.0.1:8000/

---

🔌 API Endpoint

The application provides the following endpoint:

GET /recipe/{sweet_name}

Example:

GET /recipe/gulab%20jamun

The API returns JSON containing:

sweet
recipe
decision_score
decision_reasons
source_comparison
best_method_selection
guardrail_warnings

---

📊 Example Response Structure

{
  "sweet": "Gulab Jamun",
  "recipe": {},
  "decision_score": 85,
  "decision_reasons": [],
  "source_comparison": {},
  "best_method_selection": {},
  "guardrail_warnings": []
}

---

🧪 Testing

The application was tested with different types of user input, including:

- Exact recipe names
- Uppercase names
- Lowercase names
- Extra spaces
- Partial names
- Individual words
- Recipes that do not exist

The API was also checked to ensure that it returns:

- Recipe information
- Ingredients
- Cooking steps
- Decision score
- Source comparison
- Best method
- Guardrail warnings

---

⚠️ Current Limitations

This project currently uses a predefined recipe dataset.

Therefore:

- It cannot automatically discover new recipes.
- Source comparison depends on structured information stored in the dataset.
- Exact text matching may not recognize semantically similar statements written in different ways.
- Some recipes have fewer available sources than others.
- The scoring weights are manually designed for this assignment and are not scientifically validated.

---

🔮 Future Improvements

Possible improvements include:

🗄️ Database

Move recipes and source information from Python dictionaries into a database.

🌐 Real-Time Sources

Automatically retrieve and compare recipe information from verified sources.

🧠 Semantic Comparison

Use embeddings or an NLP/LLM-based approach to recognize when different sources express the same idea using different wording.

🤖 AI Recipe Assistant

Add an AI model that can understand more flexible user questions such as:

How do I make soft Gulab Jamun?

Which method gives a stronger cardamom flavour?

What happens if I overcook the sugar syrup?

🧪 Automated Testing

Add unit and integration tests for:

- Recipe matching
- Source comparison
- Score calculation
- Method selection
- Guardrails
- API responses

🚀 Production Deployment

Deploy the FastAPI backend using a production-ready hosting environment and add logging, monitoring, validation, and authentication where required.

---

🎯 Why This Project?

The goal of Recipe Guide is not only to provide a recipe but to demonstrate how a recommendation system can make its decisions transparent and explainable.

Instead of returning only:

"Here is your recipe."

the application attempts to answer:

"What information was considered?"
"How did the sources compare?"
"Why was this method selected?"
"What factors affect taste and fragrance?"
"Are there any limitations or warnings?"

This makes the application more understandable and easier to evaluate.

---

👩‍💻 Author

Hiba Tk Khuraishi

GitHub:
https://github.com/hibatajkhuraishi-hub

Project Repository:
https://github.com/hibatajkhuraishi-hub/recipe-guide
