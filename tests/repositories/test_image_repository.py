from repositories.image_repository import ImageRepository

def test_save_image_calls_put_item(mocker):
    table = mocker.MagicMock()
    print(table)
    repo = ImageRepository(table)

    repo.save({"image_id": "123"})

    table.put_item.assert_called_once()
