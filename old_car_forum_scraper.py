# requires pip install of beaitfulsoup4, lxml
from bs4 import BeautifulSoup
import csv
import logging  # for debugging/tracking progress in execution
import sys
import urllib.request

# creates a beautifulsoup out of the given url, then if table is of expected
# format, it goes to the first node & calls to scrape it; called each url index
def retrieve_posts(url, posts_gathered):
    posts = []
    try:
        post_group = BeautifulSoup(urllib.request.urlopen(url),
                                   'lxml').find('table', class_='forumline')
    except:
        logging.error('Error: no matching table found in given url: {}'
                      .format(url))
        return False
    try:
        for node in post_group:
            if node.name:
                head_node = node.find('span', class_='postbody')
                if head_node:
                    post = retrieve_post_properties(node)
                    posts.append(post)
    except:
        logging.error('There was an error with the requested url: {}'
                      .format(url))
        return False

    if len(posts):
        logging.info('{} additional posts scraped.'.format(str(len(posts))))
        posts_gathered.extend(posts)
        return True
    else:
        return False


# collects the properties of each post and returns them
def retrieve_post_properties(node):
    post_id_stub = node.find(lambda tag: tag.has_attr('name'))
    post_id = post_id_stub['name']
    name = str(post_id_stub.find_next_sibling().get_text())
    date = str(node.find_all_next('span', class_='postdetails'))
    i = date.find('Posted:')
    j = date.find('m<spa')
    date = date[i+8:j+1]
    body = parse_body(node.find('span', class_='postbody'))
    post_properties = {
        'post_id': post_id,
        'name': name,
        'date': date,
        'body': body
    }
    return post_properties


# this cleans up the text of the post and makes it more readable
def parse_body(node):
    text = node.get_text().strip()
    if len(text) < 1:
        return parse_body(node.find_next('span', class_='postbody'))

    if ('__________' in text):
        text = text.split('_________')[0].strip()

    return text.replace('\n', '').replace('\r', '')


# generates a csv file with the posts & all the data in it
def format_to_csv(posts):
    with open('threads.csv', 'w') as file:
        properties = posts[0].keys()
        dictionary_writer = csv.DictWriter(file, fieldnames=properties)
        dictionary_writer.writeheader()
        for post in posts:
            dictionary_writer.writerow(post)


def main():
    url = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/viewtopic.php?t=12591&postdays=0&postorder=asc&start='
    index = 0
    INDEX_UPDATE = 15
    posts_gathered = []
    if '-v' in sys.argv:
        logging.basicConfig(level=logging.INFO)

    logging.info('Fetching posts...')
    # the index & url change by +15 (max of 15 posts are displayed per page)
    while retrieve_posts(str(url+str(index)), posts_gathered):
        index += INDEX_UPDATE

    if len(posts_gathered) > 0:
        logging.info('Writing to csv...')
        format_to_csv(posts_gathered)
        logging.info('Complete! {} posts have been scraped.'
                     .format(len(posts_gathered)))
    else:
        logging.error('No posts have been found.')


# in case this is to be called from a module in the future
if __name__ == '__main__':
    main()
