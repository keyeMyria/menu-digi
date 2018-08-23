# menu-digi
# PLEASE READ !!
## Feed back for now
 - This is all I can explain for now, I will get back to you at around 5 pm
 - Right now go through the site ensuring the features of **our agreement** have been implemented
 - Kindly understand that this project has taken a huge toll on me hence I will only implement features that we agreed on, this includes 
 support for fixing any bugs that will be detected and not including support for maintaining and adding more features.
 - A good example is that django by default does not support real-time notifications... implementing one has  not been a joke.
 - I will also like you to test all features to enable finding *bugs* ASAP so that I can fix them, you will probably find some 
 bugs, kindly write a list describing them in addition you can call me to discuss it at the time above( 5 pm)
 - One thing you may encounter is that heroku may throw an error 500 telling you maximum connections exceeded, dont worry this is
 normal as the free account offers to a maximum of 20 database connections per session,( note this is not equivalent to number of
 of users but queries made to the database) it is for this reason I have tried to my level best to implement advance mathematical
 operations to make as little queries as possible, but again if you get this error, please let me know.
 - DEBUG mode is on so you can read the correct error message, I will appreciate screen shots of the error, dont forget to also look 
 out for errors in chrome developer console and screenshot if any.
 - If you are attending the alumni thing at moringa on friday evening let me know so that I can show how the site works in general,
 like I said its pretty complex and explaining to you in person will save us both a lot of time.
 
 ## functionalities as discussed
 ### restaurant
 - restaurant creates an account[ sign up, login,email confirmation, reset password.... included ]
 - the restaurant dashboard offers
  - Profile - edit profile
  - food items - add and edit food items details such as name,category,price,availability,picture
  - food category - add and edit food categories details - name,
  - tables - add and edit tables - details table number
  - orders - see orders in real-time without having to reload the page
           - order details : food items, quantity, price, user details(name,email,contact), order table
  - reviews - add clients reviews that will appear on the restaurant customers page
  
  ## client
  - restaurant/ admin will generate a qr code with the following syntax
      - `websitename.com/customers/<name-of-restaurant>/table/<table-number>`
  - this QR code is place on the relevant site where it can be scanned by the client and be redirected to the above address
      - for example for a restaurant named `subway` and a QR code on table `6` the url should look like `menudigi.com/customers/subway/table/6`
      - note table number must have been created by the restaurant in the back-end otherwise a `404` error is to be expected
      
  - the rest is straight forward client sees menu, adds item to cart ,fills his/her details in a form then presses send order,
  if all goes well they receive a realtime notification telling them `order receive please wait` at the same time the relevant
  restaurant receives the order in realtime without reloading.
  
  Note: they are some details that I have obviuosly left out and will only becoming clear by experimenting with the actual site
                 
## Demo tests
- I have deployed the site to heroku and created a dummy restaurant with the following details 
  - username:`kfc`
  - password: `jak@1865`
  - dummy data such as tables, food items, food categories
 - I would advice that you first try to register your own restaurant before logging into that one
 - Site: [http://menu-digi.herokuapp.com](http://menu-digi.herokuapp.com). login/register through here
 - for an example of a customer link generated from a qr [http://menu-digi.herokuapp.com/customers/KFC/table/1](http://menu-digi.herokuapp.com/customers/KFC/table/1)

## simple explanation for part of the tech used
- menu digi uses django channels, a new advance tech in django that enables you to setup a [web socket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
to communicate to the server in real-time without having to send an http request to the server to get a response.
- implementing this tech to enable events such as push notifications and real time updates is not trivial in django
- First we have to shift from using WSGI server to ASGI 
- next we integrate [redis](https://redis.io/) an  in-memory data structure store, used as a database, cache and message broker 
to enable us to keep record of the sessions in the web sockets.
- Finally we have to deploy to ... and thats where problems start... luckily after more than 37+ I have been able to solve most of this issues.

