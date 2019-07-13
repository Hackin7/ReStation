const express = require('express');
const path = require('path');
const fs = require('fs')
const router = express.Router();
var app = express();

app.use(express.static(path.join(__dirname, '../assets/')));

//  routes
app.get('/', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../index.html/'));
})

app.get('/learnmore', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../learnmore.html/'));
})

app.get('/alllistings', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../alllistings.html/'));
})

app.get('/newlisting', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../newlisting.html/'));
})

app.get('/rewardstier', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../rewardstier.html/'));
})

app.get('/myrewards', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../myrewards.html/'));
})



app.get('/upload.php', (req, resp) => {
    resp.sendFile(path.join(__dirname, '../assets/js/upload.php'))
})

app.listen(5000, () => {
    console.log("Server running on port 5000!");
})

module.exports = fs;