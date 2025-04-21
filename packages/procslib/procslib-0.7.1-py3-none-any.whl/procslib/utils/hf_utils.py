import os
import shutil
import tempfile

from huggingface_hub import HfApi, hf_hub_download


class HfFileHandler:
    def __init__(self):
        # Initialize the Hugging Face API.
        self.api = HfApi()

    @staticmethod
    def is_hf_path(path: str) -> bool:
        """Check if the given path is a Hugging Face URI."""
        return path.startswith("hf://")

    @staticmethod
    def _parse_hf_uri(hf_uri: str):
        """Parse the Hugging Face URI in the format "hf://{owner}/{repo}/{relative_path_in_repo}"."""
        if not hf_uri.startswith("hf://"):
            raise ValueError("Invalid hf_uri format. It should start with 'hf://'.")
        # Remove the "hf://" prefix.
        uri = hf_uri[len("hf://") :]
        # Split into owner, repo name, and file path (relative to repository root).
        parts = uri.split("/", 2)
        if len(parts) < 3:
            raise ValueError("Invalid hf_uri format. Expected format: hf://{owner}/{repo}/{relative_path_in_repo}")
        owner, name, path_in_repo = parts[0], parts[1], parts[2]
        repo_id = f"{owner}/{name}"
        return repo_id, path_in_repo

    def cp_to_hf(self, local_file_path: str, hf_uri: str, private: bool = True):
        """Copy (upload) a local file to a Hugging Face repository.
        If the hf_uri indicates a directory (ends with a slash or has an empty file part),
        the local file's basename is appended.
        """
        repo_id, path_in_repo = self._parse_hf_uri(hf_uri)
        if hf_uri.endswith("/") or not os.path.basename(path_in_repo):
            path_in_repo = path_in_repo.rstrip("/") + "/" + os.path.basename(local_file_path)
        self.api.create_repo(repo_id=repo_id, private=private, exist_ok=True)
        self.api.upload_file(
            path_or_fileobj=local_file_path,
            path_in_repo=path_in_repo,
            repo_id=repo_id,
        )
        print(f"cp {local_file_path} hf://{repo_id}/{path_in_repo}")

    def cp_to_local(self, hf_uri: str, local_file_path: str, revision: str = "main"):
        """Copy (download) a file from a Hugging Face repository to a local path.
        If the local destination is a directory, the downloaded file is placed there
        using the HF file's basename.
        """
        repo_id, path_in_repo = self._parse_hf_uri(hf_uri)
        if os.path.isdir(local_file_path) or local_file_path.endswith(os.path.sep) or local_file_path.endswith("/"):
            local_file_path = os.path.join(local_file_path, os.path.basename(path_in_repo))
        cached_file_path = hf_hub_download(repo_id=repo_id, filename=path_in_repo, revision=revision)
        shutil.copy(cached_file_path, local_file_path)
        print(f"cp {hf_uri} {local_file_path}")

    def load_file(self, hf_uri: str, revision: str = "main") -> str:
        """Loads (downloads) a file from a Hugging Face repository (using an hf:// URI)
        and returns the local cached file path.
        """
        if not self.is_hf_path(hf_uri):
            raise ValueError("load_file requires an hf:// URI.")
        repo_id, path_in_repo = self._parse_hf_uri(hf_uri)
        model_path = hf_hub_download(repo_id=repo_id, filename=path_in_repo, revision=revision)
        print(f"load_file {hf_uri} -> {model_path}")
        return model_path

    def cp(self, src: str, dst: str, private: bool = True, revision: str = "main"):
        """Bidirectional copy. Determines whether the source and destination are local or HF URIs.
        Supports files and directories.
        """
        src_is_hf = self.is_hf_path(src)
        dst_is_hf = self.is_hf_path(dst)

        if not src_is_hf and not dst_is_hf:
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                if os.path.isdir(dst):
                    dst = os.path.join(dst, os.path.basename(src))
                shutil.copy2(src, dst)
            print(f"cp {src} {dst}")

        elif not src_is_hf and dst_is_hf:
            if os.path.isdir(src):
                if not dst.endswith("/"):
                    dst += "/"
                for root, _, files in os.walk(src):
                    for file in files:
                        local_file = os.path.join(root, file)
                        rel_path = os.path.relpath(local_file, src).replace(os.path.sep, "/")
                        dest_hf_uri = dst + rel_path
                        self.cp_to_hf(local_file, dest_hf_uri, private=private)
                print(f"cp {src} {dst}")
            else:
                self.cp_to_hf(src, dst, private=private)

        elif src_is_hf and not dst_is_hf:
            if src.endswith("/"):
                repo_id, src_path_in_repo = self._parse_hf_uri(src)
                if not os.path.isdir(dst):
                    os.makedirs(dst, exist_ok=True)
                files = self.api.list_repo_files(repo_id=repo_id)
                for file in files:
                    if file.startswith(src_path_in_repo):
                        rel_path = os.path.relpath(file, src_path_in_repo)
                        local_dest = os.path.join(dst, rel_path)
                        os.makedirs(os.path.dirname(local_dest), exist_ok=True)
                        self.cp_to_local(f"hf://{repo_id}/{file}", local_dest, revision=revision)
                print(f"cp {src} {dst}")
            else:
                self.cp_to_local(src, dst, revision=revision)

        elif src_is_hf and dst_is_hf:
            if src.endswith("/"):
                repo_id_src, src_path_in_repo = self._parse_hf_uri(src)
                repo_id_dst, dst_path_in_repo = self._parse_hf_uri(dst)
                if not dst.endswith("/"):
                    dst += "/"
                files = self.api.list_repo_files(repo_id=repo_id_src)
                for file in files:
                    if file.startswith(src_path_in_repo):
                        rel_path = os.path.relpath(file, src_path_in_repo)
                        dest_hf_uri = f"hf://{repo_id_dst}/{dst_path_in_repo.rstrip('/')}/{rel_path}"
                        self.cp(f"hf://{repo_id_src}/{file}", dest_hf_uri, private=private, revision=revision)
                print(f"cp {src} {dst}")
            else:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    temp_path = tmp_file.name
                try:
                    self.cp_to_local(src, temp_path, revision=revision)
                    self.cp_to_hf(temp_path, dst, private=private)
                    print(f"cp {src} {dst}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    def rm(self, path: str, revision: str = "main"):
        """Remove (delete) a file or directory.
        For local paths, directories are removed recursively.
        For HF URIs, if the URI ends with '/', all files under that prefix are deleted.
        """
        if not self.is_hf_path(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"rm {path}")
        else:
            repo_id, path_in_repo = self._parse_hf_uri(path)
            if path.endswith("/"):
                files = self.api.list_repo_files(repo_id=repo_id)
                for file in files:
                    if file.startswith(path_in_repo):
                        self.api.delete_file(
                            repo_id=repo_id,
                            path_in_repo=file,
                            revision=revision,
                            commit_message=f"Deleting file {file}",
                        )
                print(f"rm {path}")
            else:
                self.api.delete_file(
                    repo_id=repo_id,
                    path_in_repo=path_in_repo,
                    revision=revision,
                    commit_message=f"Deleting file {path_in_repo}",
                )
                print(f"rm {path}")

    def mv(self, src: str, dst: str, private: bool = True, revision: str = "main"):
        """Bidirectional move. Moves a file or directory from source to destination
        by performing a copy followed by a removal.
        """
        src_is_hf = self.is_hf_path(src)
        dst_is_hf = self.is_hf_path(dst)

        if not src_is_hf and not dst_is_hf:
            shutil.move(src, dst)
            print(f"mv {src} {dst}")

        elif not src_is_hf and dst_is_hf:
            if os.path.isdir(src):
                if not dst.endswith("/"):
                    dst += "/"
                for root, _, files in os.walk(src):
                    for file in files:
                        local_file = os.path.join(root, file)
                        rel_path = os.path.relpath(local_file, src).replace(os.path.sep, "/")
                        dest_hf_uri = dst + rel_path
                        self.cp_to_hf(local_file, dest_hf_uri, private=private)
                shutil.rmtree(src)
                print(f"mv {src} {dst}")
            else:
                self.cp_to_hf(src, dst, private=private)
                os.remove(src)
                print(f"mv {src} {dst}")

        elif src_is_hf and not dst_is_hf:
            if src.endswith("/"):
                repo_id, src_path_in_repo = self._parse_hf_uri(src)
                if not os.path.isdir(dst):
                    os.makedirs(dst, exist_ok=True)
                files = self.api.list_repo_files(repo_id=repo_id)
                for file in files:
                    if file.startswith(src_path_in_repo):
                        rel_path = os.path.relpath(file, src_path_in_repo)
                        local_dest = os.path.join(dst, rel_path)
                        os.makedirs(os.path.dirname(local_dest), exist_ok=True)
                        self.cp_to_local(f"hf://{repo_id}/{file}", local_dest, revision=revision)
                self.rm(src, revision=revision)
                print(f"mv {src} {dst}")
            else:
                self.cp_to_local(src, dst, revision=revision)
                self.rm(src, revision=revision)
                print(f"mv {src} {dst}")

        elif src_is_hf and dst_is_hf:
            if src.endswith("/"):
                repo_id_src, src_path_in_repo = self._parse_hf_uri(src)
                repo_id_dst, dst_path_in_repo = self._parse_hf_uri(dst)
                if not dst.endswith("/"):
                    dst += "/"
                files = self.api.list_repo_files(repo_id=repo_id_src)
                for file in files:
                    if file.startswith(src_path_in_repo):
                        rel_path = os.path.relpath(file, src_path_in_repo)
                        dest_hf_uri = f"hf://{repo_id_dst}/{dst_path_in_repo.rstrip('/')}/{rel_path}"
                        self.cp(f"hf://{repo_id_src}/{file}", dest_hf_uri, private=private, revision=revision)
                self.rm(src, revision=revision)
                print(f"mv {src} {dst}")
            else:
                self.cp(src, dst, private=private, revision=revision)
                self.rm(src, revision=revision)
                print(f"mv {src} {dst}")
