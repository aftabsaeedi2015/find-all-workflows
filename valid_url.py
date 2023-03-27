def check_url(url):
    if not url.startswith('/'):
        return url
    for i in range(len(url)):
        if url[i] == '/':
            if i < len(url) - 2 and url[i+1]!='/':
                if url[i+1]=='.':
                    if url[i+2]=='.':
                        return url[i+3:]
                    else:
                        return url[i+2:]
                else:
                    return url[i+1:]
    return None

print(check_url('actions/Catalog.action?viewProduct=&productId=FL-DSH-01'))
