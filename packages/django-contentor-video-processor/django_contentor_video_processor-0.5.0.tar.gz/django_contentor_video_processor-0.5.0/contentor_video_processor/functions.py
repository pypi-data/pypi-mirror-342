import requests
from django.conf import settings
from django.urls import reverse


def get_webhook_url():
    base_url = getattr(settings, "BASE_URL", "")
    if not base_url:
        return None
    return f"{base_url}{reverse('video_webhook')}"


def process_video(
    download_url,
    upload_url,
    resolution=None,
):

    headers = {
        "Content-Type": "application/json",
        "X-User-Access-Key": settings.CONTENTOR_VIDEO_PROCESSING_ACCESS_KEY,
        "X-User-Access-Token": settings.CONTENTOR_VIDEO_PROCESSING_ACCESS_TOKEN,
    }

    config = {
        "download_provider": settings.CONTENTOR_VIDEO_PROCESSING_DOWNLOAD_PROVIDER,
        "upload_provider": settings.CONTENTOR_VIDEO_PROCESSING_UPLOAD_PROVIDER,
        "download_url": download_url,
        "upload_url": upload_url,
        "download_access_key": settings.AWS_ACCESS_KEY_ID,
        "download_access_secret": settings.AWS_SECRET_ACCESS_KEY,
        "upload_access_key": settings.AWS_ACCESS_KEY_ID,
        "upload_access_secret": settings.AWS_SECRET_ACCESS_KEY,
        "crf": "30",
        "preset": "veryfast",
        "optimise_for_web": True,
        "webhook_url": getattr(settings, "CONTENTOR_WEBHOOK_URL", get_webhook_url())
    }

    if resolution:
        config["resolution"] = resolution

    try:
        response = requests.post(
            settings.CONTENTOR_VIDEO_PROCESSING_API_URL, headers=headers, json=config
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Video processing for {resolution} submitted successfully!")
            print(f"Job ID: {result.get('id')}")
            print(f"Status: {result.get('status')}")
            return result.get("id")
        else:
            print(
                f"❌ Error processing {resolution}: {response.status_code} - {response.text}"
            )

    except Exception as e:
        print(f"🔥 Exception while processing video at {resolution}: {str(e)}")