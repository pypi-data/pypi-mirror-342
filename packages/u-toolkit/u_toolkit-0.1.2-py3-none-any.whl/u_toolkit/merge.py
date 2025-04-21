from collections.abc import Mapping


def deep_merge_dict(
    target: dict,
    source: Mapping,
):
    """深层合并两个字典

    :param target: 存放合并内容的字典
    :param source: 来源, 因为不会修改, 所以只读映射就可以
    :param exclude_keys: 需要排除的 keys
    """

    for ok, ov in source.items():
        v = target.get(ok)
        # 如果两边都是映射类型, 就可以合并
        if isinstance(v, dict) and isinstance(ov, Mapping):
            deep_merge_dict(v, ov)
        # 如果当前值允许进行相加的操作
        # 并且不是字符串和数字
        # 并且旧字典与当前值类型相同
        elif (
            hasattr(v, "__add__")
            and not isinstance(v, str | int)
            and type(v) is type(ov)
        ):
            target[ok] = v + ov
        # 否则使用有效的值
        else:
            target[ok] = v or ov
