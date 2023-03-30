def check_url(url):
    # Remove any leading dots or slashes
    cleaned_path = url.lstrip('.\\/')

    # Return the cleaned up path
    return cleaned_path

print(check_url('//index.html/login'))
