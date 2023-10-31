# Gaming Backlog

###What is it?
This is an application to help those of us who have an issue getting through our gaming backlog.

###How do you use it?
I'm glad you asked!
1. Search for the game you want.
2. Select the game from the list of results.
3. Wait for results to generate.

###How does it work?
Another great question!

First of all, when you search for a game, the app will utilize the howlongtobeat api.
Using this, it will grab the title, how long it takes to beat the main story, the genre,
and the weblink for the game's page on howlongtobeat.com.

Once it grabs all that info, it will take the game title and get the metacritic score for that game.

With all this info, it will then divide the metacritic score by how long it takes to beat the game and
provide you with what I call the "Fun Quotient", 
which is a numerical value of the fun per time you can expect from each game.

Then it tucks it in neatly into a database for you to review whenever you're ready.

###Challenges and things I learned
My big issue in the beginning was figuring out the UI, since I decided to try
getting the front-end and back-end working simultaneously(which I do not recommend unless you hate sleep).


Once I decided to focus on the back-end first, the project became much more manageable.

My big issue with the back-end was trying to implement functionality that doesn't exist on it's own
with the howlongtobeat API. So I had to learn more about web crawling so I could get some of the information myself.
This includes the genre from howlongtobeat.com and the score from metacritic.

###In conclusion
This is still a work in progress as I finish up the back-end and get the front-end working,
but this project has been so much fun and I hope that you enjoy.