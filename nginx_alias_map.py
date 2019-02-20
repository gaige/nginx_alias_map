# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path
import logging
from urllib.parse import urlparse

from pelican import signals

logger = logging.getLogger(__name__)


class NginxAliasMapGenerator(object):

    def __init__(self, context, settings, path, theme, output_path, *args):
        self.output_path = output_path
        self.context = context
        self.alias_delimiter = settings.get('ALIAS_DELIMITER', ',')
        self.alias_file = settings.get('ALIAS_FILE','alias_map.txt')
        self.alias_map = settings.get('ALIAS_MAP', 'redirect_uri')

    def create_alias(self, page, alias, fd):
        partial_url = page.url
        if not urlparse(partial_url).scheme:
            partial_url = "https://$server_name/"+partial_url
        alias_line = "\t~^%s$ %s;" % (alias, partial_url)       
        fd.write(alias_line+"\n")

    def generate_output(self, writer):
        path = os.path.join(self.output_path, self.alias_file)
        with open(path, 'w') as fd:
            fd.write("map $uri $%s {\n" % self.alias_map)

            pages = (
                self.context['pages'] + self.context['articles'] +
                self.context.get('hidden_pages', []))

            for page in pages:
                aliases = page.metadata.get('alias', [])
                if type(aliases) != list:
                    aliases = aliases.split(self.alias_delimiter)
                for alias in aliases:
                    alias = alias.strip()
                    logger.info('[alias] Processing alias %s' % alias)
                    self.create_alias(page, alias, fd)
            fd.write("  }\n")


def get_generators(generators):
    return NginxAliasMapGenerator


def register():
    signals.get_generators.connect(get_generators)
