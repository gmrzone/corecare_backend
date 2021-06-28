import os


def blog_image_location(instance, filename):
    path = os.path.join("Blog_Images", instance.slug, filename)
    return path

def blog_image_placeholder_location(instance, filename):
    path = os.path.join("Blog_Placeholder", instance.slug, f"placeholder_{filename}")
    return path

def blog_images(instance, filename):
    path = os.path.join("Blog_Images", filename)
    return path