from ports.api.v1.schemas import DeviceTokenPayload
from fastapi import APIRouter, Depends, Response

from ports.api.v1.dependencies import get_device_service
from services import DeviceService


router = APIRouter(tags=["Device"])


@router.put("/api/v1/devices/{device_id}/token", status_code=200)
async def set_device_token(
        device_id: str,
        payload: DeviceTokenPayload,
        device_service: DeviceService = Depends(get_device_service),
):
    await device_service.set_device_token(device_id=device_id, token=payload.push_token)
    return {"ok": True}
