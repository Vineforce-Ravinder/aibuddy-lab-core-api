from fastapi import APIRouter
import psutil
from datetime import datetime


class HealthRouter:
    def __init__(self):
        self.router = APIRouter()

        @self.router.get("/health")
        async def health():
            """
            Health check endpoint that returns system status and resource consumption.
            """
            try:
                # Get resource consumption
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory_info = psutil.virtual_memory()
                disk_info = psutil.disk_usage('/')

                # Get process info
                process = psutil.Process()
                process_memory = process.memory_info().rss / (1024 * 1024)  # MB
                process_cpu = process.cpu_percent(interval=0.1)

                return {
                    "status": "ok",
                    "timestamp": datetime.utcnow().isoformat(),
                    "system_resources": {
                        "cpu_percent": round(cpu_percent, 2),
                        "memory": {
                            "total_mb": round(memory_info.total / (1024 * 1024), 2),
                            "available_mb": round(memory_info.available / (1024 * 1024), 2),
                            "used_percent": round(memory_info.percent, 2)
                        },
                        "disk": {
                            "total_gb": round(disk_info.total / (1024**3), 2),
                            "free_gb": round(disk_info.free / (1024**3), 2),
                            "used_percent": round(disk_info.percent, 2)
                        }
                    },
                    "process": {
                        "memory_mb": round(process_memory, 2),
                        "cpu_percent": round(process_cpu, 2)
                    }
                }

            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }, 500
router = APIRouter()

@router.get("/health")
async def health():
    """
    Health check endpoint that returns system status and resource consumption.
    """
    try:
        # Get resource consumption
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        # Get process info
        process = psutil.Process()
        process_memory = process.memory_info().rss / (1024 * 1024)  # MB
        process_cpu = process.cpu_percent(interval=0.1)
        
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "system_resources": {
                "cpu_percent": round(cpu_percent, 2),
                "memory": {
                    "total_mb": round(memory_info.total / (1024 * 1024), 2),
                    "available_mb": round(memory_info.available / (1024 * 1024), 2),
                    "used_percent": round(memory_info.percent, 2)
                },
                "disk": {
                    "total_gb": round(disk_info.total / (1024**3), 2),
                    "free_gb": round(disk_info.free / (1024**3), 2),
                    "used_percent": round(disk_info.percent, 2)
                }
            },
            "process": {
                "memory_mb": round(process_memory, 2),
                "cpu_percent": round(process_cpu, 2)
            }
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }, 500
