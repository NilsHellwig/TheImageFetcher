# TheImageFetcher
TheImageFetcher is a high-performance tool that allows you to quickly extract large amounts of images from Google Images. Depending on the internet connection, it is possible to fetch an image within one second. The tool allows to save the image sources in an external text file and to specify the path where the images should be saved for a search query. 

## Why should I use this tool?

If large amounts of image data are needed to train neural networks in the context of image recognition, Google is of course the best source. TheImageFetcher is very easy to use and is also adapted to the 2021 version of Google Images! 

## Requirements

* Python3 
* [Chrome Driver](https://chromedriver.chromium.org/) - Please make sure to download chromedriver for your currently installed Google Chrome version.

That's it! Just place your chromedriver anywhere you want. Make sure to that you can copy the absolute path of chromedriver!

## How To Use

### Basic Usage

```python
from TheImageFetcher import the_image_fetcher as img_fetcher

chromedriver_path = '/Users/Max_Mustermann/Downloads/chromedriver' # your absolute path of chromedriver!
query = "wheaten terrier" # specify the query for which you want to extract the images

img_fetcher.set_chrome_driver(chromedriver_path) # 
img_fetcher.fetch_images(query)
```

Images are saved with a random id as .jpg in the images folder. 

### Advanced Parameters

## Future

I will try to make the package accessible via pip.
