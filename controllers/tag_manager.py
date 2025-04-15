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