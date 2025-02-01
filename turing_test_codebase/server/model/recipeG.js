const mongoose = require('mongoose');
const { Schema } = mongoose;

const recipeSchema = new Schema({
  _id: { type: Schema.Types.ObjectId, required: true },
  Sno: { type: Number, required: true },
  title: { type: String, required: true },
  ingredients: { type: String, required: true },
  instructions: { type: String, required: true },
  Fr0: { type: Number, required: true },
  Fr1: { type: Number, required: true },
  Fr2: { type: Number, required: true },
  Fr3: { type: Number, required: true },
  Fr4: { type: Number, required: true },
  Fr5: { type: Number, required: true },
  Uid0: { type: String, required: true },
  Uid1: { type: String, required: true },
  Uid2: { type: String, required: true },
  Uid3: { type: String, required: true },
  Uid4: { type: String, required: true },
  Uid5: { type: String, required: true }
});

const RecipeG = mongoose.model('RecipeG', recipeSchema);

module.exports = RecipeG;