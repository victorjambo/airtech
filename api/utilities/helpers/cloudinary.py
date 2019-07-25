from os import getenv
from cloudinary import config, uploader


def upload_image(image, image_name):
  """Uploads an imaged to cloudinary
  """

  config(
    cloud_name=getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=getenv('CLOUDINARY_API_KEY'),
    api_secret=getenv('CLOUDINARY_API_SECRET')
  )

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
