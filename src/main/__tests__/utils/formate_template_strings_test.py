from main.utils.format_template_strings import template_to_strings


def test_template_strings():
    template = "Hello, ${name}!"
    name = "John"

    results = template_to_strings(template, {"name": name})

    assert results == "Hello, John!"
