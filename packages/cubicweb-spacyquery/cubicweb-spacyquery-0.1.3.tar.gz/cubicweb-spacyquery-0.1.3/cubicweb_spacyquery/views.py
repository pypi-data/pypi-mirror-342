# -*- coding: utf-8 -*-
# copyright 2025 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""cubicweb-spacyquery views/forms/actions/components for web ui"""
import urllib.parse

from cubicweb_web.views.startup import StartupView
from cubicweb.predicates import authenticated_user

from cubicweb_web import httpcache
from cubicweb_web.views.urlrewrite import SimpleReqRewriter

from cubicweb_spacyquery.spacyquery import (
    get_entity_extractor,
    get_query_extractor,
    ask,
)

from spacy import displacy


class SpacyQueryRewriter(SimpleReqRewriter):
    priority = 100

    rules = [
        ("/spacyquery", dict(vid="spacyquery_startup")),
        ("/query", dict(vid="query_startup")),
    ]


SPACY_QUERY_TEMPLATE = """
<h1 style="text-align: center; margin-bottom: 20px;">Pose-moi une question</h1>
<hr style="width: 60%; margin: 0 auto; border: 1px solid #ccc;">
<div class="container" style="height: 100vh; position: relative;">
    <div class="row" style="height: 100%;">
        <div class="col-xs-12 col-md-6 col-md-offset-3" style="position: absolute; top: 20.33%; left: 25%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; width: 100%;">
            <form id="search-form" class="input-group" style="width: 100%; display: flex; flex-direction: row; align-items: center;">
                <input type="search" id="search-input" name="q"
                    class="form-control" placeholder="Rechercher..." value="{q}" required style="width: 80%; margin-right: 10px;">
                <button type="submit" class="btn btn-primary">Rechercher</button>
            </form>
            <!-- Zone pour afficher les résultats -->
            <div id="search-results" style="width: 80%; margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 4px; min-height: 50px;">
                <!-- Les résultats de la recherche s'afficheront ici -->
                {output}
            </div>
        </div>
    </div>
</div>
"""  # noqa: E501


def get_question(url):
    if "?q=" in url:
        question = url.split("?q=")[1]
        question = question.replace("+", " ")
        return urllib.parse.unquote(question)


RQL_BUTTON = """
  <a href="http://localhost:8080/view?rql={}" class="btn btn-primary" role="button">
    Tester la requête
  </a>
"""


def create_colors_options(docs):
    colors = {"VALUE": "#7aecec"}
    for ent in docs.ents:
        if ":" not in ent.label_:
            if ent.label_ in colors:
                pass
            elif ent.label_[0].isupper():
                colors[ent.label_] = "#aa9cfc"
            else:
                colors[ent.label_] = "#bfe1d9"
        else:
            colors[ent.label_] = "#e4e7d2"
    return colors


class SpacyQueryView(StartupView):
    __select__ = StartupView.__select__ & authenticated_user()
    __regid__ = "spacyquery_startup"
    http_cache_manager = httpcache.NoHTTPCacheManager

    def call(self):
        cnx = self._cw.cnx
        ee = get_entity_extractor(cnx)
        url = self._cw.url()
        question = get_question(url)
        spacy_ent_html, spacy_dep_html = "", ""
        if question:
            docs = ee.get_nlp_analyze(question)
            colors = create_colors_options(docs)
            spacy_ent_html = displacy.render(
                docs, style="ent", options={"colors": colors}
            )
            spacy_dep_html = displacy.render(
                docs, style="dep", options={"compact": True, "distance": 50}
            )
            rql = "<ul>\n"
            try:
                for query in ask(cnx, question):
                    rql += (
                        f"<li>{query.to_rql()} "
                        f"{RQL_BUTTON.format(query.to_rql().replace(' ', '+'))}</li>\n"
                    )
            except Exception:
                import traceback

                traceback.print_exc()
                rql += "<li>Aucune requête trouvée</li>"
            rql += "</ul>"
            output = """
            <h2> Recherche dans la question des mots clés du modèle et des données : </h2>
            {}
            <h2> Recherche dans la question des liens entre les termes : </h2>
            {}
            <h2> Proposition de requête RQL :</h2>
            {}
            """.format(
                spacy_ent_html, spacy_dep_html, rql
            )
            self.w(SPACY_QUERY_TEMPLATE.format(output=output, q=question))
        else:
            self.w(
                SPACY_QUERY_TEMPLATE.format(
                    output="Aucun résultat pour le moment", q=question
                )
            )


class QueryView(StartupView):
    __regid__ = "query_startup"
    http_cache_manager = httpcache.NoHTTPCacheManager

    def call(self):
        cnx = self._cw.cnx
        url = self._cw.url()
        question = get_question(url)
        query_extractor = get_query_extractor(cnx)
        if question:
            target_entities = [i for i in question.split() if "#" not in i]
            target_attributes = [i for i in question.split() if "#" in i]
            rql = "<ul>\n"
            try:
                for query in query_extractor.get_queries(
                    target_entities, target_attributes
                ):
                    rql += (
                        f"<li>{query.to_rql()} "
                        f"{RQL_BUTTON.format(query.to_rql().replace(' ', '+'))}</li>\n"
                    )
            except Exception:
                import traceback

                traceback.print_exc()
                rql += "<li>Aucune requête trouvée</li>"
            rql += "</ul>"
            output = """
            <h2> Proposition de requête RQL :</h2>
            {}
            """.format(
                rql
            )
            self.w(SPACY_QUERY_TEMPLATE.format(output=output, q=question))
        else:
            self.w(
                SPACY_QUERY_TEMPLATE.format(
                    output="Aucun résultat pour le moment", q=question
                )
            )


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__)
