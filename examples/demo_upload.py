from smart_photo_sorter.boundary.photo_upload_ui import PhotoUploadUI
from smart_photo_sorter.controller.photo_controller import PhotoController
from smart_photo_sorter.entity.user import User

if __name__ == "__main__":
    user = User(user_id="u1", email="me@example.com", name="Kim")
    ui = PhotoUploadUI(PhotoController())

    ui.select_photo(user, "examples/cat1.jpg")

    # 결과 확인
    p = user.photos[-1]
    print("\n=== 저장된 Photo 정보 ===")
    print("ID      :", p.photo_id)
    print("File    :", p.file_path)
    print("Tags    :", [(t.name, t.confidence) for t in p.tags])