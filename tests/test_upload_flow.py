from pathlib import Path
from smart_photo_sorter.boundary.photo_upload_ui import PhotoUploadUI
from smart_photo_sorter.controller.photo_controller import PhotoController
from smart_photo_sorter.entity.user import User

SAMPLE = Path("examples/cat1.jpg")

def test_upload_and_auto_tag(tmp_path):
    # Arrange
    user = User(user_id="u1", email="dev@example.com", name="Dev")
    controller = PhotoController()
    ui = PhotoUploadUI(controller)

    # Act
    ui.select_photo(user, str(SAMPLE))

    # Assert
    assert len(user.photos) == 1
    p = user.photos[0]
    assert p.status == "Tagged"
    assert len(p.tags) >= 1
    # 파일이 실제로 저장됐는지
    assert p.file_path.exists()