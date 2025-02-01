import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './stats.css'; 
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { useNavigate } from 'react-router-dom';



const Stats = () => {
  const [userdata, setUserdata] = useState({
    RF: [],
    RR: [],
    FR: [],
    FF: [],
    displayName: '',
    recipe_evaluated: [],
  });
  const [starComment, setStarComment] = useState('');
  const [starCount, setStarCount] = useState(0); // New state for star count

  const colors = [
    'url(#grad1)', 
    'url(#grad2)', 
    'url(#grad3)', 
    'url(#grad4)', 
    'url(#grad5)', 
    'url(#grad6)'
  ];

  const navigate = useNavigate();

  const authorizedUsers = ['108129870778035595919', '114439477008986381098', '102906129011434823565', '108247700055597509497']; // Add Google IDs here


  const getUser = async () => {
    try {
      const response = await axios.get("/ttc/login/userdata", { withCredentials: true });
      setUserdata({
        RF: response.data.user.RF || [],
        RR: response.data.user.RR || [],
        FR: response.data.user.FR || [],
        FF: response.data.user.FF || [],
        displayName: response.data.user.displayName || '',
        recipe_evaluated: response.data.user.recipe_evaluated || [],
        googleId: response.data.user.googleId || '', // Set googleId here
      });
    } catch (error) {
      console.log("error", error);
    }
  };

  useEffect(() => {
    getUser();
  }, []);

  useEffect(() => {
    if (userdata.recipe_evaluated.length) {
      calculateStars();
    }
  }, [userdata]);

  const calculateStars = () => {
    const total = userdata.recipe_evaluated.length;

    if (total >= 300) {
      setStarComment('You are a 5 star rated user. Keep it up!');
      setStarCount(5);
    } else if (total >= 100) {
      setStarComment('You are a 4 star rated user. Keep it up!');
      setStarCount(4);
    } else if (total >= 60) {
      setStarComment('You are a 3 star rated user. Keep it up!');
      setStarCount(3);
    } else if (total >= 30) {
      setStarComment('You are a 2 star rated user. Keep it up!');
      setStarCount(2);
    } else if (total >= 10) {
      setStarComment('You are a 1 star rated user. Keep it up!');
      setStarCount(1);
    } else {
      const diff = 5 - total;
      setStarComment(`Evaluate ${diff} more recipes to get your first star!`);
      setStarCount(0); // No stars if less than 5 recipes
    }
  };

  const data = [
    { name: 'Real', value: userdata.RF.length + userdata.RR.length },
    { name: 'Fake', value: userdata.FF.length + userdata.FR.length }
  ];

  const totalRecipes = userdata.recipe_evaluated.length;

  return (
    <div id="statbox">
      {authorizedUsers.includes(userdata.googleId) && (
        <button 
          className="detailed-stats-btn" 
          style={{
            position: 'relative',
            top: 'auto',
            left: 'auto',
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
          onClick={() => {
            // Logic to get detailed stats, like opening a modal or navigating to another page
         
            navigate('/stats');
          }}
        >
          Get Detailed Stats
        </button>
      )}

      <div className="animate-gradient-text">
        <h1><i>Hi {userdata.displayName}, here are your stats</i></h1>
      </div>

      {totalRecipes > 0 ? (
        <div className="chart-container">
          <svg width={0} height={0}>
            <defs>
              {/* Gradients (Optional) */}
              <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#ff7e5f', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#feb47b', stopOpacity: 1 }} />
              </linearGradient>
              <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#6a11cb', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#2575fc', stopOpacity: 1 }} />
              </linearGradient>
              <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#f7f8f8', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#e9e9e9', stopOpacity: 1 }} />
              </linearGradient>
              <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#00c6ff', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#0072ff', stopOpacity: 1 }} />
              </linearGradient>
              <linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#ff416c', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#ff4b2b', stopOpacity: 1 }} />
              </linearGradient>
              <linearGradient id="grad6" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{ stopColor: '#a8e063', stopOpacity: 1 }} />
                <stop offset="100%" style={{ stopColor: '#56ab2f', stopOpacity: 1 }} />
              </linearGradient>
            </defs>
          </svg>
          <PieChart width={600} height={400}>
            <Pie
              data={data}
              cx={300}
              cy={200}
              labelLine={false}
              outerRadius={150}
              fill="#8884d8"
              dataKey="value"
              animationBegin={0}
              animationDuration={800}
              animationEasing="ease-in-out"
              isAnimationActive={true}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => [`${value} recipes`, '']}/>
            <Legend layout="vertical" align="right" verticalAlign="middle" />
          </PieChart>
        </div>
      ) : (
        <div id="chartdiv" style={{ height: '0px' }}>No evaluations yet!</div>
      )}

      <h1 id="star_review">{starComment}</h1>
      <div className="rating-stars">
        {[...Array(starCount)].map((_, index) => (
          <span
            className="star-icon"
            key={index}
            style={{
              color: '#F7A115', // Plain golden color for the stars
              fontSize: '60px', // Keeping the size for desktop
            }}
          >
            ★
          </span>
        ))}
      </div>
    </div>
  );
};

export default Stats;
