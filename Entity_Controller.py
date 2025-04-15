class User:
    def __init__(self, user_id, email, name):
        self.user_id = user_id
        self.email = email
        self.name = name

class Tag:
    def __init__(self, name, category, confidence):
        self.name = name
        self.category = category  # 예: '장소', '인물'
        self.confidence = confidence

class Photo:
    def __init__(self, photo_id, file_path, upload_date, status='uploaded'):
        self.photo_id = photo_id
        self.file_path = file_path
        self.upload_date = upload_date
        self.status = status
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)


# Controller for managing photos
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


# Controller for managing tagging
class TagManager:
    def __init__(self):
        pass

    def request_tagging(self, photo):
        # AI 태깅 서비스 호출 시뮬레이션
        sample_tags = [
            Tag("해변", "장소", 0.89),
            Tag("여행", "행사", 0.82)
        ]
        for tag in sample_tags:
            photo.add_tag(tag)
        photo.status = 'tagged'
        print(f"Photo {photo.photo_id} tagging complete.")

    def retag_photo(self, photo):
        print(f"Re-tagging photo {photo.photo_id}... (mock)")
