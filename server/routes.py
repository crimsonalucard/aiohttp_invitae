from aiohttp import web
from typing import List
from server.views import search_for_gene, word_suggestion

routes: List[web.RouteDef] = [
    web.get('/gene_search/', search_for_gene),
    web.get('/word_suggestion/', word_suggestion)
]
