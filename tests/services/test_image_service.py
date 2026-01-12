from services.image_service import ImageService

def test_create_image_success(mock_repo, mock_s3, mocker):
    mocker.patch("services.image_service.uuid4", return_value="img-123")

    service = ImageService(mock_repo, mock_s3)

    result = service.create_image(
        owner_id="test123",
        content_type="image/png",
        size_bytes=100,
        tags=["profile"]
    )

    assert result["image_id"] == "img-123"
    mock_repo.save.assert_called_once()
    mock_s3.generate_upload_url.assert_called_once()


def test_get_image_not_found(mock_repo, mock_s3):
    mock_repo.get.return_value = None

    service = ImageService(mock_repo, mock_s3)

    try:
        service.get_image("missing-id")
        assert False
    except ValueError as e:
        assert "not found" in str(e)
