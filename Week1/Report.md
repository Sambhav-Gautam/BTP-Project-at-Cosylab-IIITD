**Week 1 BTP Report**

**Project Title:** Data-Driven Ingredient Analysis for Recipes

**Student Name:** Sambhav Gautam and Sambhav Singh 
**Supervisor:** Dr. Ganesh Bagler  
**Lab:** Cosylab, IIIT Delhi  

**Objective for Week 1:**  
To initiate the project by developing a pipeline for extracting, cleaning, and analyzing ingredient data from recipe datasets stored in MongoDB. The primary aim was to quantify the relationship between ingredients listed in recipes and their presence in the corresponding recipe instructions.

---

### **Tasks Undertaken**

#### **1. Setting up the MongoDB Connection:**
- Established a successful connection to the MongoDB cluster containing the `recipegs` collection.
- Verified access to the `trying` database and performed initial data retrieval tests.

#### **2. Ingredient Extraction Pipeline:**
- Designed a pipeline using Python, SpaCy, and regex for extracting and cleaning ingredient names from recipe data.
- Key features of the pipeline include:
  - Removal of irrelevant words and phrases (e.g., "cups," "optional," "sliced") using a predefined stop-word list.
  - Application of SpaCy’s Named Entity Recognition (NER) and Part-of-Speech (POS) tagging to identify and filter ingredient names.
  - Storing unique ingredient-recipe pairs in a structured format for further analysis.
- Results were exported to a CSV file named `extracted_ingredients.csv`.

#### **3. Grouping and Aggregation of Ingredients:**
- Grouped extracted ingredients by recipe ID using Pandas.
- Saved the grouped data to `output.csv`, enabling a clear structure of recipe IDs and their corresponding ingredient lists.

#### **4. Quantifying Ingredient Presence in Instructions:**
- Processed `output.csv` to compare listed ingredients with the text in recipe instructions.
- Counted the occurrence of each ingredient within instructions and calculated the ratio of ingredients mentioned.
- Saved the results as `stats.csv`.

#### **5. Combining and Analyzing Data:**
- Merged data from `output.csv` and `stats.csv` to create `combined_stats.csv`.
- This file contains key metrics such as the total number of ingredients per recipe, the number of ingredients found in instructions, and the percentage of overlap.

#### **6. Visualization - Pie Chart of Ingredient Distribution:**
- Categorized recipes based on the percentage of ingredients found in instructions.
- Created bins (e.g., `== 0`, `> 0 and <= 5`, `> 5 and <= 10`, etc.) for detailed segmentation.
- Visualized the distribution using a pie chart with distinct color segments and percentage annotations for each category.

---

### **Final Results**
The pie chart generated serves as the final visualization for Week 1. It shows a detailed distribution of the percentage of ingredients mentioned in the instructions across all recipes in the dataset. The chart highlights the variability in ingredient-instruction alignment, with categories ranging from `== 0%` to `> 95%` overlap.

![Detailed Percentage Distribution of Ingredients Found in Instructions](https://github.com/Sambhav-Gautam/BTP-Project-at-Cosylab-IIITD/blob/main/Week1/Figure_1.png)

---

### **Key Learnings and Challenges**
- **Learnings:**
  - Developed a deeper understanding of NLP techniques such as NER and POS tagging for processing recipe data.
  - Gained proficiency in using Python libraries like Pandas, Matplotlib, and SpaCy for data processing and visualization.
  - Explored techniques for integrating MongoDB with Python to handle large datasets efficiently.

- **Challenges:**
  - Handling noisy and inconsistent data in ingredient lists (e.g., typos, varying units, and descriptors).
  - Ensuring efficient processing of large datasets, especially when extracting named entities and matching text.

---

### **Future Work**
- Optimize the ingredient extraction pipeline by training a custom NER model for recipe-specific terminology.
- Extend the analysis to include other recipe attributes, such as cooking time or cuisine type.
- Investigate correlations between ingredient-instruction alignment and recipe popularity or ratings.
- Build interactive visualizations for more intuitive data exploration.

---

**Conclusion:**
The work completed in Week 1 has successfully laid the foundation for the project. The pipeline is capable of extracting, cleaning, and analyzing ingredient data, providing valuable insights into how well recipe instructions incorporate listed ingredients. The generated visualization offers a clear representation of the current findings and sets the stage for deeper analysis in the coming weeks.
