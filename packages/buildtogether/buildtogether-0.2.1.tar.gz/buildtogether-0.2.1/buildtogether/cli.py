#!/usr/bin/env python
"""
Command-line interface for BuildTogether
"""
import sys
import click
from app import create_app, db
import os
import signal
import subprocess
import time
import socket
from config import Config

# Global variables for server management
SERVER_PID_FILE = os.path.expanduser('~/.btg_server.pid')

@click.group()
def cli():
    """BuildTogether (btg) - Project management for AI projects"""
    pass

# Setup command group
@cli.group()
def setup():
    """Setup and configuration commands"""
    pass

@setup.command('init')
def setup_init():
    """Initialize the Build Together application"""
    click.echo('Initializing BuildTogether application...')
    app = create_app()
    with app.app_context():
        db.create_all()
    click.echo('Initialization complete!')

@setup.command('config')
def setup_config():
    """Configure application settings"""
    click.echo('Configuring application settings...')
    # Configuration logic would go here
    click.echo('Configuration complete!')

# Server command group
@cli.group()
def server():
    """Server management commands"""
    pass

@server.command('start')
@click.option('--port', default=Config.PORT, help='Port to bind to')
@click.option('--host', default='127.0.0.1', help='Host to bind to')
@click.option('--debug', is_flag=True, help='Run in debug mode')
@click.option('--auto-port', is_flag=True, help='Automatically find an available port if specified port is in use')
def server_start(port, host, debug, auto_port):
    """Start the BuildTogether web server"""
    if is_server_running():
        click.echo('Server is already running!')
        return
    
    # Check if port is available or find an available one if auto_port is True
    if auto_port and not is_port_available(port):
        original_port = port
        port = find_available_port(starting_port=original_port)
        click.echo(f'Port {original_port} is in use. Using port {port} instead.')
    
    click.echo(f'Starting BuildTogether server on {host}:{port}')
    
    # Start the server as a subprocess
    cmd = [sys.executable, '-m', 'flask', 'run', '--host', host, '--port', str(port)]
    if debug:
        os.environ['FLASK_DEBUG'] = '1'
    
    server_process = subprocess.Popen(cmd, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)
    
    # Save the PID for later management
    with open(SERVER_PID_FILE, 'w') as f:
        f.write(str(server_process.pid))
    
    click.echo(f'Server started with PID: {server_process.pid}')
    click.echo(f'Access the application at http://{host}:{port}')

@server.command('stop')
def server_stop():
    """Stop the BuildTogether web server"""
    if not is_server_running():
        click.echo('No server is currently running.')
        return
    
    with open(SERVER_PID_FILE, 'r') as f:
        pid = int(f.read().strip())
    
    try:
        os.kill(pid, signal.SIGTERM)
        click.echo(f'Server with PID {pid} has been stopped.')
        os.remove(SERVER_PID_FILE)
    except ProcessLookupError:
        click.echo(f'No process with PID {pid} found. The server might have been stopped already.')
        os.remove(SERVER_PID_FILE)
    except Exception as e:
        click.echo(f'Error stopping server: {e}')

@server.command('restart')
def server_restart():
    """Restart the BuildTogether web server"""
    if is_server_running():
        server_stop()
        time.sleep(1)  # Wait a moment for the server to fully stop
    
    server_start(Config.PORT, '127.0.0.1', False, False)

@server.command('status')
def server_status():
    """Check the status of the BuildTogether web server"""
    if is_server_running():
        with open(SERVER_PID_FILE, 'r') as f:
            pid = f.read().strip()
        click.echo(f'Server is running with PID: {pid}')
    else:
        click.echo('Server is not running.')

# Database command group
@cli.group()
def db():
    """Database management commands"""
    pass

@db.command('init')
def init_db():
    """Initialize the database by creating all tables"""
    click.echo('Initializing the database...')
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
    click.echo('Database initialized!')

@db.command('sample-data')
def create_sample_data():
    """Create sample data for testing the application"""
    click.echo('Creating sample data...')
    # Import needed models
    from app.models import Project, Sprint, Task, Issue
    
    app = create_app()
    with app.app_context():
        # Create a sample project
        project = Project(
            name='Sample AI Project',
            description='This is a sample AI project for testing the application.',
            requirements='- Python 3.8+\n- TensorFlow 2.0+\n- PyTorch 1.8+'
        )
        db.session.add(project)
        db.session.commit()
        
        # Create sample sprints
        sprint1 = Sprint(
            name='Sprint 1: Planning',
            description='Initial planning and requirements gathering',
            status='Completed',
            project_id=project.id
        )
        
        sprint2 = Sprint(
            name='Sprint 2: Development',
            description='Core development of the AI model',
            status='Active',
            project_id=project.id
        )
        
        sprint3 = Sprint(
            name='Sprint 3: Testing',
            description='Testing and validation of the AI model',
            status='Planned',
            project_id=project.id
        )
        
        db.session.add_all([sprint1, sprint2, sprint3])
        db.session.commit()
        
        # Create sample tasks
        tasks = [
            Task(details='Define project scope', completed=True, sprint_id=sprint1.id),
            Task(details='Gather requirements', completed=True, sprint_id=sprint1.id),
            Task(details='Create project timeline', completed=True, sprint_id=sprint1.id),
            
            Task(details='Set up development environment', completed=True, sprint_id=sprint2.id),
            Task(details='Implement core AI algorithms', completed=False, sprint_id=sprint2.id),
            Task(details='Create data pipeline', completed=False, sprint_id=sprint2.id),
            
            Task(details='Create test cases', completed=False, sprint_id=sprint3.id),
            Task(details='Perform unit testing', completed=False, sprint_id=sprint3.id),
            Task(details='Validate model accuracy', completed=False, sprint_id=sprint3.id)
        ]
        
        # Create sample issues
        issues = [
            Issue(details='Unclear requirements for model accuracy', completed=True, sprint_id=sprint1.id),
            Issue(details='Missing data for training', completed=False, sprint_id=sprint2.id),
            Issue(details='Performance issues with large datasets', completed=False, sprint_id=sprint2.id)
        ]
        
        db.session.add_all(tasks)
        db.session.add_all(issues)
        db.session.commit()
        
        click.echo('Sample data created!')

# Helper functions
def is_server_running():
    """Check if the server is currently running"""
    if not os.path.exists(SERVER_PID_FILE):
        return False
    
    with open(SERVER_PID_FILE, 'r') as f:
        pid = int(f.read().strip())
    
    try:
        # Sending signal 0 to a process checks if it's running without actually sending a signal
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        # If we get a permission error, the process exists but is owned by another user
        return True

def is_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except:
            return False

def find_available_port(starting_port=5000, max_port=9000):
    """Find an available port starting from the given port number"""
    for port in range(starting_port, max_port):
        if is_port_available(port):
            return port
    raise RuntimeError(f"Could not find an available port between {starting_port} and {max_port}")

def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 