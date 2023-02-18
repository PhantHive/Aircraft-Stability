import './App.css';
import Home from './components/Home.js';
import Longitudinal from './components/Longitudinal.js';
import {HashRouter as Router, Route, Routes} from 'react-router-dom';

function App() {
    return (
        <div className="App">
            <Router>
                <Routes>
                      <Route exact path="/" element={<Home />} />
                      <Route path="/longitudinal" element={<Longitudinal />} />
                </Routes>
            </Router>
        </div>
  );
}

export default App;
