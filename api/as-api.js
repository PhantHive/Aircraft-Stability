const express = require('express');
const app = express();
const port = process.env.PORT || 3001;
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require("path");

// Parse incoming request bodies in a middleware before your handlers
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

let pythonPath;
process.env.PYTHONPATH = 'main_lon:main_lat';

// Define your /process_data route
app.post('/process_data',(req, res) => {
    // Get the input data from the request body
    let inputData = req.body;
    let file1 = JSON.stringify(inputData.file1);
    let file2 = JSON.stringify(inputData.file2);
    let selected = parseInt(inputData.selected);

    if (selected === 0) {
        pythonPath = 'main_lon'
    }
    else if (selected === 1) {
        pythonPath = 'main_lat'
    }

    // replace the double quote at the beginning and end of the string with a single quote
    file1 = file1.replace(/^"(.*)"$/, '$1');
    file2 = file2.replace(/^"(.*)"$/, '$1');

    // Call the Python script and pass in the input data as arguments
    const cmd = `py -m ${pythonPath} '${file1}' '${file2}'`;
    console.log(`Executing command: ${cmd}`);
    const process = spawn('py', ['-m', pythonPath, `${file1}`, `${file2}`]);

    // Listen for data coming back from the Python script
    let result = '';
    process.stdout.on('data', data => {
        result += data.toString();
    });

    // Listen for the Python script to finish
    process.on('close', code => {
        if (code === 0) {
            // If the Python script exits with code 0 (success), return the result to the client
            console.log("RESULT: " + result)
            res.json({ success: true, result: result });
        } else {
            // If the Python script exits with a non-zero code (error), return an error message to the client
            res.json({ success: false, error: 'An error occurred.' });
        }
    });
});

// Start the server
app.listen(port, () => {
    console.log('Server started on port ' + port + '.');
});
