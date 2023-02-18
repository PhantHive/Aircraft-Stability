import React, { useState } from 'react';
import '../styles/FileSelector.css';

function FileSelector(props) {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileSelect = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        props.onFileSelect(file);
    };

    const handleButtonClick = () => {
        document.getElementById('file-input').click();
    };

    return (
        <div className="file-selector">
            <input id="file-input" type="file" onChange={handleFileSelect} />
            <button onClick={handleButtonClick}>
                {selectedFile ? selectedFile.name : props.label}
            </button>
        </div>
    );
}

export default FileSelector;
