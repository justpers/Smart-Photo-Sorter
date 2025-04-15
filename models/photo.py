class Photo:
    def __init__(self, photo_id, file_path, upload_date, status='uploaded'):
        self.photo_id = photo_id
        self.file_path = file_path
        self.upload_date = upload_date
        self.status = status
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)
