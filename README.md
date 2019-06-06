# Python Scraper Test

Write a scraper using Python 3 (ideally) or 2.7 that collects all the posts from all of the pages of this thread on
[this](http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591) forum.
Write the results to a comma-separated-values (CSV) file named “thread.csv” which lists the posts by row with
these required fields: post id, name, date of the post (in text form or as is), and post body.

## Python Version used

3.7.3

### Prerequisites

What you need to install and how to install them

```
pip install beautifulsoup4
pip install lxml
```

## Running the program

There are two ways to run this: 

1. Getting progress info as the program runs (through logger).
2. You are only informed if any errors occur.

### Using the first way

To run the program with updates, one needs to run it with a `-v` flag:

```
python old_car_forum_scraper.py -v
```

### Using the second way

To run the program silently with only notification being with error messages: 

```
python old_car_forum_scraper.py
```

## Deployment

The layout of the forum site isn't well organized with it's tables, but still this program is ready through some slight modifications to scrape other similar sites.

## Author

* **Ivan Viro**