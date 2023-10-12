DEBUG: bool = True
MINIMUM_WORD_COUNT: int = 70
CUSTOM_HTML: str = """
    <meta charset="utf-8">
    <style>
    mark{
        background-color: #5DE23C;
    }
    .font8{
        font-size: 0.7em;
    }
    .font7{
        font-size: 0.63em;
    }
    .font6{
        font-size: 0.54em;
    }
    </style>
"""
STYLE_MAP: str = """
    u => u
    b => strong
    i => em
    highlight => mark

    r.underline => u
    r.StyleUnderline => u

    r.Style13ptBold => strong

    r.UnderlineBold => u > strong

    r.Emphasis => u > strong
    r.textbold => u > strong

    p.Shrink => r.font6
"""
