# Generated by Glenn Jocher (glenn.jocher@ultralytics.com) for https://github.com/ultralytics

import argparse
import os
import time
from tqdm import tqdm 
import pandas as pd
import pickle
from utils.general import download_uri
from custom import customAPI
        


def get_urls(search='honeybees on flowers', n=10, key='', secret='', urls_csv=False):
    t = time.time()
    flickr = customAPI(key, secret)
    license = ()  # https://www.flickr.com/services/api/explore/?method=flickr.photos.licenses.getInfo
    photos = flickr.walk(text=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
                         extras='url_o',
                         per_page=500,  # 1-500
                         license=license,
                         sort='relevance')

    urls = []
    for i, photo in enumerate(photos):
        try:
            # construct url https://www.flickr.com/services/api/misc.urls.html
            url = photo.get('url_o')  # original size
            if url is None:
                url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                      (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size

            urls.append(url)
            # print('%g/%g %s' % (i, n, url))
            if len(urls) == n:
                break
        except:
            print('%g/%g error...' % (i, n))
    if urls_csv:
        pd_urls = pd.Series(urls)
        pd_urls.to_csv("./all_urls.csv")
    return list(set(urls))


def get_user(search='internetarchivebookimages', n=10, key='', secret='', urls_csv=False):
    t = time.time()
    flickr = FlickrAPI(key, secret)
    license = ()  # https://www.flickr.com/services/api/explore/?method=flickr.photos.licenses.getInfo
    photos = flickr.walk_user(user_id=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
                            extras='url_o',
                            per_page=500,  # 1-500
                            license=license,
                            sort='relevance')

    urls = []
    for i, photo in enumerate(photos):
        try:
            # construct url https://www.flickr.com/services/api/misc.urls.html
            url = photo.get('url_o')  # original size
            if url is None:
                url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                      (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size

            urls.append(url)
            # print('%g/%g %s' % (i, n, url))
            if len(urls) == n:
                break
        except:
            print('%g/%g error...' % (i, n))
    if urls_csv:
        pd_urls = pd.Series(urls)
        pd_urls.to_csv("./all_urls.csv")
    return list(set(urls))

def get_group(search='', n=10, key='', secret='', urls_csv=False):
    t = time.time()
    flickr = customAPI(key, secret)
    license = ()  # https://www.flickr.com/services/api/explore/?method=flickr.photos.licenses.getInfo
    photos = flickr.walk_group(group_id=search,  
                            extras='url_o',
                            per_page=500,  # 1-500
                            license=license,)

    urls = []
    for i, photo in enumerate(photos):
        try:
            # construct url https://www.flickr.com/services/api/misc.urls.html
            url = photo.get('url_o')  # original size
            if url is None:
                url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                      (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size

            urls.append(url)
            # print('%g/%g %s' % (i, n, url))
            if len(urls) == n:
                break
        except:
            print('%g/%g error...' % (i, n))
    if urls_csv:
        pd_urls = pd.Series(urls)
        pd_urls.to_csv("./all_urls.csv")
    return list(set(urls))

def download_pictures(urls, save_dir, search, n):
    t = time.time()
    if save_dir is None:
        dir = os.getcwd() + os.sep + search.replace(' ', '_') + os.sep  # save directory
    elif save_dir[-1] != os.sep:
        dir = save_dir + os.sep
    if not os.path.exists(dir):
        os.makedirs(dir)

    # download pictures
    for j, url in enumerate(tqdm(urls[:n])):
        try:
            download_uri(url, dir)
        except:
            pass

    # import pandas as pd
    # urls = pd.Series(urls)
    # urls.to_csv(search + "_urls.csv")
    print('Done. (%.1fs)' % (time.time() - t))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', type=str, default='honeybees on flowers', help='flickr search term')
    parser.add_argument('--n', type=int, default=10, help='number of images')
    parser.add_argument('--download', action='store_true', help='download images')
    parser.add_argument('--get_urls', action='store_true', help='obtain csv files with all urls')
    parser.add_argument('--key', type=str, default='', help='API key')
    parser.add_argument('--secret', type=str, default='', help='API secret')
    parser.add_argument('--save_dir', type=str, default='', help='folder where to download images')
    parser.add_argument('--stream', type=str, default='general', help='where to get images from, one between ["general","user","group"]')
    opt = parser.parse_args()

    # Check key
    help_url = 'https://www.flickr.com/services/apps/create/apply'

    # assert key and secret, f'Flickr API key required in flickr_scraper.py L11-12. To apply visit {help_url}'
    if opt.stream == 'general':
        urls = get_urls(search=opt.search,  # search term
                           n=opt.n,  # max number of images
                           key=opt.key,
                           secret=opt.secret, 
                           urls_csv=opt.get_urls)
    elif opt.stream == 'user':
        urls = get_user(search=opt.search,  # search term
                           n=opt.n,  # max number of images
                           key=opt.key,
                           secret=opt.secret, 
                           urls_csv=opt.get_urls)
    elif opt.stream == 'group':
        urls = get_group(search=opt.search,  # search term
                           n=opt.n,  # max number of images
                           key=opt.key,
                           secret=opt.secret, 
                           urls_csv=opt.get_urls)

    if opt.download:
        download_pictures(urls=urls, save_dir=opt.save_dir, search=opt.search, n =opt.n)
