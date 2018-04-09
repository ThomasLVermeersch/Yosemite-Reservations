const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const PythonShell = require('python-shell');
const mongoose = require('mongoose');
const config = require('./config');
var up, lp, np, wa, ho, cf;
var north_data;
var doc_list = [up, lp, np, wa, ho, cf];

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

app.get('/all', (req, res) =>{
  var all = {};
  getDocData(up, function(result){
    all["upper_pines"] = result;
    getDocData(lp, function(result){
      all["lower_pines"] = result;
      getDocData(np, function(result){
        all["north_pines"] = result;
        getDocData(wa, function(result){
          all["wawona"] = result;
          getDocData(cf, function(result){
            all["crane_flat"] = result;
            getDocData(ho, function(result){
              all["hodgdon"] = result;
              res.json(all);
            });
          });
        });
      });
    });
  });
});

app.get('/getbydate/:start&:end', (req, res) =>{
  var end_data = {};
  var start;
  var end;
  getDaysTil(req.params.start, function(result){
    console.log("HERE");
    start = result;
    getDaysTil(req.params.end, function(result){
      end = result;
      getDocDataWithAvailability([up, start, end], function(result){
        end_data["Upper Pines"] = result;
        getDocDataWithAvailability([lp, start, end], function(result){
          end_data["Lower Pines"] = result;
          getDocDataWithAvailability([np, start, end], function(result){
          end_data["North Pines"] = result;
          getDocDataWithAvailability([cf, start, end], function(result){
            end_data["Crane Flats"] = result;
            getDocDataWithAvailability([ho, start, end], function(result){
              end_data["Hodgdon"] = result;
              getDocDataWithAvailability([wa, start, end], function(result){
                end_data["Wawona"] = result;
                findPair([end_data, start, end], function(result){
                  //console.log(result);
                  res.json(result);
                });
              });
            });
          });
        });
    });
  });
  });
});

});

app.get('/getUpper', (req,res)=>{
	getDocData(up, function(result){
    res.json(result);
  })
});

app.get('/getLower', (req,res)=>{
	getDocData(lp, function(result){
    res.json(result);
  })
});

app.get('/getNorth', (req,res)=>{
  getDocData(np, function(result){
    res.json(result);
  })
});
app.get('/getCrane', (req,res)=>{
	getDocData(cf, function(result){
    res.json(result);
  })  
});
app.get('/getWawona', (req,res)=>{
	getDocData(wa, function(result){
    res.json(result);
  })  
});
app.get('/gethodgdon', (req,res)=>{
	getDocData(ho, function(result){
    res.json(result);
  })  
});
//Get all data for one document
function getDocData(req, res){
  req.find().toArray(function(err, result) {
          res(result);
      }); 
}

//Get difference in days
function getDaysTil(req, res){
  var date = new Date(req);
  var today = new Date();
  var dd = new Date(today);
  dd = dd.toLocaleDateString('en-US', { timeZone: 'America/Los_Angeles' });
  var new_d = new Date(date);
  var today = new Date(dd);
  var time_to_date_millis = new_d.getTime() - today.getTime();
  var dts = Math.floor(time_to_date_millis / (1000 * 60 * 60 * 24)) + 1;
  console.log(dts);
  res(dts);
}
//get all data based on dates
function getDocDataWithAvailability(req, res){
  var dts = req[1];
  var dte = req[2];
  var sq = {};
  var eq = {};
  var s = "availability." + dts;
  var e = "availability." + dte;
  sq[s] = 'A';
  eq[e] = 'A';
  req[0].find({$or: [sq, eq]}).toArray(function(err, result) {
    //console.log(result);
    res(result);
  }); 
}

function findPair(req,res){
  var start_sites = {};
  var end_sites = {};
  var all_map = req[0];
  var s = req[1];
  var e = req[2];
  for(myMap in all_map){
    var i_map = all_map[myMap];
    for(end in i_map){
      if(i_map[end].availability[s] == 'A'){
        start_sites[i_map[end]._id] = i_map[end].availability;
      }
      if(i_map[end].availability[e] == 'A'){
        end_sites[i_map[end]._id] = i_map[end].availability;
      }
    }
  }
  console.log(start_sites);
  console.log(end_sites);
  var longest_start = 0;
  var best_start_site = "none";
  for(key in start_sites){
    var site_array = start_sites[key];
    var i = s;
    while(site_array[i] == 'A' && i <= e){
      i++;
    }
    if(i > longest_start){
      best_start_site = key;
    }
  }
  var longest_end = 0;
  var best_end_site = "none";
  for(key in end_sites){
    var site_array = end_sites[key];
    var i = e;
    while(site_array[i] == 'A' && i >= s){
      i--;
    }
    if(i > longest_end){
      best_end_site = key;
    }
  }
  //console.log(start_sites);
  console.log(start_sites[best_start_site]);
  console.log(end_sites[best_end_site]);
  console.log("BEST START: " + best_start_site);
  console.log("BEST END: " + best_end_site);
}

app.listen('3000', () =>{
	console.log('Server started on port 3000');
});