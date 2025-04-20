import dataclasses


@dataclasses.dataclass
class PackMode:
    """打包模式"""

    MODES = dict(
        archive=("", "压缩"),
        rebuild=("", "重构"),
        debug=("非调试", "调试"),
        offline=("在线", "离线"),
        simplify=("", "简化"),
        use_tk=("", "tk"),
    )

    archive: bool = False  # 压缩包模式
    rebuild: bool = False  # 重构模式
    debug: bool = False  # 调试模式，显示打包时间等信息
    offline: bool = False  # 离线模式
    simplify: bool = False  # 简化模式, 加速pyside等库打包速度
    use_tk: bool = False  # 启用 tk 打包

    def __repr__(self):
        """显示模式信息"""

        mode_str = []
        for k, v in self.__dict__.items():
            prefix = "[red bold]" if int(v) else "[green bold]"
            val = self.MODES.get(k)[int(v)]
            if val:
                mode_str.append(prefix + val + "[/]")

        return f"模式: [{', '.join(mode_str)}]"
