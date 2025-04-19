import typing

from magic_hour.core import (
    AsyncBaseClient,
    RequestOptions,
    SyncBaseClient,
    default_request_options,
    to_encodable,
    type_utils,
)
from magic_hour.types import models, params


class ImageToVideoClient:
    def __init__(self, *, base_client: SyncBaseClient):
        self._base_client = base_client

    def create(
        self,
        *,
        assets: params.V1ImageToVideoCreateBodyAssets,
        end_seconds: float,
        height: int,
        style: params.V1ImageToVideoCreateBodyStyle,
        width: int,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.V1ImageToVideoCreateResponse:
        """
        Image-to-Video

        Create a Image To Video video. The estimated frame cost is calculated using 30 FPS. This amount is deducted from your account balance when a video is queued. Once the video is complete, the cost will be updated based on the actual number of frames rendered.

        Get more information about this mode at our [product page](/products/image-to-video).


        POST /v1/image-to-video

        Args:
            name: The name of video
            assets: Provide the assets for image-to-video.
            end_seconds: The total duration of the output video in seconds.
            height: The height of the input video. This value will help determine the final orientation of the output video. The output video resolution may not match the input.
            style: Attributed used to dictate the style of the output
            width: The width of the input video. This value will help determine the final orientation of the output video. The output video resolution may not match the input.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        client.v1.image_to_video.create(
            assets={"image_file_path": "api-assets/id/1234.png"},
            end_seconds=5.0,
            height=960,
            style={"prompt": "a dog running"},
            width=512,
            name="Image To Video video",
        )
        ```
        """
        _json = to_encodable(
            item={
                "name": name,
                "assets": assets,
                "end_seconds": end_seconds,
                "height": height,
                "style": style,
                "width": width,
            },
            dump_with=params._SerializerV1ImageToVideoCreateBody,
        )
        return self._base_client.request(
            method="POST",
            path="/v1/image-to-video",
            auth_names=["bearerAuth"],
            json=_json,
            cast_to=models.V1ImageToVideoCreateResponse,
            request_options=request_options or default_request_options(),
        )


class AsyncImageToVideoClient:
    def __init__(self, *, base_client: AsyncBaseClient):
        self._base_client = base_client

    async def create(
        self,
        *,
        assets: params.V1ImageToVideoCreateBodyAssets,
        end_seconds: float,
        height: int,
        style: params.V1ImageToVideoCreateBodyStyle,
        width: int,
        name: typing.Union[
            typing.Optional[str], type_utils.NotGiven
        ] = type_utils.NOT_GIVEN,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> models.V1ImageToVideoCreateResponse:
        """
        Image-to-Video

        Create a Image To Video video. The estimated frame cost is calculated using 30 FPS. This amount is deducted from your account balance when a video is queued. Once the video is complete, the cost will be updated based on the actual number of frames rendered.

        Get more information about this mode at our [product page](/products/image-to-video).


        POST /v1/image-to-video

        Args:
            name: The name of video
            assets: Provide the assets for image-to-video.
            end_seconds: The total duration of the output video in seconds.
            height: The height of the input video. This value will help determine the final orientation of the output video. The output video resolution may not match the input.
            style: Attributed used to dictate the style of the output
            width: The width of the input video. This value will help determine the final orientation of the output video. The output video resolution may not match the input.
            request_options: Additional options to customize the HTTP request

        Returns:
            Success

        Raises:
            ApiError: A custom exception class that provides additional context
                for API errors, including the HTTP status code and response body.

        Examples:
        ```py
        await client.v1.image_to_video.create(
            assets={"image_file_path": "api-assets/id/1234.png"},
            end_seconds=5.0,
            height=960,
            style={"prompt": "a dog running"},
            width=512,
            name="Image To Video video",
        )
        ```
        """
        _json = to_encodable(
            item={
                "name": name,
                "assets": assets,
                "end_seconds": end_seconds,
                "height": height,
                "style": style,
                "width": width,
            },
            dump_with=params._SerializerV1ImageToVideoCreateBody,
        )
        return await self._base_client.request(
            method="POST",
            path="/v1/image-to-video",
            auth_names=["bearerAuth"],
            json=_json,
            cast_to=models.V1ImageToVideoCreateResponse,
            request_options=request_options or default_request_options(),
        )
