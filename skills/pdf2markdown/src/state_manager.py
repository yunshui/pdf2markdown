"""状态管理模块 - 用于断点续传功能."""

import json
import os
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


class StateManager:
    """管理PDF转换状态，支持断点续传."""

    def __init__(self, output_dir: str, pdf_name: str):
        """初始化状态管理器.

        Args:
            output_dir: 输出目录路径
            pdf_name: PDF文件名（不含扩展名）
        """
        self.output_dir = output_dir
        self.pdf_name = pdf_name
        self.state_file = os.path.join(output_dir, f"{pdf_name}_md", ".state.json")
        self.state = self._load_state()
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """设置中断信号处理器."""
        self._interrupted = False
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        """处理中断信号（Ctrl+C）.

        Args:
            signum: 信号编号
            frame: 当前栈帧
        """
        print("\n\n⚠️  收到中断信号，正在保存状态...")
        self._interrupted = True
        self.save_state()
        print("✓ 状态已保存，可以使用 --resume 继续")
        raise KeyboardInterrupt("转换被中断，状态已保存")

    def _load_state(self) -> Dict:
        """加载状态文件.

        Returns:
            状态字典
        """
        if not os.path.exists(self.state_file):
            return {
                "pdf_name": self.pdf_name,
                "start_time": datetime.now().isoformat(),
                "total_pages": 0,
                "completed_pages": [],
                "failed_pages": [],
                "current_page": 0,
                "page_times": {},
                "total_time": 0,
                "status": "not_started"
            }

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  无法加载状态文件，将重新开始: {e}")
            return {
                "pdf_name": self.pdf_name,
                "start_time": datetime.now().isoformat(),
                "total_pages": 0,
                "completed_pages": [],
                "failed_pages": [],
                "current_page": 0,
                "page_times": {},
                "total_time": 0,
                "status": "not_started"
            }

    def save_state(self):
        """保存当前状态到文件."""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def initialize(self, total_pages: int):
        """初始化转换状态.

        Args:
            total_pages: PDF总页数
        """
        self.state.update({
            "total_pages": total_pages,
            "start_time": datetime.now().isoformat(),
            "completed_pages": [],
            "failed_pages": [],
            "current_page": 0,
            "page_times": {},
            "total_time": 0,
            "status": "in_progress"
        })
        self.save_state()

    def is_page_completed(self, page_num: int) -> bool:
        """检查页面是否已完成.

        Args:
            page_num: 页码（1-indexed）

        Returns:
            True如果页面已完成
        """
        return page_num in self.state.get("completed_pages", [])

    def mark_page_completed(self, page_num: int, duration: float):
        """标记页面为已完成.

        Args:
            page_num: 页码（1-indexed）
            duration: 处理耗时（秒）
        """
        completed = self.state.setdefault("completed_pages", [])
        page_times = self.state.setdefault("page_times", {})

        if page_num not in completed:
            completed.append(page_num)
            page_times[page_num] = duration
            self.state["current_page"] = page_num
            self.state["total_time"] = sum(page_times.values())
            self.save_state()

    def mark_page_failed(self, page_num: int, error: str):
        """标记页面失败.

        Args:
            page_num: 页码（1-indexed）
            error: 错误信息
        """
        failed = self.state.setdefault("failed_pages", [])
        failed.append({
            "page": page_num,
            "error": error,
            "time": datetime.now().isoformat()
        })
        self.state["current_page"] = page_num
        self.save_state()

    def get_completed_pages(self) -> Set[int]:
        """获取已完成的页面集合.

        Returns:
            已完成页码的集合
        """
        return set(self.state.get("completed_pages", []))

    def get_failed_pages(self) -> List[Dict]:
        """获取失败的页面列表.

        Returns:
            失败页面信息列表
        """
        return self.state.get("failed_pages", [])

    def get_average_time(self) -> float:
        """获取平均页面处理时间.

        Returns:
            平均时间（秒），如果没有数据则返回0
        """
        page_times = self.state.get("page_times", {})
        if not page_times:
            return 0.0
        return sum(page_times.values()) / len(page_times)

    def get_estimated_remaining_time(self) -> float:
        """预估剩余时间.

        Returns:
            剩余时间（秒）
        """
        total_pages = self.state.get("total_pages", 0)
        completed = self.state.get("completed_pages", [])
        avg_time = self.get_average_time()

        remaining = total_pages - len(completed)
        return remaining * avg_time

    def get_progress(self) -> Dict:
        """获取当前进度信息.

        Returns:
            包含进度详情的字典
        """
        total_pages = self.state.get("total_pages", 0)
        completed = self.state.get("completed_pages", [])
        failed = self.state.get("failed_pages", [])

        completed_count = len(completed)
        failed_count = len(failed)

        return {
            "total_pages": total_pages,
            "completed": completed_count,
            "failed": failed_count,
            "processed": completed_count + failed_count,
            "remaining": total_pages - completed_count - failed_count,
            "progress_percent": round((completed_count / total_pages * 100) if total_pages > 0 else 0, 2),
            "average_time": self.get_average_time(),
            "estimated_remaining": self.get_estimated_remaining_time(),
            "total_elapsed": self.state.get("total_time", 0),
            "status": self.state.get("status", "unknown")
        }

    def mark_completed(self):
        """标记整个转换完成."""
        self.state["status"] = "completed"
        self.state["end_time"] = datetime.now().isoformat()
        self.save_state()

    def reset(self):
        """重置状态文件."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        self.state = self._load_state()

    def show_progress(self):
        """显示当前进度到控制台."""
        progress = self.get_progress()

        print(f"\n{'='*60}")
        print(f"PDF转换进度: {self.pdf_name}")
        print(f"{'='*60}")
        print(f"总页数: {progress['total_pages']}")
        print(f"已完成: {progress['completed']}")
        print(f"失败: {progress['failed']}")
        print(f"进度: {progress['progress_percent']}%")
        print(f"已用时间: {self._format_time(progress['total_elapsed'])}")
        print(f"预估剩余: {self._format_time(progress['estimated_remaining'])}")
        print(f"平均每页: {self._format_time(progress['average_time'])}")
        print(f"状态: {progress['status']}")
        print(f"{'='*60}")

        if progress['failed'] > 0:
            print("\n失败的页面:")
            for fail in self.state.get("failed_pages", []):
                print(f"  页面 {fail['page']}: {fail['error']}")

    @staticmethod
    def _format_time(seconds: float) -> str:
        """格式化时间显示.

        Args:
            seconds: 秒数

        Returns:
            格式化的时间字符串
        """
        if seconds < 60:
            return f"{int(seconds)}秒"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}分{secs}秒"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours}小时{minutes}分钟"

    def log_progress(self, logger):
        """记录进度到日志.

        Args:
            logger: Logger实例
        """
        progress = self.get_progress()
        logger.info(
            f"Conversion progress: {progress['progress_percent']}% "
            f"({progress['completed']}/{progress['total_pages']} completed)",
            total_pages=progress['total_pages'],
            completed=progress['completed'],
            failed=progress['failed'],
            estimated_remaining=progress['estimated_remaining'],
            average_time=progress['average_time']
        )