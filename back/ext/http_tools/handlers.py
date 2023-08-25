from fastapi import Request, Response


async def handler409(request: Request, exception: Exception):
    return Response(content=str(exception), status_code=409)


async def handler404(request: Request, exception: Exception):
    return Response(content=str(exception), status_code=404)
