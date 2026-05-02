import uvicorn

from app.settings import is_production


def main() -> None:
    production = is_production()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=not production,
        access_log=not production,
        server_header=False,
    )


if __name__ == "__main__":
    main()
