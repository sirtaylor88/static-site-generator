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
