"""Define HTML node."""

import typing as tp


class HTMLNode:
    """HTML node."""

    def __init__(
        self,
        tag: tp.Optional[str] = None,
        value: tp.Optional[str] = None,
        children: tp.Optional[list["HTMLNode"]] = None,
        props: tp.Optional[dict] = None,
    ) -> None:
        """Inits HTMLNode."""
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """To be overwritten by chil classes."""
        raise NotImplementedError

    def props_to_html(self) -> str:
        """String representantion HTML node attributes."""
        if self.props:
            return " ".join([f'{k}="{v}"' for k, v in self.props.items()])
        return ""

    def __repr__(self) -> str:
        """String representantion of a HTMLNode instance."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """HTML node."""

    def __init__(
        self, value: str, tag: tp.Optional[str] = None, props: tp.Optional[dict] = None
    ) -> None:
        """Inits LeafNode."""
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        """Overwrite `to_html` method.

        Raises:
            ValueError if leaf node has no value.

        Returns:
            A string.
        """
        if not self.value:
            raise ValueError("Leaf node must have a value.")
        if self.tag is None:
            return self.value
        if self.props_to_html():
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        """String representantion of a LeafNode instance."""
        return f"LeafNode({self.tag}, value: {self.value}, {self.props})"
