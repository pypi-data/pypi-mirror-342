class Permissions:
    """Defines available permissions for subusers with descriptions."""

    # Control Permissions
    console = {"key": "control.console"}
    start = {"key": "control.start"}
    stop = {"key": "control.stop"}
    restart = {"key": "control.restart"}
    
    # User Permissions
    create_user = {"key": "user.create"}
    read_user = {"key": "user.read"}
    update_user = {"key": "user.update"}
    delete_user = {"key": "user.delete"}

    # File Permissions
    create_file = {"key": "file.create"}
    read_file = {"key": "file.read"}
    readcontent_file = {"key": "file.read-content"}
    file_update = {"key": "file.update"}
    file_delete = {"key": "file.delete"}
    file_archive = {"key": "file.archive"}
    sftp = {"key": "file.sftp"}

    # Backup Permissions
    backup_create = {"key": "backup.create"}
    backup_read = {"key": "backup.read"}
    backup_delete = {"key": "backup.delete"}
    backup_download = {"key": "backup.download"}
    backup_restore = {"key": "backup.restore"}

    # Allocation Permissions
    alloc_read = {"key": "allocation.read"}
    alloc_create = {"key": "allocation.create"}
    alloc_update = {"key": "allocation.update"}
    alloc_delete = {"key": "allocation.delete"}

    # Startup Permissions
    startup_read = {"key": "startup.read"}
    startup_update = {"key": "startup.update"}
    startup_docker = {"key": "startup.docker-image"}

    # Database Permissions
    db_create = {"key": "database.create"}
    db_read = {"key": "database.read"}
    db_update = {"key": "database.update"}
    db_delete = {"key": "database.delete"}
    db_viewpwd = {"key": "database.view_password"}

    # Schedule Permissions
    schedule_create = {"key": "schedule.create"}
    schedule_read = {"key": "schedule.read"}
    schedule_update = {"key": "schedule.update"}
    schedule_delete = {"key": "schedule.delete"}

    # Settings Permissions
    settings_rename = {"key": "settings.rename"}
    settings_reinstall = {"key": "settings.reinstall"}

    # Activity Permissions
    activity_read = {"key": "activity.read"}