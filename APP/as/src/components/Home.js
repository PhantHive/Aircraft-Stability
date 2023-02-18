import React from 'react';
import '../styles/Home.css';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function Home() {

    const navigate = useNavigate();

    const handleNavigation = (e) => {
        e.preventDefault();
        navigate('/longitudinal');
    };

    return (
        <div className="menu">
            <h1>Select an option:</h1>
            <ul>
                <li onClick={handleNavigation}><Link to="/longitudinal" style={{ textDecoration: 'inherit', color: 'inherit' }}>Longitudinal</Link></li>
                <li>Lateral</li>
            </ul>
        </div>
    );
}

export default Home;
