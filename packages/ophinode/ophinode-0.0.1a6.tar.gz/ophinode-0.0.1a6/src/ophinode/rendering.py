import collections
from typing import Union

from .nodes.base import *

class RenderContext:
    def __init__(self, site: "ophinode.site.Site"):
        self._site = site
        self._current_page = None
        self._current_page_path = None
        self._site_data = {}
        self._page_data = {}
        self._built_pages = {}
        self._expanded_pages = {}
        self._rendered_pages = {}
        self._exported_files = {}

    @property
    def site(self):
        return self._site

    @property
    def current_page(self):
        return self._current_page

    @property
    def current_page_path(self):
        return self._current_page_path

    @property
    def site_data(self):
        return self._site_data

    @property
    def page_data(self):
        return self._page_data.get(self._current_page_path)

    def get_page_data(self, path: str = None):
        return self._page_data.get(
            path if path is not None else self._current_page_path
        )

    @property
    def built_pages(self):
        return self._built_pages

    @property
    def expanded_pages(self):
        return self._expanded_pages

    @property
    def rendered_pages(self):
        return self._rendered_pages

    @property
    def exported_files(self):
        return self._exported_files

class RenderNode:
    def __init__(self, value: Union[OpenRenderable, ClosedRenderable, None]):
        self._value = value
        self._children = []
        self._parent = None

    @property
    def value(self):
        return self._value

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def render(self, context: RenderContext):
        result = []
        depth = 0
        stk = collections.deque()
        stk.append((self, False))
        no_auto_newline_count = 0
        no_auto_indent_count = 0
        total_text_content_length = 0
        text_content_length_stk = collections.deque()
        while stk:
            render_node, revisited = stk.pop()
            v, c = render_node._value, render_node._children
            if isinstance(v, OpenRenderable):
                if revisited:
                    depth -= 1
                    text_content = v.render_end(context)
                    if not (
                        text_content_length_stk
                        and text_content_length_stk[-1]
                            == total_text_content_length
                    ):
                        if (
                            text_content
                            and total_text_content_length
                            and (
                                no_auto_newline_count == 0
                                or no_auto_indent_count == 0
                            )
                        ):
                            text_content = "\n" + text_content
                        if no_auto_indent_count == 0 and text_content:
                            text_content = ("\n"+"  "*depth).join(
                                text_content.split("\n")
                            )
                    result.append(text_content)
                    total_text_content_length += len(text_content)
                    text_content_length_stk.pop()
                    if not v.auto_newline:
                        no_auto_newline_count -= 1
                    if not v.auto_indent:
                        no_auto_indent_count -= 1
                else:
                    text_content = v.render_start(context)
                    if text_content and (
                        (
                            total_text_content_length
                            and no_auto_newline_count == 0
                        )
                        or
                        (
                            text_content_length_stk
                            and text_content_length_stk[-1]
                                == total_text_content_length
                            and no_auto_indent_count == 0
                        )
                    ):
                        text_content = "\n" + text_content
                    if no_auto_indent_count == 0 and text_content:
                        text_content = ("\n"+"  "*depth).join(
                            text_content.split("\n")
                        )
                    result.append(text_content)
                    total_text_content_length += len(text_content)
                    text_content_length_stk.append(total_text_content_length)
                    if not v.auto_newline:
                        no_auto_newline_count += 1
                    if not v.auto_indent:
                        no_auto_indent_count += 1
                    stk.append((render_node, True))
                    depth += 1
            elif isinstance(v, ClosedRenderable):
                if revisited:
                    depth -= 1
                else:
                    text_content = v.render(context)
                    if text_content and (
                        (
                            total_text_content_length
                            and no_auto_newline_count == 0
                        )
                        or
                        (
                            text_content_length_stk
                            and text_content_length_stk[-1]
                                == total_text_content_length
                            and no_auto_indent_count == 0
                        )
                    ):
                        text_content = "\n" + text_content
                    if no_auto_indent_count == 0 and text_content:
                        text_content = ("\n"+"  "*depth).join(
                            text_content.split("\n")
                        )
                    result.append(text_content)
                    total_text_content_length += len(text_content)
                    stk.append((render_node, True))
                    depth += 1
            if not revisited and c:
                for i in reversed(c):
                    stk.append((i, False))
        result.append("\n")
        return "".join(result)

