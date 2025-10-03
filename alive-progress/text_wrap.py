import textwrap

indented_code = """
    def example_function():
        print("Hello, world!")
"""
dedented_code = textwrap.dedent(indented_code)
print("**************")
print(dedented_code)

print("**************")
long_text = "This is a very long string that needs to be wrapped into multiple lines for better readability."
wrapped_lines = textwrap.wrap(long_text, width=20)
print(wrapped_lines)

print("**************")
filled_text = textwrap.fill(long_text, width=20)
print(filled_text)