# import os
# from pathlib import Path

# volume_path = str(Path.home() / "x17" / "data" / "mongo")
# mongo_config = {
#     "name": "x17-mongo",
#     "image": "mongo:7.0",
#     "ports": {
#         "27017/tcp": 27017  # 宿主机:容器
#     },
#     "environment": {
#         "MONGO_INITDB_ROOT_USERNAME": "admin",
#         "MONGO_INITDB_ROOT_PASSWORD": "admin123"
#     },
#     "volumes": {
#         volume_path: {
#             "bind": "/data/db",
#             "mode": "rw"
#         }
#     },
#     "detach": True  # 后台运行
# }

# import docker

# class ContainerManager:
#     def __init__(self):
#         self.client = docker.from_env()

#     def run_container(self, config: dict):
#         return self.client.containers.run(
#             image=config["image"],
#             name=config["name"],
#             ports=config.get("ports"),
#             environment=config.get("environment"),
#             volumes=config.get("volumes"),
#             detach=config.get("detach", True),
#         )

#     def stop_and_remove(self, name: str):
#         try:
#             container = self.client.containers.get(name)
#             container.stop()
#             container.remove()
#         except docker.errors.NotFound:
#             print(f"Container {name} not found.")
            
            
# manager = ContainerManager()
# manager.run_container(mongo_config)

