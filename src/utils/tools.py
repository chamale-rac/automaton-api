import base64


def extract_svg_height_width(svg_string, HEIGHT_REGEX, WIDTH_REGEX):
    height_match = HEIGHT_REGEX.search(svg_string)
    width_match = WIDTH_REGEX.search(svg_string)
    if height_match is None or width_match is None:
        return None, None
    height = float(height_match.group(1))
    if height_match.group(2) == 'pt':
        height *= 1.25
    width = float(width_match.group(1))
    if width_match.group(2) == 'pt':
        width *= 1.25
    return height, width


def to_base64(svg_string, HEIGHT_REGEX, WIDTH_REGEX):
    height, width = extract_svg_height_width(
        svg_string.decode('utf-8'),  HEIGHT_REGEX, WIDTH_REGEX)
    return base64.b64encode(svg_string).decode('utf-8'), width, height


def get_letter(index):
    if index < 0:
        raise ValueError('Index must be non-negative')
    quotient = index // 26
    remainder = index % 26
    if quotient == 0:
        return chr(ord('A') + remainder)
    else:
        return get_letter(quotient - 1) + chr(ord('A') + remainder)
