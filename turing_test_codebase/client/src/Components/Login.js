import React from 'react';
import './login.css'; // Make sure to adjust your CSS file accordingly




const Login = () => {
    const loginWithGoogle = () => {
        window.open("/ttc/auth/google/callback", "_self");
    };

    return (
        <div className="main_box">
            <div className="animate-gradient-text">
                <h1 style={{ padding: '20px' }}>TTChef</h1>
            </div>
            <h5>Turing test for Chef</h5>
            <div className="g_body">
                <button className="g-button" onClick={loginWithGoogle}>
                    <img className="g-logo" src="./1298745_google_brand_branding_logo_network_icon.png" alt="Google Logo" />
                    <p className="g-text">Continue with Google</p>
                </button>
            </div>
            <p style={{ fontSize: 'small' }}>
                By continuing, you agree to google <br />
                <span style={{ color: '#5162FF', fontSize: 'small' }}>Terms of Use</span> and <span style={{ color: '#5162FF', fontSize: 'small' }}>Privacy Policy.</span>
            </p>
        </div>
    );
};

export default Login;


