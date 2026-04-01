"""
storage/upload_handler.py

Handles file uploads to Supabase Storage.
Supports image compression (Pillow) before upload.

Usage:
    from storage.upload_handler import upload_files
    urls = await upload_files(files, folder="grievances")
"""

import io
import os
import uuid
import mimetypes
from typing import List, Optional
from fastapi import UploadFile, HTTPException

from database import get_supabase, get_bucket

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ── Config ──────────────────────────────────────────────────────
MAX_IMAGE_SIZE_MB = 5
MAX_VIDEO_SIZE_MB = 50
IMAGE_COMPRESS_QUALITY = 82    # JPEG quality (0-100)
IMAGE_MAX_DIMENSION = 1920     # px — resize if larger than this


# ── Helpers ─────────────────────────────────────────────────────

def _is_image(content_type: str) -> bool:
    return content_type.startswith("image/")


def _is_video(content_type: str) -> bool:
    return content_type.startswith("video/")


def _ext_from_content_type(content_type: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/png":  ".png",
        "image/webp": ".webp",
        "video/mp4":  ".mp4",
        "video/quicktime": ".mov",
        "video/x-msvideo": ".avi",
    }
    return mapping.get(content_type, mimetypes.guess_extension(content_type) or ".bin")


def _compress_image(data: bytes, content_type: str) -> bytes:
    """Resize and compress an image using Pillow."""
    if not PIL_AVAILABLE:
        return data
    try:
        img = Image.open(io.BytesIO(data))
        # Convert RGBA → RGB for JPEG compatibility
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        # Resize if too large
        w, h = img.size
        if max(w, h) > IMAGE_MAX_DIMENSION:
            ratio = IMAGE_MAX_DIMENSION / max(w, h)
            img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=IMAGE_COMPRESS_QUALITY, optimize=True)
        return buf.getvalue()
    except Exception:
        return data   # fall back to original if compression fails


# ── Main Upload Function ─────────────────────────────────────────

async def upload_files(
    files: List[UploadFile],
    folder: str = "misc",
    compress_images: bool = True,
) -> List[str]:
    """
    Upload a list of UploadFile objects to Supabase Storage.

    Args:
        files:           List of FastAPI UploadFile objects
        folder:          Sub-folder in the bucket (e.g. 'grievances', 'crime')
        compress_images: Compress images before upload (default True)

    Returns:
        List of public URLs for the uploaded files
    """
    sb     = get_supabase()
    bucket = get_bucket()
    urls: List[str] = []

    for file in files:
        content_type = file.content_type or "application/octet-stream"
        data = await file.read()
        size_mb = len(data) / (1024 * 1024)

        # ── Validate size ──
        if _is_image(content_type) and size_mb > MAX_IMAGE_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"Image '{file.filename}' exceeds {MAX_IMAGE_SIZE_MB}MB limit."
            )
        if _is_video(content_type) and size_mb > MAX_VIDEO_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"Video '{file.filename}' exceeds {MAX_VIDEO_SIZE_MB}MB limit."
            )

        # ── Compress images ──
        if compress_images and _is_image(content_type):
            data = _compress_image(data, content_type)
            content_type = "image/jpeg"   # always JPEG after compression

        # ── Build unique storage path ──
        ext  = _ext_from_content_type(content_type)
        name = f"{folder}/{uuid.uuid4().hex}{ext}"

        # ── Upload to Supabase Storage ──
        response = sb.storage.from_(bucket).upload(
            path=name,
            file=data,
            file_options={"content-type": content_type},
        )

        if hasattr(response, "error") and response.error:
            raise HTTPException(
                status_code=500,
                detail=f"Storage upload failed: {response.error}"
            )

        # ── Get public URL ──
        public_url = sb.storage.from_(bucket).get_public_url(name)
        urls.append(public_url)

    return urls


async def delete_file(storage_path: str) -> bool:
    """
    Delete a file from Supabase Storage by its path (not full URL).
    e.g. delete_file("grievances/abc123.jpg")
    """
    sb     = get_supabase()
    bucket = get_bucket()
    try:
        sb.storage.from_(bucket).remove([storage_path])
        return True
    except Exception:
        return False
