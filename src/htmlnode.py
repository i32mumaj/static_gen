class HTMLNode:
    def __init__(self, tag: str | None = None, value: str| None = None, children = None, props: dict[str, str]| None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented yet")

    def props_to_html(self) -> str:

        if self.props == None: return ""

        ret_v = ""

        for k,v in self.props.items():
            if ret_v == "":
                ret_v += f"{k}=\"{v}\""
            else:
                ret_v += f" {k}=\"{v}\""
            
        return ret_v

    def __repr__(self) -> str:
        ret_v =  {
            "tag": self.tag,
            "value": self.value,
            "children": self.children,
            "props": self.props,
        }

        return str(ret_v)