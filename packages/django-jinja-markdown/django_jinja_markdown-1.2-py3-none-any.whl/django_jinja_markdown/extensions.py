import jinja2
import markdown
from jinja2.ext import Extension


class MarkdownExtension(Extension):
    tags = {"markdown"}

    def __init__(self, environment):
        super().__init__(environment)
        environment.extend(
            markdowner=markdown.Markdown(extensions=["tables", "codehilite", "fenced_code", "toc", "nl2br"])
        )

    def parse(self, parser):
        """
        Parse template code.

        :param parser:  - Jinja2 parser;
        :return:        - markdown result.
        """

        lineno = next(parser.stream).lineno
        body = parser.parse_statements(["name:endmarkdown"], drop_needle=True)
        return jinja2.nodes.CallBlock(self.call_method("_markdown_support"), [], [], body).set_lineno(lineno)

    def _markdown_support(self, caller):
        """
        Parse template with markdown.

        :param caller:  - caller of method;
        :return:        - parsed template.
        """
        return self.environment.markdowner.convert(caller()).strip()
