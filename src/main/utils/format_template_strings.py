import string


def template_to_strings(template: str, props: dict) -> str:
    new_template = string.Template(template)
    return new_template.safe_substitute(props)
