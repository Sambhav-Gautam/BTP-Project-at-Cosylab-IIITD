const mongoose = require('mongoose');
const { Schema } = mongoose;

const recipeSchemaO = new Schema({
  _id: { type: Schema.Types.ObjectId, required: true },
  Sno: { type: Number, required: true },
  title: { type: String, required: true },
  ingredients: { type: String, required: true },
  instructions: { type: String, required: true }
});

const RecipeO = mongoose.model('RecipeO', recipeSchemaO);

module.exports = RecipeO;
