# Blogly 

This is a mock blog app I made for Springboard    

***

### What was this project about?  

This project was an exercise in backend development with Python, Flask, Jinja, and Flask-SQLAlchemy for my PostgreSQL database.  

### What I did:  

I used Flask-SQLAlchemy as an ORM to create models for User, Post, Tag, and a table that tracked the many to many relationship between posts and tags.  

I then used python/flask to define routes for basic CRUD functionality. I rendered HTML templates largely with Jinja, passing along data that I queried based on user input. I utilized Bootstrap to add some basic styling to the app. 

I stayed mindful of keeping my concerns as separate as possible, moving non-view functions to helpers.py.  

I also wrote integration tests for my code (with a test DB) with the python unittest module. 

### What I learned:  

This unit has instilled in me a joy for backend development. I really wasn't sure what to expect when moving to server-side code, but I'm realizing how powerful and flexible a lot of the tech on this end can be, and the joy that comes with seeing my app respond as expected.  

I'm excited to learn more of the tools/frameworks available on this side of the equation. 

### Looking forward:  

I'm excited to learn about authentication on the back end so I can make an app similar to this one (with better styling) in which users are able to create accounts, log in, write their own blog posts and *not* be able to delete anyone else. 


