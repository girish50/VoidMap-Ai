import uvicorn
from app.config import settings

def main():
    print("====================================================")
    print("🌌 VOIDMAP AI ENGINE — BACKEND SERVER STARTING UP...")
    print(f"Host: {settings.HOST}")
    print(f"Port: {settings.PORT}")
    print(f"Database Configured: {settings.DATABASE_URL}")
    print(f"Local Fallback Mode Forced: {settings.FORCE_LOCAL_FALLBACKS}")
    print("====================================================")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    main()
