import os
import shutil
from pathlib import Path
from typing import List, Union


class FileCopier:
    """文件拷贝工具"""

    @staticmethod
    def copy(
            src_paths: Union[str, Path, List[Union[str, Path]]],
            dst_dir: Union[str, Path]
    ) -> List[Path]:
        """
        批量拷贝文件/目录到目标文件夹

        Args:
            src_paths: 单个文件/目录路径，或路径列表
            dst_dir: 目标目录路径

        Returns:
            成功拷贝的目标路径列表
        """
        if isinstance(src_paths, (str, Path)):
            src_paths = [src_paths]  # 单个文件路径封装至List

        dst_dir = Path(dst_dir)
        dst_dir.mkdir(parents=True, exist_ok=True)
        copied_paths = []

        for src in map(Path, src_paths):
            dst = dst_dir / src.name
            try:
                if src.is_file():
                    shutil.copy2(src, dst)  # 保留元数据
                else:
                    shutil.copytree(src, dst, dirs_exist_ok=True)  # 批量
                copied_paths.append(dst)
            except Exception as e:
                print(f"[Error] Copy failed: {src} -> {dst}\nReason: {e}")

        return copied_paths

    @staticmethod
    def copy_to_extra(
            src_paths: Union[str, Path, List[Union[str, Path]]],
    ) -> List[Path]:
        """
        拷贝文件到环境变量指定的路径下

        Args:
            src_paths: 单个文件/目录路径，或路径列表
            extra_path_key: 环境变量键名
            sub_dir: 在目标路径下创建的子目录（可选）

        Returns:
            成功拷贝的目标路径列表

        Raises:
            ValueError: 当环境变量未设置时抛出
        """
        extra_path = os.environ.get("EXTRA_PATH_KEY")
        if not extra_path:
            raise ValueError("环境变量EXTRA_PATH_KEY未设置")

        target_dir = Path(extra_path)

        return FileCopier.copy(src_paths, target_dir)
