from flickrapi import FlickrAPI
from flickrapi.core import require_format

class customAPI(FlickrAPI):
    def __init__(self, api_key, secret):
        super().__init__(api_key, secret)

    @require_format('etree')
    def walk_group(self, group_id='', per_page=50, **kwargs):
        """walk_group(self, group_id, per_page=50, ...) -> \
                generator, yields each photo in a group photostream.
        :Parameters:
            group_id
                the group ID, or 'me'
            per_page
                the number of photos that are fetched in one call to
                Flickr.
        Other arguments can be passed, as documented in the
        flickr.groups.pools.getPhotos_ API call in the Flickr API
        documentation, except for ``page`` because all pages will be
        returned eventually.
        .. _flickr.groups.pools.getPhotos:
            https://www.flickr.com/services/api/flickr.groups.pools.getPhotos.html
        Uses the ElementTree format, incompatible with other formats.
        """

        return self.data_walker(self.groups_pools_getPhotos,
                                group_id=group_id, per_page=per_page, **kwargs)
