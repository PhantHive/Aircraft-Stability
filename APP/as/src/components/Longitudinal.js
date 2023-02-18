import React, { useState } from 'react';
import '../styles/Longitudinal.css';
import FileSelector from './FileSelector.js';

function Longitudinal() {
    const [file, setFile] = useState(null);
    const [calculationResult, setCalculationResult] = useState(null);

    const handleFileChange = (selectedFile) => {
        setFile(selectedFile);
    };


    const handleCalculate = () => {
        // check if file is null
        if (!file) {
            alert('Please select a file');
            return;
        }
        // check if file is JSON
        if (file.type !== 'application/json') {
            alert('Please select a JSON file');
            return;
        }
        // Perform calculation here and set the result in the calculationResult state
        console.log('Calculating using file:', file.name);
    };

    const handleDownload = () => {
        // Download data here
        console.log('Downloading data');
    };

    return (
        <div className="longitudinal-container">
            <h1 className="longitudinal-title">Longitudinal stability calculation</h1>
            <h2 className="select">Select a JSON file containing plane data (follow README.md)</h2>
            <div className="longitudinal-file-selector">
                <FileSelector key={file} label="Flight Data" onFileSelect={handleFileChange} />
                <FileSelector key={file} label="Derivatives Data" onFileSelect={handleFileChange} />
            </div>
            <div className="longitudinal-calculation-button">
                <button onClick={handleCalculate} className="calculate">Calculate</button>
            </div>
            {calculationResult && (
                <div className="longitudinal-calculation-result">
                    <h2>Calculation result:</h2>
                    <button onClick={handleDownload} className="longitudinal-download-button">Download data</button>
                </div>
            )}
        </div>
    );
}

export default Longitudinal;
