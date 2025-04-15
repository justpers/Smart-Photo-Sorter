from models.photo import Photo

class PhotoManager:
    def __init__(self):
        self.photos = []

    def upload_photo(self, photo):
        # 업로드 로직 예시
        self.photos.append(photo)
        print(f"Photo {photo.photo_id} uploaded successfully.")

    def delete_photo(self, photo_id):
        self.photos = [p for p in self.photos if p.photo_id != photo_id]
        print(f"Photo {photo_id} deleted.")

    def find_duplicates(self):
        # 중복 탐지 로직 예시
        print("Finding duplicate photos... (mock)")
