const mongoose = require("mongoose");

const DB = "mongodb+srv://sambhavsingh911:nigganigga@tcluster0.osayr3i.mongodb.net/trying?retryWrites=true&w=majority&appName=tCluster0";

mongoose.connect(DB,{
    useUnifiedTopology:true,
    useNewUrlParser:true
}).then(()=>console.log("database connected")).catch((err)=>console.log("errr",err))