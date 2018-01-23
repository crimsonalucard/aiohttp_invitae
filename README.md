Description:
This framework is aiohttp. aiohttp is an http framework that utilizes
coroutines. Coroutines is the latest and greatest way of doing asyncIO
in nodejs. Python3 happens to support this as well. Additionally, I use uvloop
as a library which integrates nodejs's underlying async implementation in C (libuv)
with python. This makes this python server run at the speed of nodejs. Unlike the standard
python deployment, this server should theoretically handle 10k concurrent connections. 

Additionally, I use the latest python3 type annotations to type check
with mypy. 

The code is pretty straight forward. However I use a unique pattern in views.
Essentially the views return raw sql data instead of responses. The pattern
I use is to have all data wrangling and conversion handled by decorators.
This makes all the views more precise and to the point with data transformation
abstracted away from the intention of the code for readability and modularity. 

Front end is written with react. Honestly it's a horrible frontend, but it gets the job
done. I'm more of a backend guy, but I consider myself pretty good with front end and core 
javascript. Please take note that I did not know anything about react prior to building the 
front end, I had to put in extra time to learn react. 

Unfortunately, I did not have time to implement unit tests.
I did implement type checking in python which is a layer of checks and balances
that has in certain respects as much if not more coverage then unit tests. 


This code is not up to my standards. Typically I like 
to implement type checking, unit testing, and cleaner better designed frontend. 
I would've deployed as well given more time. Some factors that influenced this:

1. It took the recruiter 5 days to answer my questions. It may be because he was 
busy or the engineers were busy. Not trying to blame, anyone or anything but,
this really effected the amount of time I had to work on this. 

2. I do not know react. I had to learn it before this assignment was due.

Overall it was an interesting assignment. Hopefully, although it is not up to my best coding
standards it displays my capabilities.  


Steps:
Install everything in the requirements file.

Load up a postgresql database and create a table called
variants using the schema.sql file, under postgres.public.

then load the data into the data base using postgres_public_variants.sql

run the server using ./main.py

make sure you have the latest version of python

you can type check on python using mypy
run: mypy main.py 

You will also need redis installed on your local computer.

Front end can be run by running: npm start run


