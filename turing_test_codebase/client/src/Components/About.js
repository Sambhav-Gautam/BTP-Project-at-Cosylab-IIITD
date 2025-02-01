// src/Components/About.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './About.css'; // Ensure this CSS file is created

const About = () => {
    const navigate = useNavigate(); // Initialize the useNavigate hook

    const handleContinue = () => {
        // Navigate to the dashboard
        navigate('/dashboard');
    };

    return (
        <div className="about-container">
            <div className="animate-gradient-text">
                <h1>TTChef</h1>
            </div>
            <div className="about">
                <p>'Can machines cook?'</p>
                <p>'Can machines think like a Chef?'</p>
                <p>
                    Can they create novel recipes? Or recipe instructions that can fool a Chef into thinking that a fake (computer-generated) recipe is real.
                </p>
                <p>
                    We have developed (and constantly improving) <a href='https://cosylab.iiitd.edu.in/ratatouille2/'>Ratatouille</a>, an algorithm for generating novel recipes. Trained with a structured corpus of 118,000+ recipes, Ratatouille is our tribute to cumulative culinary intuition accumulated over millennia by cultures across the globe.
                </p>
                <p>
                    With the 'Turing Test for Chef,' we are building on Alan Turing's inquiry into human intelligence and machines' ability to imitate.
                </p>
                <p>Let the imitation game begin!</p>
            </div>
            <div className="continue">
                <button id="continue_main" onClick={handleContinue}>Continue</button>
            </div>
        </div>
    );
};

export default About;
