def parseURL(url):
    parts = url.split('/')
    desiredPart = '/'.join(parts[:3])
    return desiredPart

