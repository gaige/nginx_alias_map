import logging
import os.path
from re import escape
import sys
from urllib.parse import urlparse

from pelican import signals

logger = logging.getLogger(__name__)


class NginxAliasMapGenerator:
    def __init__(self, context, settings, path, theme, output_path, *args):
        self.output_path = output_path
        self.context = context
        self.alias_delimiter = settings.get("ALIAS_DELIMITER", ",")
        self.alias_file = settings.get("ALIAS_FILE", "alias_map.txt")
        self.alias_map = settings.get("ALIAS_MAP", "redirect_uri")
        self.alias_map_temp = settings.get("ALIAS_MAP_TEMP", self.alias_map + "_1")

    def create_alias(self, page, alias, fd):
        partial_url = page.url
        if not urlparse(partial_url).scheme:
            partial_url = "https://$server_name/" + partial_url
        if sys.version_info < (3, 7):
            quoted_alias = escape(alias).replace("\\/", "/")
        else:
            quoted_alias = escape(alias)
        alias_line = f"\t~^{quoted_alias}$ {partial_url};"
        fd.write(alias_line + "\n")

    def generate_output(self, writer):
        path = os.path.join(self.output_path, self.alias_file)

        pages = (
            self.context["pages"]
            + self.context["articles"]
            + self.context.get("hidden_pages", [])
        )

        query_aliases = []
        noquery_aliases = []
        for page in pages:
            aliases = page.metadata.get("alias", [])
            if not isinstance(aliases, list):
                aliases = aliases.split(self.alias_delimiter)
            for alias in aliases:
                alias = alias.strip()
                if "?" in alias:
                    query_aliases += [(page, alias)]
                    logger.info("[alias] Saving query alias %s" % alias)
                else:
                    noquery_aliases += [(page, alias)]
                    logger.info("[alias] Saving alias %s" % alias)

        with open(path, "w") as fd:
            default_variable = None
            if len(noquery_aliases) > 0:
                if len(query_aliases) > 0:
                    default_variable = self.alias_map_temp
                    fd.write("map $uri $%s {\n" % default_variable)
                else:
                    fd.write("map $uri $%s {\n" % self.alias_map)

                for page, alias in noquery_aliases:
                    logger.info("[alias] Processing quoted alias %s" % alias)
                    self.create_alias(page, alias, fd)
                fd.write("  }\n")

            if len(query_aliases) > 0:
                fd.write("\nmap $request_uri $%s {\n" % self.alias_map)
                if default_variable:
                    fd.write("\tdefault $%s;\n" % default_variable)
                for page, alias in query_aliases:
                    logger.info("[alias] Processing quoted alias %s" % alias)
                    self.create_alias(page, alias, fd)
                fd.write("  }\n")


def get_generators(generators):
    return NginxAliasMapGenerator


def register():
    signals.get_generators.connect(get_generators)
