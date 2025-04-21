import sphinx
from pathlib import Path
from docutils import nodes
from docutils.parsers.rst import directives
from pygments.lexers import get_all_lexers
from sphinx.highlighting import lexer_classes
from sphinx.util.docutils import SphinxDirective
from sphinx.directives.code import CodeBlock
from fnmatch import fnmatch
from functools import partial

LEXER_MAP = {}
for lexer in get_all_lexers():
    for short_name in lexer[1]:
        LEXER_MAP[short_name] = lexer[0]

CSS_FILES = [
    "tabs_selector.css",
]


class SphinxTabsContainer(nodes.container):
    pass


class SphinxTabsPanel(nodes.container):
    pass


class SphinxTabsTab(nodes.paragraph):
    pass


class SphinxTabsTablist(nodes.container):
    pass


class TabsDirective(SphinxDirective):
    """Top-level tabs directive"""

    has_content = True

    def run(self):
        """Parse a tabs directive"""
        self.assert_has_content()

        node = nodes.container(type="tab-element")
        self.state.nested_parse(self.content, self.content_offset, node)

        return [node]


class TabDirective(SphinxDirective):
    """Tab directive, for adding a tab to a collection of tabs"""

    has_content = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        """Parse a tab directive"""
        self.assert_has_content()

        tab_name = SphinxTabsTab()
        # tab_name["classes"].extend(sorted(self.tab_classes))
        self.state.nested_parse(self.content[0:1], 0, tab_name)
        # Remove the paragraph node that is created by nested_parse
        tab_name.children[0].replace_self(tab_name.children[0].children)

        tab_title = tab_name.children[0].astext()

        # first judge include
        if self.env.config.tabs_include:
            for include in self.env.config.tabs_include:
                if fnmatch(tab_title, include):
                    break
            else:
                return []

        # then judge exclude
        for exclude in self.env.config.tabs_exclude:
            if fnmatch(tab_title, exclude):
                return []

        # Use base docutils classes

        node = nodes.container()
        node["classes"].append("flatten-sphinx-tabs-tab")
        flatten_tab_title_node = nodes.container()
        flatten_tab_title_node.append(nodes.Text(tab_title))
        flatten_tab_title_node["classes"].append("flatten-tab-title")

        node.append(flatten_tab_title_node)
        self.state.nested_parse(self.content[1:], self.content_offset, node)

        return [node]


class GroupTabDirective(TabDirective):
    """Tab directive that toggles with same tab names across page"""

    has_content = True

    def run(self):
        self.assert_has_content()

        node = super().run()
        return node


class CodeTabDirective(GroupTabDirective):
    """Tab directive with a codeblock as its content"""
    has_content = True
    required_arguments = 1  # Lexer name
    optional_arguments = 1  # Custom label
    final_argument_whitespace = True
    option_spec = {  # From sphinx CodeBlock
        "force": directives.flag,
        "linenos": directives.flag,
        "dedent": int,
        "lineno-start": int,
        "emphasize-lines": directives.unchanged_required,
        "caption": directives.unchanged_required,
        "class": directives.class_option,
        "name": directives.unchanged,
    }

    def run(self):
        """Parse a code-tab directive"""
        self.assert_has_content()

        if len(self.arguments) > 1:
            tab_name = self.arguments[1]
        elif self.arguments[0] in lexer_classes and not isinstance(
                lexer_classes[self.arguments[0]], partial
        ):
            tab_name = lexer_classes[self.arguments[0]].name
        else:
            try:
                tab_name = LEXER_MAP[self.arguments[0]]
            except KeyError as invalid_lexer_error:
                raise ValueError(
                    f"Lexer not implemented: {self.arguments[0]}"
                ) from invalid_lexer_error

        # All content parsed as code, so this code-tab directive should contain only code
        code_block = CodeBlock.run(self)

        # Reset to generate tab node
        self.content.data = [tab_name, ""]
        self.content.items = [("", 0), ("", 1)]

        node = super().run()
        if len(node):
            node[0].extend(code_block)
        return node


class _FindTabsDirectiveVisitor(nodes.NodeVisitor):
    """Visitor pattern than looks for a sphinx tabs
    directive in a document"""

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self._found = False

    def unknown_visit(self, node):
        if (
                not self._found
                and isinstance(node, nodes.container)
                and "classes" in node
                and isinstance(node["classes"], list)
        ):
            self._found = "flatten-tab-title" in node["classes"]

    @property
    def found_tabs_directive(self):
        """Return whether a sphinx tabs directive was found"""
        return self._found


def update_context(app, pagename, templatename, context, doctree):
    """Remove sphinx-tabs CSS and JS asset files if not used in a page"""
    if doctree is None:
        return
    visitor = _FindTabsDirectiveVisitor(doctree)
    doctree.walk(visitor)

    include_assets_in_all_pages = False
    if sphinx.version_info >= (4, 1, 0):
        include_assets_in_all_pages = app.registry.html_assets_policy == "always"

    if visitor.found_tabs_directive or include_assets_in_all_pages:
        for css in CSS_FILES:
            app.add_css_file(css)


def setup(app):
    """Set up the plugin"""
    app.add_config_value("tabs_include", [], "")
    app.add_config_value("tabs_exclude", [], "")
    # if not set tabs_include and tabs_exclude, will not use this plugin override sphinx-tabs.tabs
    if not (app.config.tabs_include or app.config.tabs_exclude):
        return
    # override the tabs directive from sphinx-tabs.tabs
    app.add_directive("tabs", TabsDirective, override=True)
    app.add_directive("tab", TabDirective, override=True)
    app.add_directive("group-tab", GroupTabDirective, override=True)
    app.add_directive("code-tab", CodeTabDirective, override=True)
    # add static files
    static_dir = Path(__file__).parent / "static"
    app.connect("builder-inited", (lambda app: app.config.html_static_path.insert(0, static_dir.as_posix())), )
    app.connect("html-page-context", update_context)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
