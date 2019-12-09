Design decisions and reasons

1. This project contains 29 html pages, 6 javascript files, 3 css files, 3 tables in a database, bunches of images designed by myself and is organized by using Flask in python.
2. 29 html pages are catagorized into 7 groups: welcome, login, register, my space, write a card, browse, and search. "Write a card" contains most of html pages because it provide not only
   two front-side designs, a back-side design, but also provide 4 styles to choose, with detailed instructions.
3. Among 6 javascript files, 4 of them are used to create interactive webcam filters. The source code were found on https://www.openprocessing.org, I resized the canvas, modified the functions
   inside, and added touch-gui to each of them so that users can customize their own filters based on what are provided. The other two javascript files are downloaded from
   https://tympanus.net/codrops/, which support the animation of top-left drop-down menu.
4. 2 css files contained in css folder were downloaded from https://tympanus.net/codrops/, which support the animation of top-left drop-down menu. The other css file is specially customized
   for this project.
5. In the database called "emotionlibrary.db" contains 3 tables: "users", "firstcard", "card". "users" is used to store users' accounts. "firstcard" is used to store input information user
   typed in on the front side of first card. I seperated it from "card" because it contains more columns of information than other cards. "card" stores the input information users typed in
   on the completely empty new cards.
6. I have spent several days on the UI/UX design. All the images in the static folder were drawn by myself in order to make every webpage look like a certain view of a room so that users will
   have a feeling like walking into a virtual library when they use the website.
7. Except "index.html", "login.html", "register.html", all the other pages should require users to login first.