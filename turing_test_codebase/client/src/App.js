import logo from './logo.svg';
import './App.css';
import Home from './Components/Home';
import Headers from './Components/Headers';
import Login from './Components/Login';
import Error from './Components/Error';
import About from './Components/About'; // Import About component
import { Routes, Route } from "react-router-dom";
import OccupationAdder from './Components/occup';
import RandomRecipeComponent from './Components/Dashboard';
import Stats from './Components/stats';
import StatsPage from './Components/StatsPage';
import RecipeDetails from './Components/RecipeDetails';

function App() {
  return (
    <>
      <Headers />
      <Routes>
        <Route path='/' element={<Login />} />
        <Route path='/login' element={<Login />} />
        <Route path='/error' element={ <Error />} />
        <Route path='/dashboard' element={<RandomRecipeComponent />} />
        <Route path='/occupation_adder' element={<OccupationAdder />} />
        <Route path='/about' element={<About />} /> {/* Add About route */}
        <Route path='*' element={<Error />} />
        <Route path='/stats' element={<StatsPage />} />
        <Route path='/profile' element={<Stats />} />
        <Route path='/recipe/:recipeId' element={<RecipeDetails />} />
      </Routes>
    </>
  );
}

export default App;
