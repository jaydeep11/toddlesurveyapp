from PIL import Image
import urllib.request

class ImageService(object):
    """Image method to generate and save thumbnail from image_url"""
    @classmethod
    def generate_thumbnail(cls,image_url):
        try:
            image = urllib.request.urlretrieve(image_url)
            image = Image.open(image[0]) 
            
            SIZE = (50, 50) 
            image.thumbnail(SIZE) 
            image.save("temp_image.jpg",format='JPEG')
            return image
        except:
            return None