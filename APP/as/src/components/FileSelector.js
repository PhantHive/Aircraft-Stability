import React, { Component } from 'react';
import '../styles/FileSelector.css';
import { v4 as uuidv4 } from 'uuid'; // Import the uuid library

class FileSelector extends Component {
    constructor(props) {
        super(props);

        this.state = {
            selectedFile: null,
        };

        this.id = uuidv4();
    }

    handleFileSelect = (event) => {
        const file = event.target.files[0];
        this.setState({ selectedFile: file });
        this.props.onFileSelect(file);
    };

    handleButtonClick = () => {
        document.getElementById(this.id).click();
    };

    render() {
        return (
            <div className="file-selector">
                <input id={this.id} type="file" onChange={this.handleFileSelect} />
                <button onClick={this.handleButtonClick}>
                    {this.state.selectedFile ? this.state.selectedFile.name : this.props.label}
                </button>
            </div>
        );
    }
}

export default FileSelector;
