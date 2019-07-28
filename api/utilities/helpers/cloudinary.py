from os import getenv
from cloudinary import config, uploader

class Cloud:
  config(
    cloud_name=getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=getenv('CLOUDINARY_API_KEY'),
    api_secret=getenv('CLOUDINARY_API_SECRET')
  )

  def upload_image(self, image, image_name):
    """Uploads an imaged to cloudinary
    """

    return uploader.upload(
      image,
      public_id=image_name,
      crop='limit',
      width='2000',
      height='2000',
      eager=[{
        'width': 200,
        'height': 200,
        'crop': 'thumb',
        'gravity': 'auto',
        'radius': 20,
        'effect': 'sepia'
      },{
        'width': 100,
        'height': 150,
        'crop': 'fit',
        'format ': 'png'
      }],
      tags=['image_ad', 'NAPI']
    )

  def delete_image(self, public_id):
    """Delete image from cloudinary

    returns: {'result': 'ok'}
    """

    return uploader.destroy(public_id)
