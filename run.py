from TheImageFetcher import TheImageFetcher as img_fetcher

chromedriver_path = '<your chromedriver path>'
query = "wheaten terrier"
img_fetcher.set_chrome_driver(chromedriver_path)
img_fetcher.fetch_images(query)