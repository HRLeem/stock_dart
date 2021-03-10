# -*- coding: utf-8 -*-
import execution.defs.defs_search as defs_search

def start(year):
    search = defs_search.Search()
    search.pick_corp(year)
