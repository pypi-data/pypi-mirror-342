from pathlib import Path
import questionary
import typer
from hrms_connect.services import login as login_service
from hrms_connect.services import logout as logout_service
from hrms_connect.services import check_in as check_in_service
from hrms_connect.services import report as report_service
from hrms_connect.services import project_service
from hrms_connect.services import check_out as check_out_service

app = typer.Typer()
TOKEN_FILE = Path("auth_token.json")


@app.command()
def login(
    remove: bool = typer.Option(
        False, "-remove", "-r", help="Remove stored login credentials and exit."
    ),
):
    """
    Login to your HRMS account. Uses cached token if valid.
    """
    if remove:
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
            typer.echo("🧹 Login credentials removed successfully.")
        else:
            typer.echo("⚠️ No login credentials found.")
        raise typer.Exit()

    if not login_service.is_token_expired():
        token = login_service.get_valid_access_token()
        if token:
            typer.echo("✅ Already logged in with a valid token.")
            return

    email = typer.prompt("Enter your email")
    password = typer.prompt("Enter your password", hide_input=True)
    result = login_service.login(email, password)
    typer.echo(result)


@app.command()
def logout():
    """Logout from your HRMS account"""
    result = logout_service.logout()
    typer.echo(result)


@app.command(name="in")
def checkin():
    """Check-in to the HRMS system."""
    existing_check_in = check_in_service.check_existing_check_in()
    if existing_check_in is not None:
        typer.echo("⚠️ Already checked in today.")
        return

    result = check_in_service.check_in()
    typer.echo(result)


@app.command(name="out")
def checkout():
    """Check-out to the HRMS system."""
    existing_check_out = check_out_service.check_existing_check_out()
    if existing_check_out is not None:
        typer.echo("⚠️ Already checked out today.")
        return

    result = check_out_service.check_out()
    typer.echo(result)


@app.command(name="dr")
def report(
    list_reports: bool = typer.Option(
        False, "--list", "-l", help="List submitted reports"
    ),
):
    """
    Submit or list HRMS reports.
    """
    if list_reports:
        result = report_service.list_reports()
        typer.echo(result)
        return

    # Get stored projects
    projects = project_service.list_projects()

    if not projects:
        # If no projects exist, prompt the user to add a new project
        typer.echo("⚠️  No projects available. You need to add a new project.")
        new_project = typer.prompt("Enter the new project title : ")

        # Add new project
        project_service.add_project(new_project)
        projects = project_service.list_projects()  # Refresh the projects list

    # Select project from list
    project_title = questionary.select("Select project title", choices=projects).ask()

    # Select status
    status = questionary.select(
        "Select status", choices=["In Progress", "Completed", "Pending", "On Hold"]
    ).ask()

    # Now handle multiline report summary
    typer.echo("Enter your report summary (Press 'Ctrl+D' or 'Ctrl+C' to finish):")

    report_summary = ""
    while True:
        try:
            line = input()
            report_summary += line + "\n"  # Concatenate each new line
        except (KeyboardInterrupt, EOFError):  # Handle end of input (Ctrl+D or Ctrl+C)
            break

    report_summary = report_summary.strip()  # Clean up any trailing newlines

    # Confirm submission (optional)
    typer.echo("\n📋 Summary Preview:\n" + "-" * 30)
    typer.echo(report_summary)
    if not typer.confirm("Do you want to submit this report?"):
        typer.echo("❌ Report submission cancelled.")
        raise typer.Abort()

    # Call the service function to submit the report
    result = report_service.submit_report(
        project_title=project_title, status=status, report_summary=report_summary
    )

    typer.echo(result)


# Helper function
@app.command(name="pr")
def projects(
    list: bool = typer.Option(False, "--list", "-l", help="List all projects"),
):
    """Manage projects: Add/Delete via UI, or list with -l."""

    if list:
        projects = project_service.list_projects()
        if not projects:
            typer.echo("📭 No projects found.")
        else:
            typer.echo("📁 Project List:")
            for p in projects:
                typer.echo(f" - {p}")
        return

    # Interactive mode if --list is not used
    action = questionary.select(
        "What do you want to do?", choices=["Add", "Delete"]
    ).ask()

    if action == "Add":
        name = questionary.text("Enter project name to add:").ask()
        if name:
            result = project_service.add_project(name.strip())
            typer.echo(result)
        else:
            typer.echo("⚠️ No project name entered.")

    elif action == "Delete":
        current_projects = project_service.list_projects()
        if not current_projects:
            typer.echo("📭 No projects to delete.")
            return

        name = questionary.select(
            "Select project to delete:", choices=current_projects
        ).ask()

        result = project_service.delete_project(name)
        typer.echo(result)


if __name__ == "__main__":
    app()
