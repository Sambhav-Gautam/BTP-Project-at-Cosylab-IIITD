import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './randi.css';

const RandomRecipeComponent = () => {
    const [recipe, setRecipe] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userdata, setUserdata] = useState({});
    const [evaluation, setEvaluation] = useState(null); // To store the evaluation string
    const [activeButton, setActiveButton] = useState(null); // To track the active button

    // Function to fetch user data from the backend
    const getUser = async () => {
        try {
            const response = await axios.get("/ttc/login/success", { withCredentials: true });
            setUserdata(response.data.user); // Set user data here
        } catch (error) {
            console.log("Error fetching user data", error);
        }
    };

    // Fetch random recipe once user data is available
    const fetchRandomRecipe = async () => {
        try {
            if (userdata) {
                const userId = userdata._id;
                const response = await axios.get("/ttc/api/random-recipe", {
                    userId,
                }, { withCredentials: true });
                setRecipe(response.data);
            }
        } catch (err) {
            setError(err.response?.data?.message || "Error fetching recipe");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            await getUser();
        };
        fetchData();
    }, []); // Runs once on mount

    useEffect(() => {
        const fetchData = async () => {
            await fetchRandomRecipe();
        };
        fetchData();
    }, [userdata]); // Runs once user data is fetched

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    const evaluateRecipe = async (evaluation) => {
        const recipeId = recipe._id;
        const userId = userdata._id;
        try {
            const response = await axios.post("/ttc/api/evaluate-recipe", {
                userId,
                recipeId,
                evaluation
            }, { withCredentials: true });

            console.log(response.data.message);
            window.location.reload();
        } catch (error) {
            console.error("Error evaluating recipe:", error.response?.data?.message || error.message);
        }
    };

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
                            <p><i>Ingredients</i></p> {/* Keeping this separate for styling */}
                        </b>
                        <div className="ingredients-container">
                            <table id="ing1" >
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
                            <ul id="ing2" >
                                {ingredients.map((ingredient, index) => (
                                    <li key={index} style={{ listStyle: 'none', padding: 0 }}>✅ {ingredient}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>


                <div className="instructions">
                    <b><i>Instructions</i></b> {/* Ensure this is bold and the same size */}
                    <ul>
                        {instructions.map((instruction, index) => (
                            <li key={index}><b>🥣 {instruction.charAt(0).toUpperCase() + instruction.slice(1)}</b></li>
                        ))}
                    </ul>
                </div>
            </div>

            <div className="bottom_box" id="inner_fixed">
                <div className="evaluate">
                    <div className="evaluate_upper">
                        <h1>Is this recipe fake or real?</h1>
                        <ul className="progressbar">
                            <li
                                id="bt0"
                                className={`blurry ${activeButton === 0 ? 'active' : ''}`}
                                onClick={() => {
                                    setEvaluation('fake');
                                    setActiveButton(0); // Set the active button
                                }}
                            ></li>
                            <li
                                id="bt1"
                                className={`blurry ${activeButton === 1 ? 'active' : ''}`}
                                onClick={() => {
                                    setEvaluation('fake');
                                    setActiveButton(1); // Set the active button
                                }}
                            ></li>
                            <li
                                id="bt2"
                                className={`blurry ${activeButton === 2 ? 'active' : ''}`}
                                onClick={() => {
                                    setEvaluation('fake');
                                    setActiveButton(2); // Set the active button
                                }}
                            ></li>
                            <li
                                id="bt3"
                                className={`blurry ${activeButton === 3 ? 'active' : ''}`}
                                onClick={() => {
                                    setEvaluation('real');
                                    setActiveButton(3); // Set the active button
                                }}
                            ></li>
                            <li
                                id="bt4"
                                className={`blurry ${activeButton === 4 ? 'active' : ''}`}
                                onClick={() => {
                                    setEvaluation('real');
                                    setActiveButton(4); // Set the active button
                                }}
                            ></li>
                            <li
                                id="bt5"
                                className={`blurry ${activeButton === 5 ? 'active' : ''}`}
                                onClick={() => {
                                    setEvaluation('real');
                                    setActiveButton(5); // Set the active button
                                }}
                            ></li>
                        </ul>
                        <ul className="bts" style={{ padding: 0 }}>
                            <li>
                                <button className="sbtn" id="sbt" onClick={() => {
                                    if (evaluation) {
                                        evaluateRecipe(evaluation);
                                    }
                                }}>Submit</button>
                            </li>
                            <li>
                                <button className="sbtn" id="skp" onClick={() => evaluateRecipe('skip')}>Skip</button>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RandomRecipeComponent;
