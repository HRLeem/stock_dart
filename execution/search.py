# -*- coding: utf-8 -*-
import execution.defs.defs_search as defs_search

def start():
    make_list = defs_search.Request_list()
    search = defs_search.Search()

    make_list.get_corp_xml()
    make_list.xml_to_list()
    search.corp_list = make_list.corp_list_has_stockcode
    search.pick_corp()
