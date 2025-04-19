from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.permissions import IsAuthenticated
from sparkplug_core.utils import get_validated_dataclass

from ..models import Avatar
from ..serializers import AvatarDetailSerializer, InputData, InputSerializer
from ..tasks import process_avatar_task


class UploadView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (CamelCaseMultiPartParser,)

    def post(self, request: Request) -> Response:
        validated_data: InputData = get_validated_dataclass(
            InputSerializer,
            input_data=request.data,
        )

        instance, _ = Avatar.objects.update_or_create(
            creator=request.user,
            defaults={"file": validated_data.file},
        )

        process_avatar_task(instance.uuid)()

        return Response(
            data=AvatarDetailSerializer(instance).data,
            status=status.HTTP_200_OK,
        )
