import React, { useEffect, useState } from 'react';
import "./header.css";
import { NavLink } from "react-router-dom";
import axios from "axios";

const Headers = () => {
    const [userdata, setUserdata] = useState({});
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [profileImage, setProfileImage] = useState("profile.png");
    const [showProfileText, setShowProfileText] = useState(false); // Track if all image attempts failed

    const getUser = async () => {
        if (Object.keys(userdata).length === 0) { // Fetch user only if data is empty
            try {
                const response = await axios.get("/ttc/login/success", { withCredentials: true });
                setUserdata(response.data.user);
                setProfileImage(response.data.user?.image || "profile.png");
            } catch (error) {
                console.log("Error fetching user data", error);
            }
        }
    };

    const logout = () => {
        window.open("/ttc/logout", "_self");
    };

    useEffect(() => {
        getUser();
    }, []);

    const toggleDropdown = () => {
        setDropdownOpen(prevState => !prevState);
    };

    const handleClickOutside = (event) => {
        if (event.target.closest('.dropdown-container') === null) {
            setDropdownOpen(false);
        }
    };

    useEffect(() => {
        document.addEventListener('click', handleClickOutside);
        return () => {
            document.removeEventListener('click', handleClickOutside);
        };
    }, []);

    return (
        <header>
            <nav>
                <div className="left">
                    <NavLink to="/dashboard" className="logo-link">
                        <h1>TTChef</h1>
                    </NavLink>
                </div>
                <div className="right">
                    <ul>
                        {Object.keys(userdata).length > 0 ? (
                            <li className="dropdown-container">
                                {!showProfileText ? (
                                    <img
                                        src={profileImage}
                                        alt="Profile"
                                        style={{ width: "60px", height: "60px", borderRadius: "50%", cursor: "pointer" }}
                                        onClick={toggleDropdown}
                                        onError={() => {
                                            if (profileImage !== "profile.png") {
                                                setProfileImage("profile.png"); // Try fallback image
                                            } else {
                                                setShowProfileText(true); // Show text if both images fail
                                            }
                                        }}
                                    />
                                ) : (
                                    <span
                                        style={{ cursor: "pointer", fontSize: "1rem", fontWeight: "bold" }}
                                        onClick={toggleDropdown}
                                    >
                                        Profile
                                    </span>
                                )}
                                {dropdownOpen && (
                                    <ul className="dropdown">
                                        <li>
                                            <NavLink to="/profile">Profile</NavLink>
                                        </li>
                                        <li>
                                            <NavLink to="/about">About</NavLink>
                                        </li>
                                        <li>
                                            <NavLink to="/login" onClick={logout}>Logout</NavLink>
                                        </li>
                                    </ul>
                                )}
                            </li>
                        ) : (
                            <li>
                                <NavLink to="/login">Login</NavLink>
                            </li>
                        )}
                    </ul>
                </div>
            </nav>
        </header>
    );
};

export default Headers;
