class Server:
    def __init__(self, attr: dict, panel):
        self._panel = panel

        self.id = attr.get("identifier")
        self.uuid = attr.get("uuid")
        self.name = attr.get("name")
        self.owner = attr.get("server_owner")
        self.node = attr.get("node")
        self.description = attr.get("description", "")
        self.invocation = attr.get("invocation", "")
        self.status = attr.get("status")
        self.sftp_ip = attr.get("sftp_details", {}).get("ip")
        self.sftp_port = attr.get("sftp_details", {}).get("port")
        
        limits = attr.get("limits", {})
        self.memory = limits.get("memory")
        self.disk = limits.get("disk")
        self.cpu = limits.get("cpu")

        relationships = attr.get("relationships", {})
        self.allocations = [
            f'{a["attributes"]["ip"]}:{a["attributes"]["port"]}'
            for a in relationships.get("allocations", {}).get("data", [])
        ]

    def __repr__(self):
        return f"<Server name={self.name}, owner={self.owner}, node={self.node}>"
    
    def _power_action(self, signal: str):
        return self._panel._request(
            "POST",
            f"servers/{self.id}/power",
            json={"signal": signal}
        )
    
    def start(self):
        return self._power_action("start")

    def stop(self):
        return self._power_action("stop")

    def restart(self):
        return self._power_action("restart")
    
    def send_command(self, cmd: str):
        return self._panel._request(
            "POST",
            f"servers/{self.id}/command",
            json={"command": cmd}
        )
    
    def add_subuser(self, email: str, permissions: list):
        permission_keys = [perm["key"] for perm in permissions]
        return self._panel._request(
            "POST",
            f"servers/{self.id}/users",
            json={
                "email": email, 
                "permissions": [
                    "control.start",
                    "control.stop",
                    "control.restart",
                    "control.console"
                ]
            }
        ); print("Successfully added a subuser!")
    
    def list_subusers(self):
        return self._panel._request(
            "GET",
            f"servers/{self.id}/users",
        )
    
    def delete_subuser(self, username: str):
        return self._panel._request(
            "DELETE",
            f"servers/{self.id}/users/{username}"
        )
    
    def rename(self, name: str, description: str):

        data = {"name": name}
        if description is not None:
            data["description"] = description

        return self._panel._request(
            "POST",
            f"servers/{self.id}/settings/rename",
            json=data
        )
    
    def reinstall(self):
        return self._panel._request(
            "POST",
            f"servers/{self.id}/settings/reinstall"
        )
    
