import datetime as dt
from PIL import Image

from src import clip_service
from src.meme import Meme
from src.qdrant import meme_service

memeImage = Image.open("../resources/test_data/meme2.jpg")
meme = Meme(memeImage, "Bernie Madoff", dt.datetime.now(), "123456789", "123456789", "123456789")
meme_vectors = clip_service.get_vectors(meme.image)

memeImage2 = Image.open("../resources/test_data/croppedmeme2.png")
meme2 = Meme(memeImage2, "Baron Harknonen", dt.datetime.now(), "123456789", "123456789", "123456789")
meme2_vectors = clip_service.get_vectors(meme2.image)

different_meme_image1 = Image.open("../resources/test_data/meme.png")
different_meme1 = Meme(different_meme_image1, "De Moai", dt.datetime.now(), "123456789", "123456789", "123456789")
different_meme1_vectors = clip_service.get_vectors(different_meme1.image)

different_meme_image2 = Image.open("../resources/test_data/different_meme.jpg")
different_meme2 = Meme(different_meme_image2, "Egg", dt.datetime.now(), "123456789", "123456789", "123456789")
different_meme2_vectors = clip_service.get_vectors(different_meme2.image)

similar_plane_meme_image = Image.open("../resources/test_data/similar_plane_meme.jpg")
similar_plane_meme = Meme(similar_plane_meme_image, "Sniper's Dream", dt.datetime.now(), "123456789", "123456789", "123456789")
similar_plane_meme_vectors = clip_service.get_vectors(similar_plane_meme.image)

meme_service.upload_vectors(meme_vectors, {"name": "meme", "sender": meme.sender, "timestamp": meme.timestamp})
meme_service.upload_vectors(different_meme1_vectors, {"name": "unique meme", "sender": different_meme1.sender, "timestamp": different_meme1.timestamp})


print("List of points from cropped meme that match")
points = meme_service.query_vectors(meme2_vectors[0])

print()
print("List of points from similar meme that match")
print(meme_service.query_vectors(similar_plane_meme_vectors[0]))
print("List of points from different meme 2 that match")
print(meme_service.query_vectors(different_meme2_vectors[0]))