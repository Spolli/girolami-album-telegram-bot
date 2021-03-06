#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def load_json(src):
    with open(src, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def update_json(src, obj):
    with open(src, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

def append_obj(src, obj):
    with open(src, 'a', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)