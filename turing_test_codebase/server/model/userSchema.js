// // const mongoose = require("mongoose");

// // const userSchema = new mongoose.Schema({
//     // googleId:String,
//     // displayName:String,
//     // email:String,
//     // image:String
// // },{timestamps:true});


// // const userdb = new mongoose.model("users",userSchema);

// // module.exports = userdb;


// const mongoose = require('mongoose');
// const { Schema } = mongoose;

// const userSchema = new Schema({
// //   _id: { type: Schema.Types.ObjectId, required: true },
//   googleId:String,
//     displayName:String,
//     email:String,
//     image:String,
// //   name: { type: String, required: true },
// //   user_img: { type: String, required: false },
//   occupation: { type: String, required: false },
//   real_count: { type: Number, required: false },
//   fake_count: { type: Number, required: false },
//   RF: { type: Array, required: false },
//   FR: { type: Array, required: false },
//   RR: { type: Array, required: false },
//   FF: { type: Array, required: false },
//   total: { type: Number, required: false },
//   recipe_evaluated: { type: Array, required: false },
//   recipe_skipped: { type: Array, required: false },
//   rand_num: { type: Number, required: false }
// },{timestamps:true});

// module.exports = mongoose.model('User', userSchema);



const mongoose = require('mongoose');
const { Schema } = mongoose;

const userSchema = new Schema({
  googleId: { type: String, index: true }, // Added index for faster queries
  displayName: { type: String },
  email: { type: String, required: true, unique: true }, // Unique constraint for email
  image: { type: String },
  occupation: { type: String },
  real_count: { type: Number, default: 0 }, // Default value to avoid undefined
  fake_count: { type: Number, default: 0 }, // Default value to avoid undefined
  RF: { type: [String], default: [] }, // Array of strings, can be changed based on use case
  FR: { type: [String], default: [] },
  RR: { type: [String], default: [] },
  FF: { type: [String], default: [] },
  total: { type: Number, default: 0 },
  recipe_evaluated: { type: [String], default: [] }, // Assuming it stores evaluated recipe IDs or names
  recipe_skipped: { type: [String], default: [] }, // Assuming it stores skipped recipe IDs or names
  rand_num: { type: Number, default: 0 }
}, { timestamps: true });

module.exports = mongoose.model('User', userSchema);
