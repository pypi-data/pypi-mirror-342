import os
import tarfile
import tempfile
from kubernetes import client
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
from grdpcli import logger
import logging
import base64

# logger.setLevel(logging.DEBUG)

class CopyManager:
    def __init__(self, namespace):
        self.namespace = namespace
        self.api = client.CoreV1Api()

    def _check_pod_exists(self, pod_name):
        """Check if pod exists in namespace"""
        try:
            self.api.read_namespaced_pod(name=pod_name, namespace=self.namespace)
            return True
        except ApiException:
            logger.error(f"Pod {pod_name} not found in namespace {self.namespace}")
            return False

    def _copy_from_pod(self, pod_name, pod_file_path, local_path):
        """Copy file from pod to local system"""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # First, check if source is file or directory
                check_type_cmd = f"if [ -d {pod_file_path} ]; then echo 'directory'; elif [ -f {pod_file_path} ]; then echo 'file'; else echo 'none'; fi"
                source_type = stream(
                    self.api.connect_get_namespaced_pod_exec,
                    pod_name,
                    self.namespace,
                    command=['/bin/sh', '-c', check_type_cmd],
                    stderr=True,
                    stdin=False,
                    stdout=True,
                    tty=False
                ).strip()

                if source_type == 'none':
                    logger.error(f"Source path {pod_file_path} does not exist")
                    return False

                logger.debug(f"Source type: {source_type}")

                # Prepare tar command based on source type
                if source_type == 'directory':
                    # For directories, we want to preserve the directory structure
                    tar_command = f"cd {pod_file_path}/.. && tar czf - $(basename {pod_file_path}) | base64"
                else:
                    # For single files, we just tar the file itself
                    tar_command = f"cd $(dirname {pod_file_path}) && tar czf - $(basename {pod_file_path}) | base64"
                
                # Get base64 encoded tar data
                resp = stream(
                    self.api.connect_get_namespaced_pod_exec,
                    pod_name,
                    self.namespace,
                    command=['/bin/sh', '-c', tar_command],
                    stderr=True,
                    stdin=False,
                    stdout=True,
                    tty=False
                )

                # Save tar content to a temporary file
                temp_tar = os.path.join(temp_dir, 'temp.tar.gz')
                                
                # Decode base64 and write to file
                with open(temp_tar, 'wb') as f:
                    f.write(base64.b64decode(resp))

                tar_size = os.path.getsize(temp_tar)
                logger.debug(f"Complete tar file size: {tar_size} bytes")

                if tar_size == 0:
                    logger.error("Received empty tar file")
                    return False

                # Determine the target extraction path
                if os.path.isdir(local_path):
                    target_dir = local_path
                else:
                    target_dir = os.path.dirname(local_path) or '.'

                # Extract files
                with tarfile.open(temp_tar, 'r:gz') as tar:
                    members = tar.getmembers()
                    if not members:
                        logger.error("Tar file contains no files")
                        return False

                    # If copying to a specific file (not directory), rename the first member
                    if not os.path.isdir(local_path):
                        members[0].name = os.path.basename(local_path)

                    # Extract all members
                    tar.extractall(target_dir, members)

                    # Verify extraction
                    if source_type == 'file':
                        final_path = local_path if not os.path.isdir(local_path) else os.path.join(local_path, os.path.basename(pod_file_path))
                        if os.path.exists(final_path):
                            file_size = os.path.getsize(final_path)
                            logger.debug(f"Extracted file size: {file_size} bytes")
                        else:
                            logger.error(f"Failed to find extracted file at {final_path}")
                            return False

                logger.info(f"Successfully copied to {local_path}")
                return True

        except Exception as e:
            logger.error(f"Error copying from pod: {str(e)}")
            logger.debug(f"Full error: {str(e)}", exc_info=True)
            return False

    def _copy_to_pod(self, local_path, pod_name, pod_file_path):
        """Copy file from local system to pod"""
        try:
            if not os.path.exists(local_path):
                logger.error(f"Local file {local_path} does not exist")
                return False

            # Create a temporary tar file
            with tempfile.NamedTemporaryFile(delete=False) as temp_tar:
                with tarfile.open(fileobj=temp_tar, mode='w:gz') as tar:
                    tar.add(local_path, arcname=os.path.basename(local_path))
                
                temp_tar_path = temp_tar.name

                # Prepare target directory in pod
                target_dir = os.path.dirname(pod_file_path) if not pod_file_path.endswith('/') else pod_file_path
                
                # Create target directory if it doesn't exist
                mkdir_cmd = f'mkdir -p {target_dir}'
                stream(
                    self.api.connect_get_namespaced_pod_exec,
                    pod_name,
                    self.namespace,
                    command=['/bin/sh', '-c', mkdir_cmd],
                    stderr=True,
                    stdin=False,
                    stdout=True,
                    tty=False
                )

                # Start the tar process in the pod
                with open(temp_tar_path, 'rb') as f:
                    exec_command = ['/bin/sh', '-c', f'cat > {target_dir}/transfer.tar.gz']
                    resp = stream(
                        self.api.connect_get_namespaced_pod_exec,
                        pod_name,
                        self.namespace,
                        command=exec_command,
                        stderr=True,
                        stdin=True,
                        stdout=True,
                        tty=False,
                        _preload_content=False
                    )

                    # Read and send the tar file in smaller chunks
                    CHUNK_SIZE = 1024 * 1024  # 1MB chunks
                    while True:
                        chunk = f.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        resp.write_stdin(chunk)

                resp.close()

                # Extract the tar file in pod
                extract_cmd = f'cd {target_dir} ; tar xzf transfer.tar.gz || echo "Error extracting tar"; rm -f transfer.tar.gz || echo "Error removing tar"'

                stream(
                    self.api.connect_get_namespaced_pod_exec,
                    pod_name,
                    self.namespace,
                    command=['/bin/sh', '-c', extract_cmd],
                    stderr=True,
                    stdin=False,
                    stdout=True,
                    tty=False
                )

                logger.info(f"Successfully copied {local_path} to {pod_name}:{pod_file_path}")

                # Clean up the temporary tar file
                try:
                    os.remove(temp_tar_path)
                    logger.debug(f"Removed temporary tar file: {temp_tar_path}")
                except Exception as e:
                    logger.error(f"Failed to remove temporary tar file: {str(e)}")

                return True

        except Exception as e:
            logger.error(f"Error copying to pod: {str(e)}")
            return False

    def copy(self, source, destination):
        """Copy files to/from pods"""
        try:
            # Determine the direction of the copy
            if ':' in source:
                # Copying from pod
                pod_path = source.split(':')
                pod_name = pod_path[0]
                pod_file_path = pod_path[1]
                local_path = destination
                
                if not self._check_pod_exists(pod_name):
                    return False

                logger.info(f"Copying from pod {pod_name}:{pod_file_path} to {local_path}")
                success = self._copy_from_pod(pod_name, pod_file_path, local_path)
                
            else:
                # Copying to pod
                pod_path = destination.split(':')
                pod_name = pod_path[0]
                pod_file_path = pod_path[1]
                
                # If the path in the pod ends with /, add the name of the source file
                if pod_file_path.endswith('/'):
                    pod_file_path = os.path.join(pod_file_path, os.path.basename(source))
                
                local_path = source
                
                if not self._check_pod_exists(pod_name):
                    return False

                logger.info(f"Copying from {local_path} to pod {pod_name}:{pod_file_path}")
                success = self._copy_to_pod(local_path, pod_name, pod_file_path)
                
                
            return success
                
        except Exception as e:
            logger.error(f"Error during copy operation: {str(e)}")
            return False