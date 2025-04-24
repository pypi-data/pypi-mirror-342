import functools

from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.view import view_config

from cubicweb_spacyquery.spacyquery import get_query_extractor


def authenticated(func):
    @functools.wraps(func)
    def wrapped(request, *args):
        if request.authenticated_userid is None:
            raise HTTPUnauthorized()
        return func(request, *args)

    return wrapped


@view_config(route_name="spacyquery-paths", request_method="GET", renderer="json")
@authenticated
def spacy_query_path(request):
    params = request.params.dict_of_lists()
    qe = get_query_extractor(request.cw_cnx)
    target_entities = params.get("target_entities", [])
    target_attrs = params.get("target_attrs", [])
    return {
        "rql": qe.get_queries(target_entities, target_attrs),
        "status": "ok",
    }


def includeme(config):
    config.add_route("spacyquery-paths", "/spacy-query/paths")
    config.scan(__name__)
