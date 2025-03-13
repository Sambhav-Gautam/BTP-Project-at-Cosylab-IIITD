// export default OccupationAdder;
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./OccupationAdder.css"; // Assuming you have this CSS file
import { useNavigate } from "react-router-dom";

const OccupationAdder = ({ name }) => {
  const [occupation, setOccupation] = useState("Amateur");
  const [userdata, setUserdata] = useState({});
  const navigate = useNavigate();  // Initialize navigate

  // Function to fetch user data from the backend
  const getUser = async () => {
    try {
      const response = await axios.get("/ttc/login/success", { withCredentials: true });
      setUserdata(response.data.user);
    } catch (error) {
      console.log("error", error);
    }
  }

  // useEffect to fetch user data on component mount
  useEffect(() => {
    getUser();
  }, []); // Empty array means this runs only once on mount

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/ttc/occupation_adder", {
        googleId: userdata.googleId, // Assuming user is fetched successfully
        occupation: occupation
      });
      console.log("Occupation updated successfully:", response.data);
      
      // Redirect to dashboard after occupation is added
      navigate("/dashboard");  // This will navigate to the dashboard route
    } catch (error) {
      console.error("Error occurred while updating occupation", error);
    }
  };

  return (
    <div className="main_box">
      <div className="upper_content">
        <h1>Hi {name}!</h1>
        <div className="animate-gradient-text" style={{ fontFamily: "'Berkshire Swash'", padding: '10px' }}>
          <h1>TTChef</h1>
        </div>
        <h2>How do you identify yourself as a Chef?</h2>
      </div>

      <form onSubmit={handleSubmit}>
        <section>
          <div>
            <input
              type="radio"
              id="control_01"
              name="select"
              value="Professional"
              checked={occupation === "Professional"}
              onChange={(e) => setOccupation(e.target.value)}
            />
            <label htmlFor="control_01">
              <h2>Professional</h2>
            </label>
          </div>
          <div>
            <input
              type="radio"
              id="control_02"
              name="select"
              value="Expert"
              checked={occupation === "Expert"}
              onChange={(e) => setOccupation(e.target.value)}
            />
            <label htmlFor="control_02">
              <h2>Expert</h2>
            </label>
          </div>
          <div>
            <input
              type="radio"
              id="control_03"
              name="select"
              value="Amateur"
              checked={occupation === "Amateur"}
              onChange={(e) => setOccupation(e.target.value)}
            />
            <label htmlFor="control_03">
              <h2>Amateur</h2>
            </label>
          </div>
        </section>
        <br />
        <br />
        <br />
        <button id="submit_ocp" type="submit" >
          Register
        </button>
      </form>
    </div>
  );
};

export default OccupationAdder;
