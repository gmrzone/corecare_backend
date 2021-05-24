import os


def blog_image_location(instance, filename):
    path = os.path.join("Blog_Images", instance.title, filename)
    return path

def blog_images(instance, filename):
    path = os.path.join("Blog_Images", instance.post.title, filename)
    return path