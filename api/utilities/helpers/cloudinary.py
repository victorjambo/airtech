from os import getenv
from cloudinary import config, uploader

class Cloud:
  config(
    cloud_name=getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=getenv('CLOUDINARY_API_KEY'),
    api_secret=getenv('CLOUDINARY_API_SECRET')
  )

  def upload_image(self, image):
    """Uploads an imaged to cloudinary
    """

    return uploader.upload(image)

  def delete_image(self, public_id):
    """Delete image from cloudinary

    returns: {'result': 'ok'}
    """

    return uploader.destroy(public_id)
