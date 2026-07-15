class HTMLNode:
    def __init__(self, tag:str|None = None, value:str|None = None, children:list[HTMLNode]|None = None, props:dict|None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def prop_to_html(self) -> str:
        return_str = ''
        if self.props:
            for key, val in self.props.items():
                return_str += f'{key}="{val}" '

        return return_str.strip()
    
    def __repr__(self) -> str:

        # HTMLNode(TAG, VALUE, CHILDREN, PROPS)
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):

    # Doesn't accept children
    def __init__(self, tag: str | None, value: str, props: dict | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError('All leaf nodes must have a value')
        
        if not self.tag:
            return self.value
    
        return f'<{self.tag} {self.prop_to_html()}>{self.value}</{self.tag}>' if self.props else f'<{self.tag}>{self.value}</{self.tag}>'
    
    def __repr__(self) -> str:

        # LeafNode(TAG, VALUE, PROPS)
        return f"LeafNode({self.tag}, {self.value}, {self.props})"