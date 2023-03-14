import '../styles/Lateral.css';

import React, {Component} from 'react';
import {Link} from "react-router-dom";

import FileSelector from './FileSelector.js';

class Lateral extends Component {
  constructor(props) {
    super(props);
    this.imgPhugoid = null;
    this.imgShort = null;
    this.state = {
      file1 : null,
      file2 : null,
      calculationResult : null,
      calculationComplete : false
    };
  }

  downloadResult = (data) => {
    let dataToTxt = JSON.stringify(data, null, 4);
    dataToTxt = dataToTxt.replace(/^-+$/gm, ''); // Remove separator lines
    dataToTxt =
        dataToTxt.replace(/\\r\\n/g, '\n'); // Replace new line characters
    dataToTxt = dataToTxt.replace(/^{.+result": "/s, ''); // remove leading JSON

    // from formData get what is between "ImageData<" and ">"
    this.imgRolling =
        dataToTxt.substring(dataToTxt.indexOf('ImageDataRolling<') + 17,
                            dataToTxt.indexOf('>Rolling'));
    this.imgSpiral =
        dataToTxt.substring(dataToTxt.indexOf('ImageDataSpiral<') + 16,
                            dataToTxt.indexOf('>Spiral'));
    console.log(this.imgRolling);
    console.log(this.imgSpiral);

    // remove the image data from the text file and save it
    dataToTxt = dataToTxt.replace(/ImageDataRolling<.+>/s, '');
    dataToTxt = dataToTxt.replace(/ImageDataSpiral<.+>/s, '');
    // remove last trailing characters " and } from the text file
    dataToTxt = dataToTxt.substring(0, dataToTxt.length - 3);

    let blob = new Blob([ dataToTxt ], {type : 'text/plain'});
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.download = 'plane_data.txt';
    a.href = url;
    document.body.appendChild(a);
    a.click();
  };

  handleFile1Change = (file) => {
    this.setState({file1 : file});
    console.log(this.state.file1);
  };

  handleFile2Change = (file) => {
    this.setState({file2 : file});
    console.log(this.state.file2);
  };

  handleCalculate = () => {
    const {file1, file2} = this.state;

    // check if file is null
    if (file1 === null || file2 === null) {
      alert('Please select a file');
      return;
    }

    // check if file is JSON
    if (file1.type !== 'application/json' ||
        file2.type !== 'application/json') {
      alert('Please select a JSON file');
      return;
    }

    // // Perform calculation here and set the result in the calculationResult
    // state console.log('Calculating using file:', file1, file2); const
    // formData = new FormData(); formData.append('file1', file1);
    // formData.append('file2', file2);
    //
    // const boundary = '----WebKitFormBoundary' +
    // Math.random().toString().slice(2);

    // concatenate the two files and stringify them
    // read the contents of file1 as a string
    let formData = null;
    const reader1 = new FileReader();
    reader1.onload = () => {
      const file1Content = reader1.result;
      // read the contents of file2 as a string
      const reader2 = new FileReader();
      reader2.onload = () => {
        const file2Content = reader2.result;
        // concatenate the two files and stringify them
        formData = JSON.stringify(
            {file1 : file1Content, file2 : file2Content, selected : 1});
        // do something with the form data
        console.log(formData);
        fetch('http://localhost:3001/process_data', {
          method : 'POST',
          body : formData,
          headers : {'Content-Type' : 'application/json'}
        })
            .then(response => response.json())
            .then(data => {
              console.log('Received data:', data);
              // transform json to .txt file and make it available for download
              this.downloadResult(data);
              document.getElementsByClassName('lateral-file-selector')[0]
                  .remove();
              document.getElementsByClassName('lateral-calculation-button')[0]
                  .remove();
              document.getElementsByClassName('select')[0].innerHTML =
                  'Download your data or Reset';

              this.setState(
                  {calculationResult : data, calculationComplete : true});
            })
            .catch(error => {
              console.error('Error:', error);
              console.log(error.response);
            });
      };
      reader2.readAsText(file2);
    };
    reader1.readAsText(file1);

    console.log(formData);
  };

  handleDownload = () => { this.downloadResult(this.state.calculationResult); };

  handleReset = () => {
    // Reset calculation here
    console.log('Resetting calculation');
    window.location.reload();
  };

  render() {
        return (
            <div className="lateral-container">
                <div className="home-button">
                    <Link to="/">
                        <button className="home">Home</button>
                    </Link>
                </div>
                <h1 className="lateral-title">lateral stability calculation</h1>
                <img className="lateral-image" src={require('../assets/images/plane-lateral.png')} alt="lateral stability" />
                <h2 className="select">Select a JSON file containing plane data (follow README.md)</h2>
                <div className="lateral-file-selector">
                    <FileSelector key="flight-data" label="Flight Data" onFileSelect={this.handleFile1Change} />
                    <FileSelector key="derivatives-data" label="Derivatives Data" onFileSelect={
      this.handleFile2Change} />
                </div>
                <div className="lateral-calculation-button">
                    <button onClick={this.handleCalculate} className="calculate">Calculate</button>
                </div>
                {this.state.calculationComplete && (
                    <div className="lateral-calculation-result">
                        <h2>Calculation result:</h2>
                        <button onClick={this.handleDownload} className="lateral-download-button">Download data</button>
                    </div>
                )}
                {this.state.calculationComplete && (
                    <div className="reset">
                        <button onClick={this.handleReset} className="reset-button">Reset</button>
                        <div className="plot-images">
                            <img src={`data:image/png;base64,${this.imgRolling}`} alt="Rolling Mode Response" className="rolling-curve"/>
                            <img src={`data:image/png;base64,${this.imgSpiral}`} alt="Spiral Mode Response" className="spiral-curve"/>
                        </div>
                    </div>

                )}
            </div>
        );
    }
}

export default Lateral;