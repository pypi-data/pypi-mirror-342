PIXABAY_API_ENDPOINT_URL = 'https://pixabay.com/api/?'
"""
This endpoint must be called with specific 
parameters to obtain a response. Those parameters
must be 'key' (the API KEY), 'q' (the query to
search) and 'image_type' (with 'photo' or 'video'
according to what type we are looking for).

Those parameters must be concatenated as encoded
url parameters '.../?key=xxx&q=yyy...'.
"""
PIXABAY_VIDEOS_API_ENDPOINT_URL = 'https://pixabay.com/api/videos/?'
"""
This endpoint must be called with specific 
parameters to obtain a response. Those parameters
must be 'key' (the API KEY), 'q' (the query to
search) and 'pretty' (as 'true' or 'false' if we
want the response made pretty).

Those parameters must be concatenated as encoded
url parameters '.../?key=xxx&q=yyy...'.
"""