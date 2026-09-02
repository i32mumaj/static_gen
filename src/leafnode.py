from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag == None:
            return self.value

        if self.props:
            ret_v = f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            ret_v = f"<{self.tag}>{self.value}</{self.tag}>"

        return ret_v


    def __repr__(self) -> str:
        ret_v =  {
            "tag": self.tag,
            "value": self.value,
            "props": self.props,
        }

        return str(ret_v)