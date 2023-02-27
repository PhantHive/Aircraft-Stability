import "../styles/Longitudinal.css";

import React, { Component } from "react";

import FileSelector from "./FileSelector.js";

class Longitudinal extends Component {
  constructor(props) {
    super(props);
    this.imgData = null;
    this.state = {
      file1: null,
      file2: null,
      calculationResult: null,
      calculationComplete: false,
    };
  }

  downloadResult = (data) => {
    let dataToTxt = JSON.stringify(data, null, 4);
    dataToTxt = dataToTxt.replace(/^-+$/gm, ""); // Remove separator lines
    dataToTxt = dataToTxt.replace(/\\r\\n/g, "\n"); // Replace new line characters
    dataToTxt = dataToTxt.replace(/^{.+result": "/s, ""); // remove leading JSON

    // from formData get what is between "ImageData<" and ">"
    this.imgData = dataToTxt.substring(
      dataToTxt.indexOf("ImageData<") + 10,
      dataToTxt.indexOf(">")
    );

    // remove the image data from the text file and save it
    dataToTxt = dataToTxt.replace(/ImageData<.+>/s, "");
    // remove last trailing characters " and } from the text file
    dataToTxt = dataToTxt.substring(0, dataToTxt.length - 3);

    let blob = new Blob([dataToTxt], { type: "text/plain" });
    let url = URL.createObjectURL(blob);
    let a = document.createElement("a");
    a.download = "data.txt";
    a.href = url;
    document.body.appendChild(a);
    a.click();
  };

  handleFile1Change = (file) => {
    this.setState({ file1: file });
    console.log(this.state.file1);
  };

  handleFile2Change = (file) => {
    this.setState({ file2: file });
    console.log(this.state.file2);
  };

  handleCalculate = () => {
    const { file1, file2 } = this.state;

    // check if file is null
    if (file1 === null || file2 === null) {
      alert("Please select a file");
      return;
    }

    // check if file is JSON
    if (
      file1.type !== "application/json" ||
      file2.type !== "application/json"
    ) {
      alert("Please select a JSON file");
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
        formData = JSON.stringify({ file1: file1Content, file2: file2Content });
        // do something with the form data
        console.log(formData);
        fetch("http://localhost:3001/process_data", {
          method: "POST",
          body: formData,
          headers: { "Content-Type": "application/json" },
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Received data:", data);
            // transform json to .txt file and make it available for download
            this.downloadResult(data);
            document
              .getElementsByClassName("longitudinal-file-selector")[0]
              .remove();
            document
              .getElementsByClassName("longitudinal-calculation-button")[0]
              .remove();
            document.getElementsByClassName("select")[0].innerHTML =
              "Download your data or Reset";

            this.setState({
              calculationResult: data,
              calculationComplete: true,
            });
          })
          .catch((error) => {
            console.error("Error:", error);
            console.log(error.response);
          });
      };
      reader2.readAsText(file2);
    };
    reader1.readAsText(file1);

    console.log(formData);
  };

  handleDownload = () => {
    this.downloadResult(this.state.calculationResult);
  };

  handleReset = () => {
    // Reset calculation here
    console.log("Resetting calculation");
    window.location.reload();
  };

  render() {
    return (
      <div className="longitudinal-container">
        <h1 className="longitudinal-title">
          Longitudinal stability calculation
        </h1>
        <img
          className="longitudinal-image"
          src={require("../assets/images/plane-longitudinal.png")}
          alt="Longitudinal stability"
        />
        <h2 className="select">
          Select a JSON file containing plane data (follow README.md)
        </h2>
        <div className="longitudinal-file-selector">
          <FileSelector
            key="flight-data"
            label="Flight Data"
            onFileSelect={this.handleFile1Change}
          />
          <FileSelector
            key="derivatives-data"
            label="Derivatives Data"
            onFileSelect={this.handleFile2Change}
          />
        </div>
        <div className="longitudinal-calculation-button">
          <button onClick={this.handleCalculate} className="calculate">
            Calculate
          </button>
        </div>
        {this.state.calculationComplete && (
          <div className="longitudinal-calculation-result">
            <h2>Calculation result: </h2>
            <button
              onClick={this.handleDownload}
              className="longitudinal-download-button"
            >
              Download data
            </button>
          </div>
        )}
        {this.state.calculationComplete && (
          <div className="reset">
            <button onClick={this.handleReset} className="reset-button">
              Reset
            </button>
            <img
              src={`data:image/png;base64,${this.imgData}`}
              alt="Phugoid Mode Response"
              className="phugoid-curve"
            />
          </div>
        )}
      </div>
    );
  }
}

export default Longitudinal;
