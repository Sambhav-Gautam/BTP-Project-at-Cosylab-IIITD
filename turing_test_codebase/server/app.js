require("dotenv").config();
const express = require("express");
const app = express();
const cors = require("cors");
require("./db/conn")
const PORT = 6005;
const session = require("express-session");
const passport = require("passport");
const OAuth2Strategy = require("passport-google-oauth2").Strategy;
const userdb = require("./model/userSchema")
const path = require( 'path' );

const clientid = ""
const clientsecret = ""
const RecipeG = require("./model/recipeG"); // Adjust the path as necessary
const RecipeO = require("./model/recipeO"); // Adjust the path as necessary


const BASE_PATH = '/ttc';

app.use(`${BASE_PATH}/static`, express.static(path.join(__dirname, "../client/build/static")));
app.use(`${BASE_PATH}/`, express.static(path.join(__dirname, "../client/build")));

app.use(cors({
    origin:["http://localhost:3000","http://localhost:3000/","http://localhost:6005/","http://localhost:6005","http://cosylab.iiitd.edu.in"],
    methods:"GET,POST,PUT,DELETE",
    credentials:true
}));


const ensureHttps = (req, res, next) => {
    if (req.secure || req.headers['x-forwarded-proto'] === 'https') {
        return next();
    }
    res.redirect(`https://${req.headers.host}${req.url}`);
};


app.use(ensureHttps);




app.use(express.json());

// setup session
app.use(session({
    secret:"YOUR SECRET KEY",
    resave:false,
    saveUninitialized:true
}))

// setuppassport
app.use(passport.initialize());
app.use(passport.session());

passport.use(
    new OAuth2Strategy({
        clientID:clientid,
        clientSecret:clientsecret,
        callbackURL:`https://cosylab.iiitd.edu.in/ttc/auth/google/callback`,
        scope:["profile","email"]
    },
    async(accessToken,refreshToken,profile,done)=>{
        try {
            let user = await userdb.findOne({googleId:profile.id});

            if(!user){
                user = new userdb({
                    googleId:profile.id,
                    displayName:profile.displayName,
                    email:profile.emails[0].value,
                    image:profile.photos[0].value,
                });

                await user.save();
            }

            return done(null,user)
        } catch (error) {
            return done(error,null)
        }
    }
    )
)

passport.serializeUser((user,done)=>{
    done(null,user);
})

passport.deserializeUser((user,done)=>{
    done(null,user);
});

// initial google ouath login
// app.get("/auth/google",passport.authenticate("google",{scope:["profile","email"]}));

// app.get("/auth/google/callback",passport.authenticate("google",{
//     successRedirect:"http://localhost:3000/occupation_adder",
//     failureRedirect:"http://localhost:3000/login"
// }))

app.get(`${BASE_PATH}/auth/google`, passport.authenticate("google", {scope: ["profile", "email"]}));


app.get(`${BASE_PATH}/auth/google/callback`, 
    passport.authenticate("google", { failureRedirect: `${BASE_PATH}/login` }),
    async (req, res) => {
        try {
            const googleId = req.user.googleId; // Now, req.user will be populated
            const existingUser = await userdb.findOne({ googleId });

            if (existingUser) {
                if (existingUser.occupation) {
                    // If the user has an occupation, redirect to the dashboard
                    return res.redirect(`${BASE_PATH}/dashboard`);
                } else {
                    // If the user doesn't have an occupation, redirect to occupation_adder
                    return res.redirect(`${BASE_PATH}/occupation_adder`);
                }
            } else {
                // If the user is not found, redirect to login (though this shouldn't happen)
                return res.redirect(`${BASE_PATH}/login`);
            }
        } catch (error) {
            console.error('Error during Google callback:', error);
            return res.redirect(`${BASE_PATH}/login`);
        }
    }
);

app.get(`${BASE_PATH}/login/success`,async(req,res)=>{

    if(req.user){
        res.status(200).json({message:"user Login",user:req.user})
    }else{
        res.status(400).json({message:"Not Authorized"})
    }
})

app.get(`${BASE_PATH}/logout`,(req,res,next)=>{
    req.logout(function(err){
        if(err){return next(err)}
        res.redirect(`${BASE_PATH}/login`);
    })
})


app.post(`${BASE_PATH}/occupation_adder`, async (req, res) => {
    const { googleId, occupation } = req.body;

    try {
        // Find the user by googleId and update the occupation
        const updatedUser = await userdb.findOneAndUpdate(
            { googleId }, // Find the user by googleId
            { occupation: occupation }, // Update the occupation field
            { new: true } // Return the updated user document
        );

        if (updatedUser) {
            res.status(200).json({ message: 'Occupation updated successfully', user: updatedUser });
            // res.redirect("http://localhost:3000/dashboard");
        } else {
            res.status(404).json({ message: 'User not found' });
        }
    } catch (error) {
        console.error('Error updating occupation:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

// Import the required models at the top of your file


// // Add this route for fetching a random recipe
// app.get("/api/random-recipe", async (req, res) => {

// const { userId } = req.body;


// try {
// // Generate a random number (0 or 1)
// const randomNumber = Math.floor(Math.random() * 2);
// let recip,recipe;

// if (randomNumber === 0) {
// // Fetch a random recipe from RecipeG
// const count = await RecipeG.countDocuments();
// const randomIndex = Math.floor(Math.random() * count);
// recipe = await RecipeG.findOne().skip(randomIndex);
            
// } else {
// // Fetch a random recipe from RecipeO
// const count = await RecipeO.countDocuments();
// const randomIndex = Math.floor(Math.random() * count);
// recipe = await RecipeO.findOne().skip(randomIndex);
// }

// if (!recipe) {
// return res.status(404).json({ message: "No recipe found" });
// }

// res.status(200).json(recipe);
// } catch (error) {
// console.error("Error fetching random recipe:", error);
// res.status(500).json({ message: "Internal server error" });
// }
// });

app.get(`${BASE_PATH}/api/random-recipe`, async (req, res) => {
    const { userId } = req.body; // Assuming userId is passed as a query parameter

    try {
        // Fetch the user by userId
        const user = userdb.findById(userId);

        if (!user) {
            return res.status(404).json({ message: "User not found" });
        }

        // Combine all checked recipes (RF, FR, RR, FF) into a single array
        const checkedRecipes = user.recipe_evaluated;

        let recipe;
        let count;
        let attempts = 0; // Add a fallback in case no unchecked recipes are found

        while (!recipe && attempts < 10) { // Attempt 10 times to find an unchecked recipe
            const randomNumber = Math.floor(Math.random() * 2);

            if (randomNumber === 0) {
                // Fetch random recipe from RecipeG that has not been checked
                count = await RecipeG.countDocuments({ _id: { $nin: checkedRecipes } });
                if (count === 0) break; // No more unchecked recipes in RecipeG
                const randomIndex = Math.floor(Math.random() * count);
                recipe = await RecipeG.findOne({ _id: { $nin: checkedRecipes } }).skip(randomIndex);
            } else {
                // Fetch random recipe from RecipeO that has not been checked
                count = await RecipeO.countDocuments({ _id: { $nin: checkedRecipes } });
                if (count === 0) break; // No more unchecked recipes in RecipeO
                const randomIndex = Math.floor(Math.random() * count);
                recipe = await RecipeO.findOne({ _id: { $nin: checkedRecipes } }).skip(randomIndex);
            }

            attempts++;
        }

        if (!recipe) {
            return res.status(404).json({ message: "No unchecked recipe found" });
        }

        res.status(200).json(recipe);
    } catch (error) {
        console.error("Error fetching random recipe:", error);
        res.status(500).json({ message: "Internal server error" });
    }
});



app.post(`${BASE_PATH}/api/evaluate-recipe`, async (req, res) => {

    const { userId, recipeId, evaluation } = req.body;

    try {
        // Find the recipe in RecipeG or RecipeO
        const recipeGe = await RecipeG.findById(recipeId);
        const recipeOe = await RecipeO.findById(recipeId);

        // Determine where the recipe is located and update user's feedback
        const user = await userdb.findById(userId);


        if(evaluation ==='skip'){
            user.recipe_skipped.push(recipeId);
        }

        if (recipeGe) {
            // Recipe was found in RecipeG
            if (evaluation === 'real') {
                user.RF.push(recipeId);
                user.recipe_evaluated.push(recipeId);
            } else if (evaluation === 'fake') {
                user.FF.push(recipeId);
                user.recipe_evaluated.push(recipeId);
            }
        } else if (recipeOe) {
            // Recipe was found in RecipeO
            if (evaluation === 'real') {
                user.RR.push(recipeId);
                user.recipe_evaluated.push(recipeId);
            } else if (evaluation === 'fake') {
                user.FR.push(recipeId);
                user.recipe_evaluated.push(recipeId);
            }
        } else {
            return res.status(404).json({ message: "Recipe not found" });
        }

        await user.save();
        res.status(200).json({ message: "Evaluation saved successfully" });
        // res.redirect("http://localhost:3000/dashboard");

    } catch (error) {
        res.status(500).json({ message: "Error saving evaluation", error });
    }
});


app.get(`${BASE_PATH}/login/userdata`, async (req, res) => {
    if (req.user) {
        try {
            // Fetch the user data from the database
            const user = await userdb.findById(req.user._id); // Use the user ID stored in the session

            if (!user) {
                return res.status(404).json({ message: "User not found" });
            }

            // Return the updated user data
            res.status(200).json({ message: "User data fetched successfully", user });
        } catch (error) {
            console.error("Error fetching user data:", error);
            res.status(500).json({ message: "Internal server error" });
        }
    } else {
        res.status(400).json({ message: "Not Authorized" });
    }
});

app.get(`${BASE_PATH}/`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });

app.get(`${BASE_PATH}/dashboard`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });
  

app.get(`${BASE_PATH}/profile`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });
  
app.get(`${BASE_PATH}/error`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });

app.get(`${BASE_PATH}/login`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });
  
app.get(`${BASE_PATH}/about` , (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });
    


// Fallback route to serve index.html for unknown paths
app.get(`${BASE_PATH}/occupation_adder`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
  });
  



app.listen(PORT,()=>{
    console.log(`server start at port no ${PORT}`)
})



// New 








app.get(`${BASE_PATH}/stats`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});


app.get(`${BASE_PATH}/api/recipe/:recipeId`, async (req, res) => {
    const { recipeId } = req.params;
    console.log(`Received request for recipe ID: ${recipeId}`); // Log the received ID

    try {
        // First, check in RecipeG
        const recipeG = await RecipeG.findById(recipeId);
        console.log('RecipeG found:', recipeG); // Log the result from RecipeG

        if (recipeG) {
            return res.status(200).json(recipeG);
        }

        // If not found in RecipeG, check in RecipeO
        const recipeO = await RecipeO.findById(recipeId);
        console.log('RecipeO found:', recipeO); // Log the result from RecipeO
        
        if (recipeO) {
            return res.status(200).json(recipeO);
        }

        // If not found in either, return a 404
        console.warn(`Recipe not found for ID: ${recipeId}`); // Log when not found
        return res.status(404).json({ message: 'Recipe not found' });
    } catch (error) {
        console.error('Error fetching recipe details:', error);
        return res.status(500).json({ message: 'Internal server error' });
    }
});


app.get(`${BASE_PATH}/recipe/:recipeId`, (req, res) => {
    res.sendFile(path.join(__dirname, '../client/build', 'index.html'));
});


// In your backend (server.js or app.js)
app.get(`${BASE_PATH}/api/fetch-confusion-matrix`, async (req, res) => {
    try {
        const user_data = await userdb.find(); // Fetch all user data

        // Aggregate values across all users
        let FF = 0, FR = 0, RF = 0, RR = 0;
        user_data.forEach(user => {
            FF += user.FF.length;
            FR += user.FR.length;
            RF += user.RF.length;
            RR += user.RR.length;
        });

        // Return the confusion matrix data
        res.json({ FF, FR, RF, RR });
    } catch (error) {
        console.error('Error fetching user data:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});

app.get(`${BASE_PATH}/api/fetch-intersections`, async (req, res) => {
    try {
        const user_data = await userdb.find();

        let ffIntersection = user_data.length > 0 ? [...user_data[0].FF] : [];
        let rfIntersection = user_data.length > 0 ? [...user_data[0].RF] : [];
        let frIntersection = user_data.length > 0 ? [...user_data[0].FR] : [];
        let rrIntersection = user_data.length > 0 ? [...user_data[0].RR] : [];

        const intersection = (arr1, arr2) => arr1.filter(value => arr2.includes(value));

        user_data.forEach(user => {
            ffIntersection = intersection(ffIntersection, user.FF);
            rfIntersection = intersection(rfIntersection, user.RF);
            frIntersection = intersection(frIntersection, user.FR);
            rrIntersection = intersection(rrIntersection, user.RR);
        });

        // Always return arrays, even if they're empty
        res.json({
            FF: ffIntersection,
            RF: rfIntersection,
            FR: frIntersection,
            RR: rrIntersection,
        });
    } catch (error) {
        console.error('Error fetching user data:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});


// Endpoint to fetch unions across all users
app.get(`${BASE_PATH}/api/fetch-unions`, async (req, res) => {
    try {
        const user_data = await userdb.find(); // Fetch all user data

        // Initialize union arrays
        let FF = [];
        let RF = [];
        let FR = [];
        let RR = [];

        // Loop through all users to collect union data
        user_data.forEach(user => {
            FF = [...new Set([...FF, ...user.FF])];
            RF = [...new Set([...RF, ...user.RF])];
            FR = [...new Set([...FR, ...user.FR])];
            RR = [...new Set([...RR, ...user.RR])];
        });

        // Return the union data
        res.json({ FF, RF, FR, RR });
    } catch (error) {
        console.error('Error fetching union data:', error);
        res.status(500).json({ message: 'Internal server error' });
    }
});
