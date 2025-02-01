import React, { useState } from 'react';
import './StatsPage.css';

import  { useEffect} from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { NavLink } from "react-router-dom";


import { useNavigate } from 'react-router-dom';

const StatsPage = () => {
    const [confusionMatrix, setConfusionMatrix] = useState(null);
    const [intersections, setIntersections] = useState(null);
    const [unions, setUnions] = useState(null); // State for union data
    const [userdata, setUserdata] = useState({});
    const navigate = useNavigate();

    // List of authorized Google IDs
    const authorizedUsers = ['108129870778035595919', '114439477008986381098', '102906129011434823565', '108247700055597509497']; // Add Google IDs here

    // Fetch user data
    const getUser = async () => {
        try {
            const response = await axios.get("/ttc/login/success", { withCredentials: true });
            setUserdata(response.data.user);

            // Check if user is authorized
            if (!authorizedUsers.includes(response.data.user.googleId)) {
                // If not authorized, navigate to the login page
                navigate('/login');
            }
        } catch (error) {
            console.log("Error fetching user data:", error);
            navigate('/login'); // In case of an error, navigate to login page
        }
    };

    // useEffect to fetch user data on component mount
    useEffect(() => {
        getUser();
    }, []);




    // Function to fetch the latest confusion matrix data
    const fetchFreshData = async () => {
        try {
            const response = await fetch('/ttc/api/fetch-confusion-matrix');
            const data = await response.json();
            setConfusionMatrix(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    // Function to fetch intersections across all users
    const fetchIntersections = async () => {
        try {
            const response = await fetch('/ttc/api/fetch-intersections');
            const data = await response.json();
            setIntersections(data);
        } catch (error) {
            console.error('Error fetching intersection data:', error);
        }
    };

    // Function to fetch unions across all users
    const fetchUnions = async () => {
        try {
            const response = await fetch('/ttc/api/fetch-unions');
            const data = await response.json();
            setUnions(data);
        } catch (error) {
            console.error('Error fetching union data:', error);
        }
    };

    return (
        <div className="stats-container">
            <h11>Statistics</h11>
            <p1>Click the button to get the latest confusion matrix data.</p1>
            <button1 onClick={fetchFreshData}>Run</button1>
            <button1 onClick={fetchIntersections}>Fetch Intersections</button1>
            <button1 onClick={fetchUnions}>Fetch Unions</button1>

            {confusionMatrix && (
                <div>
                    <h2>Confusion Matrix</h2>
                    <table className="matrix-table">
                        <thead>
                            <tr>
                                <th>Actual / Predicted</th>
                                <th>Fake</th>
                                <th>Real</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Fake</td>
                                <td>{confusionMatrix.FF}</td>
                                <td>{confusionMatrix.FR}</td>
                            </tr>
                            <tr>
                                <td>Real</td>
                                <td>{confusionMatrix.RF}</td>
                                <td>{confusionMatrix.RR}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            )}

            {intersections && (
                <div>
                    <h2>Intersections</h2>
                    <table className="matrix-table">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Values</th>
                            </tr>
                        </thead>
                        <tbody>
  {['FF', 'RF', 'FR', 'RR'].map(type => (
    <tr key={type}>
      <td>{type}</td>
      <td>
        {Array.isArray(intersections[type]) && intersections[type].length > 0 
          ? intersections[type].map((recipeId, index) => (
              <span key={recipeId}>
                <a href={`/ttc/recipe/${recipeId}`} target="_blank" rel="noopener noreferrer">
                  {recipeId}
                </a>
                {index < intersections[type].length - 1 && ', '}
              </span>
            ))
          : 'No intersection found'}
      </td>
    </tr>
  ))}
</tbody>



                    </table>
                </div>
            )}

            {unions && (
                <div>
                    <h2>Unions</h2>
                    <table className="matrix-table">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Values</th>
                            </tr>
                        </thead>
                        <tbody>
  {['FF', 'RF', 'FR', 'RR'].map(type => (
    <tr key={type}>
      <td>{type}</td>
      <td>
        {Array.isArray(unions[type]) && unions[type].length > 0 
          ? unions[type].map((recipeId, index) => (
              <span key={recipeId}>
                <a href={`/ttc/recipe/${recipeId}`} target="_blank" rel="noopener noreferrer">
                  {recipeId}
                </a>
                {index < unions[type].length - 1 && ', '}
              </span>
            ))
          : 'No union found'}
      </td>
    </tr>
  ))}
</tbody>

                    </table>
                </div>
            )}
        </div>
    );
};

export default StatsPage;
