# This file is part of App3 (http://code.google.com/p/app3).
# 
# Copyright (C) 2009 JJ Geewax http://geewax.org/
# All rights reserved.
# 
# This software is licensed as described in the file COPYING.txt,
# which you should have received as part of this distribution.

import logging
import hmac
import base64
from datetime import datetime

TIMEFORMAT = "%a, %d %b %Y %H:%M:%S +0000"

def generate_auth(request):
    """
    The timestamp format should be as specified in RFC 2822 and in UTC:
        "%a, %d %b %Y %H:%M:%S +0000"
        
    - See http://www.faqs.org/rfcs/rfc2822.html
    """
    params = request.params
    if not params: params = {}
    
    params = '&'.join(["%s=%s" % (key, params[key]) for key in sorted(params.keys())])
    message = "%s\n%s\n%s" % (request.path, params, request.app3_timestamp)
    
    auth = hmac.new(
        key = request.secret_key,
        msg = message,
    ).digest()
    
    return base64.encodestring(auth).strip()

def generate_timestamp():
    """
    Generates a timestamp in the standard format.
    """
    return datetime.utcnow().strftime(TIMEFORMAT)

def is_within_n_minutes(sent_time, n=15):
    """
    Check whether one of our timestamps is within n minutes of
    now. (All times are in UTC)
    """
    sent_time = datetime.strptime(sent_time, TIMEFORMAT)
    diff = abs(datetime.utcnow() - sent_time)
    return diff.seconds < n * 60
    
def is_authorized(request):
    """
    Returns whether a user is authorized based on the request.
    """
    # Need all of the headers to have been passed for authentication
    if not all( (request.app3_auth, request.app3_timestamp) ):
        logging.info('Failed authorization: missing headers.')
        return False
    
    # Time skew... Could be replay attack?
    if not is_within_n_minutes(request.app3_timestamp, 15): 
        logging.info('Failed authorization: not within n minutes.')
        return False
    
    # Check whether we generate the same auth header as they did
    if request.app3_auth != generate_auth(request):
        logging.info('Failed authorization: auth mismatch.')
        return False

    return True
