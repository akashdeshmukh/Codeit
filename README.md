CodeIt
======================================

Simple app in Django
------------------------------------------------------------

Installation:

1. Clone this repository.
  ```
  https://github.com/tripples/CJ.git
  cd CJ/
  ```
   Use xdot to know about used models.
   ```
   xdot packages_No_Name.dot
   xdot classes_No_Name.dot
   ```

2. Install python dependencies.
  ```
  sudo pip install -r requirements.txt
  ```

3. Create database
  ( Ensure you have installed sqlite3 or set your database settings
  in settings.py )
  ```
  python manage.py syncdb
  ```
  When you run above command, create superuser.
  Enter name and password for admin.

4. Start server.
  ```
  python manage.py runserver
  ```

5.  Open localhost:8000 in browser.
    At first time your database will be empty.
    So add entries through admin first.
    Receipt no should be in database to access other pages.

-----------------------------------------------------------------
