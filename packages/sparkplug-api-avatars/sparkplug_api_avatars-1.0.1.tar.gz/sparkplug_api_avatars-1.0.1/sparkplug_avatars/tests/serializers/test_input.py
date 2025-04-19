from django.test import TestCase
from rest_framework.exceptions import ValidationError

from sparkplug_avatars.serializers.input import InputData, InputSerializer


class TestInputSerializer(TestCase):
    def test_valid_file_extension(self):
        # Test with a valid file extension
        data = {"file": "example.jpg"}
        serializer = InputSerializer(data=data)
        assert serializer.is_valid()
        validated_data = serializer.validated_data
        assert validated_data.file == "example.jpg"

    def test_invalid_file_extension(self):
        # Test with an invalid file extension
        data = {"file": "example.txt"}
        with self.assertRaises(ValidationError) as exc_info:
            InputData(file=data["file"])
        assert "file" in exc_info.exception.detail
        assert (
            "File must have one of the following extensions: jpg, jpeg, png"
            in exc_info.exception.detail["file"]
        )

    def test_missing_file_field(self):
        # Test with missing file field
        data = {}
        serializer = InputSerializer(data=data)
        assert not serializer.is_valid()
        assert "file" in serializer.errors
