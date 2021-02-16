# Project 1

ENGO 551
This is my **Website** which you can search a book and leave a comment about it.
This website has different parts contains:
1. register for website
2. login to website/ logout the website
3. search a book
4. see the details about the book (ISBN, Title, Author, Year published, and also reviews)
5. Users can leave comments (rate the book from 1 to 5 and leave a text comment as well)
6. API access: Users can make GET request (/api/<isbn>) and see the resulting JSON which follows the specific format
---
- **books.csv file:**   
this file includes all information about books.  
- **import.py file:**   
it reads data from books.csv file and insert data to the database.
- **application.py file:**  
all the routes for this web application is created in this file.  
---
### templates folder:  
- **index.html file:**  
this is the first page and the login page. if you are a new user, you could register.  
- **register.html file:**  
this page is for new users who still do not have an account  
- **search.html file:**  
user can search a book by its ISBN or title or the author. This page could find any matches and show the results after the user submit the information, even if just part of a title, ISBN or author name are typed.  
- **book_single.html file:**  
After choosing one book from search page, the user can see the details about that book in this new page. It also shows the reviews on that book. Users can leave comments and rate the book (from 1 to 5), then submit it.  
---

[**Click here to see the video for demonstrating the project**](https://drive.google.com/file/d/1LdYnHVgSTpfJVLG1lqEjftuBlQf2FvL8/view?usp=sharing)
