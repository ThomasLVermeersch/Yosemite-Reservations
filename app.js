const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const PythonShell = require('python-shell');
const mongoose = require('mongoose');
const config = require('./config');
var up;

mongoose.connect(config.MONGODB_URL);

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log("Connected to db");
  up = db.collection('upper_pines');
  lp = db.collection('lower_pines');
  np = db.collection('north_pines');
  wa = db.collection('wawona');
  ho = db.collection('hodgdon');
  cf = db.collection('crane_flat');
});

const app = express();

//view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));


//Body parser middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

//Set static path
app.use(express.static(path.join(__dirname, 'public')));


//routes
app.get('/', (req, res) =>{
	res.render('index');
});

app.get('/getbydate/:start&:end', (req, res) =>{


});

app.get('/getUpper', (req,res)=>{
	up.find().toArray(function(err, result) {
        	console.log("RES");
        	console.log(result);
        	res.json(result);
    	});  
});

app.get('/getLower', (req,res)=>{
	lp.find().toArray(function(err, result) {
        	console.log("RES");
        	console.log(result);
        	res.json(result);
    	});  
});
app.get('/getNorth', (req,res)=>{
	np.find().toArray(function(err, result) {
        	console.log("RES");
        	console.log(result);
        	res.json(result);
    	});  
});
app.get('/getCrane', (req,res)=>{
	cf.find().toArray(function(err, result) {
        	console.log("RES");
        	console.log(result);
        	res.json(result);
    	});  
});
app.get('/getWawona', (req,res)=>{
	wa.find().toArray(function(err, result) {
        	console.log("RES");
        	console.log(result);
        	res.json(result);
    	});  
});
app.get('/gethodgdon', (req,res)=>{
	ho.find().toArray(function(err, result) {
        	console.log("RES");
        	console.log(result);
        	res.json(result);
    	});  
});


app.listen('3000', () =>{
	console.log('Server started on port 3000');
});