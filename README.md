# TTChef Project: Report

## Introduction
The TTChef project develops a platform for evaluating AI-generated and human-authored recipes through a Turing Test. It aims to understand how chefs and food enthusiasts distinguish between real and fake recipes. The project combines frontend and backend technologies, built on **React** and **Express.js**, with **MongoDB** for data storage. An ingredient analysis pipeline powered by **Natural Language Processing (NLP)** handles ingredient extraction and matching. The project is guided by **Dr. Ganesh Bagler** at **Cosylab, IIIT Delhi**, as part of the **Bachelor Thesis Project (BTP)**.

## Poster
![image](https://github.com/user-attachments/assets/f32eb6d9-cd94-4e09-bc35-22d68087d144)

## Frontend: React Components

### Login.js
**Purpose**: Handles user authentication via Google OAuth.

**Key Features**:
- Redirects users to the Google login page at `/ttc/auth/google/callback`.
- Includes a legal notice regarding Google’s terms and privacy policies.
- Features a sleek animated title using the `animate-gradient-text` library.

### Home.js
**Purpose**: Serves as the landing page.

**Key Features**:
- Displays a simple title, “Home Page,” with potential for future expansion to include project details or navigation elements.

### Headers.js
**Purpose**: Provides the navigation bar for the application.

**Key Features**:
- Displays user profile details and a dropdown menu with links to **Profile**, **About**, and **Logout** sections.
- Logout functionality calls `/ttc/logout`, terminating the user session.

### Error.js
**Purpose**: Handles undefined routes.

**Key Features**:
- Includes a “Back to Home” button that navigates users to the homepage (`/`).

### RandomRecipeComponent.js
**Purpose**: Displays a random recipe for evaluation.

**Key Features**:
- Authenticated users can view recipe ingredients and instructions.
- Provides a **Likert scale** to classify the recipe as real, fake, or skipped.
- Supports dual ingredient formats (list and checklist) for a clear, interactive user experience.

### About.js
**Purpose**: Introduces users to the TTChef project.

**Key Features**:
- Describes the project concept and mentions the backend engine, **Ratatouille**.
- Includes a “Continue” button redirecting to `/dashboard`.

### OccupationAdder.jsx
**Purpose**: Allows users to set their chef expertise level.

**Key Features**:
- Fetches user data and submits it to `/ttc/occupation_adder` for processing.
- Redirects to `/dashboard` after submission.

### Stats.jsx
**Purpose**: Displays real-time evaluation statistics.

**Key Features**:
- Shows a pie chart of real vs. fake recipe classification ratios.
- Displays a star rating for each evaluated recipe.

### StatsPage.js
**Purpose**: Admin dashboard for viewing confusion matrices and aggregated statistics.

**Key Features**:
- Fetches and aggregates data from the confusion matrix.
- Displays comprehensive stats for recipe evaluation analysis.

### RecipeDetails.js
**Purpose**: Shows detailed information for a selected recipe.

**Key Features**:
- Fetches recipe details by unique ID from `/ttc/api/recipe/:recipeId`.
- Displays ingredients and instructions in both list and table formats.

## Backend: HTTP Routes

### A. Static Asset & SPA Fallback Routes
| Method | Path               | Purpose                                      |
|--------|--------------------|----------------------------------------------|
| GET    | `/ttc/static/*`    | Serves static assets (JS, CSS, images).      |
| GET    | `/ttc/*`           | Serves `index.html` for React Router routes. |

### B. Authentication & Session Management
| Method | Path                          | Purpose                                                                 |
|--------|-------------------------------|-------------------------------------------------------------------------|
| GET    | `/ttc/auth/google`            | Redirects to Google OAuth consent screen.                               |
| GET    | `/ttc/auth/google/callback`   | Authenticates user, creates/finds user in DB, redirects based on status.|
| GET    | `/ttc/login/success`          | Returns user login status and data if authenticated.                    |
| GET    | `/ttc/logout`                 | Logs out user and redirects to login page.                             |

### C. User Profile Management
| Method | Path                        | Purpose                                              |
|--------|-----------------------------|------------------------------------------------------|
| POST   | `/ttc/occupation_adder`     | Sets user’s chef occupation or expertise level.       |
| GET    | `/ttc/login/userdata`       | Fetches full user data for the active session.        |

### D. Recipe-Judgment API
| Method | Path                         | Purpose                                                  |
|--------|------------------------------|----------------------------------------------------------|
| GET    | `/ttc/api/random-recipe`     | Returns a random unevaluated recipe for the user.         |
| POST   | `/ttc/api/evaluate-recipe`   | Records user’s judgment (real, fake, or skipped).         |
| GET    | `/ttc/api/recipe/:recipeId`  | Fetches full details of a recipe by its unique ID.        |

### E. Analytics & Aggregation Endpoints
| Method | Path                               | Purpose                                                       |
|--------|------------------------------------|---------------------------------------------------------------|
| GET    | `/ttc/api/fetch-confusion-matrix`  | Returns aggregated confusion matrix data for evaluation performance. |
| GET    | `/ttc/api/fetch-intersections`     | Finds recipes with unanimous classification (real or fake).    |
| GET    | `/ttc/api/fetch-unions`            | Collects unique recipe IDs judged across all categories.       |

### Middleware
- **cors()**: Handles cross-origin requests between frontend and backend.
- **ensureHttps**: Redirects HTTP requests to HTTPS.
- **express.json()**: Parses incoming JSON request bodies.
- **Session & Passport**: Manages user authentication and session handling.

## Data-Driven Ingredient Analysis Pipeline
The ingredient analysis pipeline processes large-scale recipe data and evaluates human evaluator performance. Key steps include:

### 1. Data Ingestion & Consolidation
**MongoDB Setup**:
- Connected to **Atlas clusters** housing the `recipegs` and `ttc` collections.
- Consolidated **12 CSV files** (~120,000 records) into the `ttc` collection, removing redundant identifiers.

**Data Validation**:
- Ensured recipes had valid titles, ingredient lists, and instructions.
- Removed duplicates by comparing titles, ingredients, and instructions.

### 2. Ingredient Extraction & Matching
**Extraction**:
- Used **SpaCy’s NER and POS tagging** with **regex** to extract ingredient names.
- Cleaned data by removing common stop-words and descriptors.

**Matching & Statistics**:
- Grouped ingredients by recipe ID and computed ingredient overlaps.
- Generated `combined_stats.csv` with statistics like ingredient count and overlap percentages.

**Visualization**:
- Produced pie charts showing ingredient coverage and alignment across the recipe corpus.

### 3. Filtering & Cleaning the Corpus
**Low-Coverage Recipe Removal**:
- Removed recipes with low ingredient overlap (≤ 15%).

**Post-Deletion Validation**:
- Validated the integrity of the remaining dataset, ensuring no violations.

### 4. Human Evaluator Performance Analysis
**Session Data Extraction**:
- Queried the `users` collection for session data, capturing judged recipes and session duration.

**Time-Based Filtering**:
- Applied thresholds (10s, 20s, 30s) to filter out fast sessions, improving evaluation quality.

**Confusion Matrices & F1 Score**:
- Computed **precision**, **recall**, and **F1 scores** for real and fake recipes at different thresholds, showing improved evaluator accuracy.

### 5. Advanced Chef-Level Filtering
**Per-Chef Metrics**:
- Calculated each chef’s **TP**, **FP**, **TN**, and **FN**, deriving metrics like **F1 score** and evaluation count.

**Basic Exclusion Criteria**:
- Excluded chefs with poor F1 scores or skewed classifications (e.g., real vs. fake recipes).

**Statistical Outlier Removal**:
- Removed poorly performing chefs based on statistical outliers (mean and standard deviation).

## Key Insights & Results
- **Data Quality**: Pruning low-coverage recipes improved corpus quality, reducing the dataset to ~111,000 recipes.
- **Evaluator Reliability**: A 20–30s minimum evaluation time increased **Macro F1** from **0.75** to **0.81**.
- **Chef Filtering**: A `min_F1` threshold of **0.40** balanced evaluator quality and sample size.
- **Pipeline Integrity**: Validation checks confirmed robust extraction, matching, and filtering processes.

## Future Directions
- **Model Training**: Train generative models to predict ingredient lists and instructions, evaluating integration with **F1 scores**.
- **Enhanced Matching**: Use **lemmatization** and **fuzzy matching** to handle ingredient variations.
- **Evaluator Training Loop**: Provide feedback to borderline chefs to improve evaluations.
- **Longitudinal Studies**: Monitor evaluator performance over time to study learning and drift.

## Conclusion
The TTChef project provides a comprehensive approach to recipe evaluation through integrated frontend UI components, backend APIs, and an advanced ingredient analysis pipeline. From data ingestion to human evaluator filtering, each step ensures quality and reliability. Future work will leverage the clean corpus to train advanced models, refine evaluator performance, and explore longitudinal trends in human judgment.
