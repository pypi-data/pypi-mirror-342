from __future__ import annotations

import base64
import os
import sys

PARAMS_SEP = '|'
NESTED_SEP = '--'
ITEMS_SEP = '\n'
BLOCK_SEP = '---'
PARAM_PREFIX = 'param'


class MenuItem:
    def __init__(self, text, **params):
        self.text = text
        self.params = params
        self.items = []

    def add_item(self, text, **params) -> MenuItem:
        # https://github.com/swiftbar/SwiftBar?tab=readme-ov-file#parameters
        if params.pop('sep', False):
            self.add_sep()
        pos = params.pop('pos', None)
        new_item = MenuItem(text, **params)
        if pos is None:
            self.items.append(new_item)
        else:
            self.items.insert(pos, new_item)
        return new_item

    def add_sep(self) -> MenuItem:
        return self.add_item(BLOCK_SEP)

    def add_link(self, text, href, **params) -> MenuItem:
        return self.add_item(text, href=href, **params)

    def add_image(self, image_path, text='', **params) -> MenuItem:
        with open(image_path, 'rb') as f:
            base64_image = base64.b64encode(f.read()).decode('utf-8')
        return self.add_item(text, image=base64_image, **params)

    def add_action(self, text, action_params: list[str], **params) -> MenuItem:
        action_params_mapped = {
            f'{PARAM_PREFIX}{idx}': param for idx, param in enumerate(action_params)
        }

        combined_params = {
            'bash': os.getenv('SWIFTBAR_PLUGIN_PATH', sys.argv[0]),
            **action_params_mapped,
            'refresh': 'false',
            'terminal': 'false',
            **params
        }

        return self.add_item(text, **combined_params)

    def render(self, depth=0) -> str:
        rendered_params = ' '.join(f'{k}={v}' for k, v in self.params.items())
        sep1 = ' ' if depth > 0 else ''
        sep2 = PARAMS_SEP if rendered_params else ''
        title = (NESTED_SEP * depth) + sep1 + \
            self.text + sep2 + rendered_params
        sep = ITEMS_SEP if self.items else ''
        return title + sep + ITEMS_SEP.join([
            item.render(depth + 1) for item in self.items
        ])

    def clear(self) -> None:
        self.items.clear()

    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.render()

    def __getitem__(self, index):
        return self.items[index]


class Menu(MenuItem):
    def __init__(self, text='', **params):
        self.items = []
        self.header_last = 0
        if text:
            self.add_item(text, **params)
            self.header_last = 1
        self.add_sep()

    def add_header(self, text, **params) -> MenuItem:
        if params.pop('sep', False):
            raise ValueError('Header cannot have sep=True')
        item = self.add_item(text, pos=self.header_last, **params)
        self.header_last += 1
        return item

    def add_action_refresh(self, text='Refresh...', **params) -> MenuItem:
        return self.add_item(text, refresh='true', terminal='false', **params)

    def render(self) -> str:  # type: ignore
        if not self.header:
            raise ValueError('Menu must have a header')
        return ITEMS_SEP.join([item.render() for item in self.items])

    def dump(self) -> None:
        print(self.render())

    @property
    def header(self) -> list[MenuItem]:
        return self.items[: self.header_last]

    @property
    def body(self) -> list[MenuItem]:
        return self.items[self.header_last + 1:]
