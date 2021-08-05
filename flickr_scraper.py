# Generated by Glenn Jocher (glenn.jocher@ultralytics.com) for https://github.com/ultralytics

import argparse
import os
import time

from flickrapi import FlickrAPI

from utils.general import download_uri

def get_urls(search='honeybees on flowers', n=10, download=False, key='', secret='', savedir = None):
    t = time.time()
    flickr = FlickrAPI(key, secret)
    license = ()  # https://www.flickr.com/services/api/explore/?method=flickr.photos.licenses.getInfo
    photos = flickr.walk(text=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
                         extras='url_o',
                         per_page=500,  # 1-500
                         license=license,
                         sort='relevance')

    if download:
        if savedir is None:
            dir = os.getcwd() + os.sep + search.replace(' ', '') + os.sep  # save directory
        else:
            dir = savedir
        if not os.path.exists(dir):
            os.makedirs(dir)

    urls = []
    for i, photo in enumerate(photos):
        if i < n:
            try:
                # construct url https://www.flickr.com/services/api/misc.urls.html
                url = photo.get('url_o')  # original size
                if url is None:
                    url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                          (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size

                # download
                if download:
                    download_uri(url, dir)

                urls.append(url)
                print('%g/%g %s' % (i, n, url))
            except:
                print('%g/%g error...' % (i, n))

    # import pandas as pd
    # urls = pd.Series(urls)
    # urls.to_csv(search + "_urls.csv")
    print('Done. (%.1fs)' % (time.time() - t) + ('\nAll images saved to %s' % dir if download else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', type=str, default='honeybees on flowers', help='flickr search term')
    parser.add_argument('--n', type=int, default=10, help='number of images')
    parser.add_argument('--download', action='store_true', help='download images')
    parser.add_argument('--key', type=str, default='', help='API key')
    parser.add_argument('--secret', type=str, default='', help='API secret')
    parser.add_argument('--savedir', type=str, default='', help='folder where to download images')
    opt = parser.parse_args()

    # Check key
    help_url = 'https://www.flickr.com/services/apps/create/apply'
    #assert key and secret, f'Flickr API key required in flickr_scraper.py L11-12. To apply visit {help_url}'

    get_urls(search=opt.search,  # search term
             n=opt.n,  # max number of images
             download=opt.download, # download images
             key=opt.key,
             secret=opt.secret,
            savedir = opt.savedir)  
