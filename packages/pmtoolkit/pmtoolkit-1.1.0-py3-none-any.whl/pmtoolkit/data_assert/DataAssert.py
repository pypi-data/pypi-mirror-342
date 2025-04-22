import json
import os
import uuid
from pathlib import Path
from typing import Dict, List, Literal, Union


class DataAssert:
    """编写数据校验工具类"""

    def __init__(self):
        self.data_assert_set = []

    def success(self, content: str) -> uuid.UUID:
        """快捷添加成功记录"""
        return self.add_assert('success', content)

    def failed(self, content: str) -> uuid.UUID:
        """快捷添加失败记录"""
        return self.add_assert('failed', content)

    def skipped(self, content: str) -> uuid.UUID:
        """快捷添加跳过记录"""
        return self.add_assert('skipped', content)

    # 添加数据校验
    def add_assert(self, result: Literal['success', 'failed', 'skipped'], content: str) -> uuid.UUID:
        """添加一条数据校验

        Args:
            result (Literal['success', 'failed', 'skipped']): 结果类型，只接受以上三种（success、failed、skipped）
            content (str): 校验文本内容

        Returns:
            uuid.UUID: 返回添加该条数据内容的uuid
        """
        data_id = uuid.uuid4()
        self.data_assert_set.append({"result": result, "content": content, "id": data_id})
        return data_id

    def batch_add_assert(self, records: List[Dict[str, Union[str, Dict]]]) -> List[uuid.UUID]:
        """批量添加数据校验"""
        return [self.add_assert(**r) for r in records]

    # 清空所有数据校验
    def clear_assert(self) -> None:
        self.data_assert_set = []

    # 将数据校验写入文件
    def write_assert_file(self, path: Union[str, Path]) -> str:
        """将数据校验写入文件

        Args:
            path (str): 需要写入的文件路径（包含文件名）

        Returns:
            str: 返回文件的绝对路径
        """
        try:
            with open(path, 'w', encoding="utf-8") as file:
                result = [
                    {"result": data["result"], "content": data["content"]}
                    for data in self.data_assert_set
                ]
                json.dump(result, file, ensure_ascii=False)
            self.clear_assert()
            return os.path.abspath(path)

        except Exception as e:
            print(f"数据写入失败：{e}")

    def write_to_assert(self,
                        filename: str = "assert.json") -> str:
        """
        写入到环境变量指定的目录

        Args:
            filename: 输出文件名

        Returns:
            输出文件的绝对路径

        Raises:
            ValueError: 当环境变量未设置时
        """
        base_dir = os.environ.get("ASSERT_PATH_KEY")
        if not base_dir:
            raise ValueError("环境变量：ASSERT_PATH_KEY未设置")

        output_dir = Path(base_dir)

        return self.write_assert_file(output_dir / filename)

    # 删除数据校验
    def delete_assert(self, assert_id: uuid.UUID) -> dict[str, str]:
        """删除一条数据校验

        Args:
            assert_id (uuid.UUID): 需要删除的数据验证id

        Returns:
            dict[str, str]: 返回被删除的内容
        """
        try:
            for data in self.data_assert_set:
                if data["id"] == assert_id:
                    self.data_assert_set.remove(data)
                    return data
        except Exception as e:
            print(f'需要删除的数据验证信息不存在:{e}')

    # 获取数据校验
    def get_assert(self) -> list[dict[str, str]]:
        """获取所有已经添加的数据校验

        Returns:
            list[dict[str, str]]: 返回一个包含已添加数据校验的数组
        """
        return self.data_assert_set
