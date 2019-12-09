Hi, welcome to use (e)motion library! You should be able to run this project within cs50 IDE and without any other plugin or special settings.

1.Title:
(e)motion library

2.Description:
(e)motion library is a platform that allows users to playfully, artistically and anonymously share their mental health concerns. It is a virtual mental world,
aimed at alleviating feelings of isolation, and destigmatizing mental illnesses.

3.Main Function:
Users are provided empty "cards". On the front side, users could type in their thoughts in text (if the user logs in for the first time, he will be asked to type in thoughts in certain
format, select options within drop-down menu). On the back side, users could choose one from four given filters, apply it to the webcam, and screen-record their faces with voices. In this
way, users create their self-portraits characterized by their emotions at that moment.
Users are able to see emotion portraits created by others in the "browse" page, and watch the portrait videos.
Users will be able to search the "library" for emotion portraits by keywords (not implemented yet).

4.Steps to use the website
1)Go to directory of the target forder called "emotionLibrary", type in  and run "flask run" in cs50 IDE, click the url and go to the index page.
2)The index page says "welcome to (e)motion library", then click enter and it will turn to "login" page.
3)If you do not have an account, you should click register on the page and it will turn to "register" page.
4)Type in your username, password, password confirmation, email address and click register. Then you will be lead back to "login" page.
5)login with your account, it will turn to "my space" page.
6)On "my space" page, you will see five buttons: write, search, browse, sunny room and rainy room.
    write: Click this button, you will be provided with an empty card. If it is your first time to write a card, it will give you a certain format, you should choose one option from
            the drop-down menu, then fill in the other input fields. When you finish, click save and flip card, your in-put information will be send to a table, and it will turn to
            "card_back" page. On this page, you should firstly see the instructions, then click one style from four different styles, adjust the silders to make your own style, and start
            speaking out your feelings while record screen. When you finish recording, click finished.

            (Attention: After you click on each style, please make sure the webpage is SECURE. If not, please use "https://", or the webcam will not be turn on and you will not be able
            to see the artistic filter)

    search: Click this button, you will be lead to the "search" page, where you can type in a keyword and search for it.(But it is invalid for now...)
    browse: Click this button, you will see the "browse" page which contains several "boxes", each of which stands for a Harvard school, and contains emotion cards generated by users in that
            school.
    sunny room: This is a gallery-like room where you store your positive-emotion cards in. You can click on the cards to watch your emotion portraits.
    rainy room: This is a gallery-like room where you store your negative-emotion cards in. You can click on the cards to watch your emotion portraits.
7)When you write a card, you need to fill in the front side and then flip it to play with the back side. After you create your first card, you will be able to write a card with totally
  empty front side.

8)Each time you make a mistake, it will turn to the "apology" page.
9)Notice there is a small gray square on the top-left corner which could extend to a navigation menu when you click on it.


I have tested the platform with several GSD students, and collect self-portraits (videos) from them. You could watch them on the website!

Enjoy!