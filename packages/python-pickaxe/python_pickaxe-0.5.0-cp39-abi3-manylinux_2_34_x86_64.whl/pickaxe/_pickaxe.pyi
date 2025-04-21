class HtmlDocument:
    """
    A parsed HTML document.
    """
    @classmethod
    def from_str(cls, raw: str) -> HtmlDocument:
        """
        Parse an HTML document from a string.
        """
        ...

    @property
    def raw(self) -> str:
        """
        The raw HTML content of the document.
        """
        ...

    @property
    def root(self) -> HtmlNode:
        """
        Get the root node of the document.
        """
        ...

    @property
    def children(self) -> list[HtmlNode]:
        """
        Get the immediate children of the document.
        """
        ...

    def find_all(self, selector: str) -> list[HtmlNode]:
        """
        Find all nodes matching the given CSS selector.
        """
        ...

    def find_all_xpath(self, xpath: str) -> list[HtmlNode | str | None]:
        """
        Find all nodes matching the given XPath selector.
        """
        ...

    def find(self, selector: str) -> HtmlNode | None:
        """
        Find the first node matching the given CSS selector.
        """
        ...

    def find_xpath(self, xpath: str) -> HtmlNode | str | None:
        """
        Find the first node matching the given XPath selector.
        """
        ...

    def find_nth(self, selector: str, n: int) -> HtmlNode | None:
        """
        Find the nth node matching the given CSS selector.
        """
        ...

    def find_nth_xpath(self, xpath: str, n: int) -> HtmlNode | str | None:
        """
        Find the nth node matching the given XPath selector.
        """
        ...


class HtmlNode:
    @property
    def text(self) -> str:
        """
        The visible text of this node.
        """
        ...

    @property
    def inner_text(self) -> str:
        """
        The inner visible text of the node and its children.
        """
        ...

    @property
    def inner_html(self) -> str:
        """
        The inner HTML of the node and its children.
        """
        ...

    @property
    def outer_html(self) -> str:
        """
        The outer HTML of the node.
        """
        ...

    @property
    def tag_name(self) -> str:
        """
        The tag name of the node.
        """
        ...

    @property
    def attributes(self) -> dict[str, str | None]:
        """
        All attributes of the node.
        """
        ...

    @property
    def children(self) -> list[HtmlNode]:
        """
        The immediate children of the node.
        """
        ...

    def find_all(self, selector: str) -> list[HtmlNode]:
        """
        Find all nodes matching the given CSS selector.
        """
        ...

    def find_all_xpath(self, xpath: str) -> list[HtmlNode | str | None]:
        """
        Find all nodes matching the given XPath selector.
        """
        ...

    def find(self, selector: str) -> HtmlNode | None:
        """
        Find the first node matching the given CSS selector.
        """
        ...

    def find_xpath(self, xpath: str) -> HtmlNode | str | None:
        """
        Find the first node matching the given XPath selector.
        """
        ...

    def find_nth(self, selector: str, n: int) -> HtmlNode | None:
        """
        Find the nth node matching the given CSS selector.
        """
        ...

    def find_nth_xpath(self, xpath: str, n: int) -> HtmlNode | str | None:
        """
        Find the nth node matching the given XPath selector.
        """
        ...

    def get_attribute(self, name: str) -> str | None:
        """
        Get the value of an attribute.
        """
        ...


def html_to_markdown(html: str, skip_tags: list[str] = ["script", "style"]) -> str:
    """
    Convert an HTML string to markdown.
    """
    ...
