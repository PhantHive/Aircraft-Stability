import './App.css';

import {HashRouter as Router, Route, Routes} from 'react-router-dom';

import Home from './components/Home.js';
import Lateral from "./components/Lateral";
import Longitudinal from './components/Longitudinal.js';

function App() {
  return (
      <div className = "App"><Router><Routes>
      <Route exact path = "/" element =
       { <Home /> } />
                      <Route path="/longitudinal
                     " element={<Longitudinal />} />
       < Route path =
           "/lateral" element = { <Lateral /> } />
                </Routes>
      </Router>
        </div>);
}

export default App;
