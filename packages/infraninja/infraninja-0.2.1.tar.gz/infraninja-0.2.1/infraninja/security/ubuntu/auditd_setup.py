from importlib.resources import files as resource_files
from pyinfra.api import deploy
from pyinfra.operations import files, systemd


@deploy("Auditd Setup")
def auditd_setup():
    # Get template paths using importlib.resources
    template_dir = resource_files("infraninja.security.templates.ubuntu")
    rules_path = template_dir.joinpath("auditd_rules.j2")
    logrotate_path = template_dir.joinpath("auditd_logrotate.j2")

    # Upload auditd rules from template
    files.template(
        name="Upload custom audit.rules",
        src=str(rules_path),
        dest="/etc/audit/rules.d/audit.rules",
        create_remote_dir=True,
    )

    # Apply log rotation configuration for auditd from template
    files.template(
        name="Upload auditd logrotate config",
        src=str(logrotate_path),
        dest="/etc/logrotate.d/audit",
    )

    systemd.service(
        name="Enable and start auditd",
        service="auditd",
        running=True,
        enabled=True,
    )

    systemd.service(
        name="Restart auditd to apply new rules",
        service="auditd",
        restarted=True,
    )
