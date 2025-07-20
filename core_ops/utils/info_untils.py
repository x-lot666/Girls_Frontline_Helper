import logging


def print_banner(text):
    """
    输出场景开始执行的日志信息，使用等号装饰，并在文字居中对齐。
    第二行只有最左右两边有=,中间用空格填充

    Args:
        text: 文本，字符串类型。
    """
    text_length = len(text)
    total_length = 80  # 根据实际需求调整总长度
    padding = total_length - 2  # 减去左右两边的等号

    if text_length > padding:
        text = text[:padding]  # 截断文本，防止超出长度
        text_length = padding

    left_padding = (padding - text_length) // 3

    middle_line = "=" + " " * left_padding + text

    logging.info("=" * total_length)
    logging.info(middle_line)
    logging.info("=" * total_length)