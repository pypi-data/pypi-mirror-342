"""Docker integration module."""

from typing import Dict, Any, List, Optional
from .tool_base import ToolIntegration

class DockerIntegration(ToolIntegration):
    """Handles Docker specific integrations."""
    
    @staticmethod
    def is_available() -> bool:
        """Check if Docker is available."""
        return ToolIntegration.is_available('docker')
    
    @staticmethod
    def generate_commands(docker_config: Dict[str, Any], working_dir: Optional[str] = None) -> List[str]:
        """Generate Docker specific commands.
        
        Args:
            docker_config: Docker specific configuration
            working_dir: Working directory for Docker operations
            
        Returns:
            List of commands to execute
        """
        commands = []
        
        # Run docker-compose if specified
        if docker_config.get('compose'):
            compose_cmd = "docker-compose"
            if docker_config.get('compose_file'):
                compose_cmd += f" -f {docker_config['compose_file']}"
            compose_cmd += f" {docker_config['compose']}"
            commands.append(compose_cmd)
            
        # Run a container if specified
        if docker_config.get('run'):
            run_config = docker_config['run']
            run_cmd = "docker run"
            
            # Add options
            if run_config.get('detach'):
                run_cmd += " -d"
            if run_config.get('interactive'):
                run_cmd += " -it"
            if run_config.get('ports'):
                for port_map in run_config['ports']:
                    run_cmd += f" -p {port_map}"
            if run_config.get('volumes'):
                for vol_map in run_config['volumes']:
                    run_cmd += f" -v {vol_map}"
            if run_config.get('env'):
                for key, value in run_config['env'].items():
                    run_cmd += f" -e {key}={value}"
            
            # Add image and command
            run_cmd += f" {run_config['image']}"
            if run_config.get('command'):
                run_cmd += f" {run_config['command']}"
                
            commands.append(run_cmd)
            
        # Build an image if specified
        if docker_config.get('build'):
            build_config = docker_config['build']
            build_cmd = f"docker build -t {build_config['tag']}"
            
            if build_config.get('dockerfile'):
                build_cmd += f" -f {build_config['dockerfile']}"
                
            context = build_config.get('context', '.')
            build_cmd += f" {context}"
            
            commands.append(build_cmd)
            
        return commands