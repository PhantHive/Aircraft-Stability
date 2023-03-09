import React from 'react';
import '../styles/Home.css';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function Home() {

    const navigate = useNavigate();

    const handleNavigation = (e) => {
        e.preventDefault();
        // check if the link is to the longitudinal page
        if (e.target.innerText === 'Longitudinal') {
            navigate('/longitudinal');
        }
        // check if the link is to the lateral page
        else if (e.target.innerText === 'Lateral') {
            navigate('/lateral');
        }
    };

    return (
        <div className="menu">
            <h1>Select an option:</h1>
            <ul>
                <li onClick={handleNavigation}><Link to="/longitudinal" style={{ textDecoration: 'inherit', color: 'inherit' }}>Longitudinal</Link></li>
                <li onClick={handleNavigation}><Link to="/lateral" style={{ textDecoration: 'inherit', color: 'inherit' }}>Lateral</Link></li>
            </ul>
        </div>
    );
}

export default Home;
