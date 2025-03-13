import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import './randi.css';

const RecipeDetails = () => {
  const { recipeId } = useParams();
  const [recipe, setRecipe] = useState(null); // Initialize as null for loading state
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        const response = await axios.get(`/ttc/api/recipe/${recipeId}`, { withCredentials: true });
        console.log('Fetched recipe:', response.data); // Log the response data
        setRecipe(response.data);
      } catch (error) {
        console.error('Error fetching recipe details:', error);
        setError('Error fetching recipe details. Please try again later.'); // Set error message
      }
    };

    fetchRecipe();
  }, [recipeId]);

  if (error) {
    return <div>{error}</div>; // Show error message
  }

  if (!recipe || !recipe.title) {
    return <div>Loading recipe details...</div>; // Check for recipe title
  }

  // Split ingredients and instructions
  const ingredients = recipe.ingredients?.split('|').map(ingredient => ingredient.trim()) || [];
  const instructions = recipe.instructions?.split('.').map(instruction => instruction.trim()).filter(instruction => instruction) || [];

  return (
    <div id="outer">
      <div id="inner_remaining">
        <div className="content">
          <div className="recp_name">
            <b>
              <p>🍽️ {recipe.title}</p>
              <p><i>Ingredients</i></p>
            </b>
            <div className="ingredients-container">
              <table id="ing1">
                {ingredients.map((ingredient, index) => (
                  index % 3 === 0 && (
                    <tr key={index}>
                      {ingredients.slice(index, index + 3).map((ing, i) => (
                        <td key={i}>{ing}</td>
                      ))}
                    </tr>
                  )
                ))}
              </table>
              <ul id="ing2">
                {ingredients.map((ingredient, index) => (
                  <li key={index} style={{ listStyle: 'none', padding: 0 }}>✅ {ingredient}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="instructions">
          <b><i>Instructions</i></b>
          <ul>
            {instructions.map((instruction, index) => (
              <li key={index}><b>🥣 {instruction.charAt(0).toUpperCase() + instruction.slice(1)}</b></li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetails;
