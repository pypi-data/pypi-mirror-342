from cubicweb.cwctl import CWCTL
from cubicweb.toolsutils import Command
from cubicweb.utils import admincnx

from cubicweb_spacyquery import spacyquery


class SpacyQueryPreparation(Command):
    """Prepare data for spacy query

    <instance>
      identifier of the instance into which the scheme will be imported.

    """

    arguments = "[options] <instance>"
    name = "spacy-query-preparation"
    min_args = 1

    def run(self, args):
        appid = args[0]

        with admincnx(appid) as cnx:
            spacyquery.prepare(cnx, appid)


CWCTL.register(SpacyQueryPreparation)
