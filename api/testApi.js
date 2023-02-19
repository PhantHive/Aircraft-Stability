fetch('http://localhost:3001/process_data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "input": "data" })
})
    .then(response => response.json())
    .then(data => {
        console.log('Received data:', data);
        // Do something with the received data
    })
    .catch(error => {
        console.error('Error:', error);
    });
