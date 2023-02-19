const express = require('express');
const app = express();
const port = process.env.PORT || 3001;
const axios = require('axios');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require("path");
const multer = require('multer');

// Parse incoming request bodies in a middleware before your handlers
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const pythonPath = path.join('main');
process.env.PYTHONPATH = pythonPath;

// Define a storage strategy for the uploaded files
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, file.originalname)
    }
});

// Configure the multer middleware to use the storage strategy and limit the file size
const upload = multer({
    storage: storage,
    limits: {
        fileSize: 1024 * 1024 * 10 // 10 MB
    }
});

// Define your /process_data route
app.post('/process_data', upload.fields([
    { name: 'file1', maxCount: 1 },
    { name: 'file2', maxCount: 1 }
]), (req, res) => {

    // Get the input data from the request body
    const file1 = req.files['file1'][0];
    const file2 = req.files['file2'][0];
    const inputData = [file1, file2]


    // Call the Python script and pass in the input data as arguments
    const cmd = `py -m ${pythonPath} ${JSON.stringify(inputData)}`;
    console.log(`Executing command: ${cmd}`);
    const process = spawn('py', ['-m', pythonPath, JSON.stringify(inputData)]);

    // Listen for data coming back from the Python script
    let result = '';
    process.stdout.on('data', data => {
        result += data.toString();
    });

    // Listen for the Python script to finish
    process.on('close', code => {
        if (code === 0) {
            // If the Python script exits with code 0 (success), return the result to the client
            // console.log("RESULT: " + result)
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
