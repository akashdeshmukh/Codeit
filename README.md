CodeIt
======================================

* Description :-
-----------------------------------------------------------------------------
Online judge written in Django( python framework) for coding competition 
organized at VIT, PUNE.It supports different languages like C, C++, Java, 
Python. For evalution of programs, we are allowing user to execute program 
under limeted no. of system signals. Program will evaluated over standard 
input, standard output. As django supports ORM , codeit can work over Sqlite, 
MySQL,PostgreSQL or any django compatible database. Ranking is dynamically 
updated for user on submitting correct program for problem statement. 

* Installation :-
------------------------------------------------------------------------------
Assuming you are using Linux distro.

1. Clone this repository.
  ```
  git clone https://github.com/tripples/CJ.git
  ```
  Make sure that this repository is copied in your home .
  E.g My home path is '/home/sanket' So ultimate path for repository will be 
  '/home/sanket/CJ/'
 
2. Install python dependencies.
  ```
  sudo pip install -r requirements.txt
  ```

3. Change USR variable in CJ/settings.py
   Set USR variable as your username.

4. Create database and 
  Enter database settings in CJ/settings.py
  ```
  python manage.py syncdb
  ```
  When you run above command, create superuser.
  Enter name and password for admin.

5. Start server.
  ```
  python manage.py runserver
  ```

6.  Open localhost:8000 in browser.
    At first time your database will be empty.
    So add entries through admin first.
    Receipt no should be in database to access other pages.

* Contributors :- 
-----------------------------------------------------------------
 Sanket Sudake [ sanketsudake@gmail.com ]
 Nikhil Pachpande [ pachpandenikhil@gmail.com ]
 Prathamesh Sonpatki
