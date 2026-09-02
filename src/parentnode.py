from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("Parent node must have a tag")
        if self.children == None:
            raise ValueError("Parent node must have children/s")

        children_text = ""

        for child in self.children:
            children_text += child.to_html()

        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{children_text}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_text}</{self.tag}>"
  