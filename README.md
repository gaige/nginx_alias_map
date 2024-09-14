nginx_alias_map: A Plugin for Pelican
====================================================

[![Build Status](https://img.shields.io/github/actions/workflow/status/gaige/nginx_alias_map/main.yml?branch=main)](https://github.com/gaige/nginx_alias_map/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-nginx-alias-map)](https://pypi.org/project/pelican-nginx-alias-map/)
![License](https://img.shields.io/pypi/l/pelican-nginx-alias-map?color=blue)


This Pelican plugin creates an nginx-compatible map between the final page locations
and prior locations, defined in the "Alias" attribute for any article or page.

Loosely based on [pelican-alias](https://github.com/Nitron/pelican-alias) by Chris Williams,
which itself was inspired by jekyll_alias_generator.

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-nginx-alias-map

Usage
-----

Add the directory to the base plugins directory to `PLUGIN_PATHS` in
`pelicanconf.py`, and then add `nginx_alias_map` to the `PLUGINS` list. For example,

    PLUGIN_PATHS = ["plugins"]
    PLUGINS = ['nginx_alias_map']

Definable parameters (with defaults in brackets) allow some configuration of the output
of the plugin.

There are two definable parameters, one from Chris's code (`ALIAS_DELIMITER`), which
defines the delimiter for multiple aliases for the same item; and `ALIAS_FILE`, which
defines the final name of the output file containing the map; and

    ALIAS_DELIMITER : Delimeter between multiple aliases for the same item [","]
    ALIAS_FILE : Name of map file to be placed in `output` ['alias_map.txt']
    ALIAS_MAP : Name of the map used in the alias file ['redirect_uri']
    ALIAS_MAP_TEMP: Name of the map used in the alias file when 2-stage lookup is needed ['redirect_uri_1']

### Support for URLs with query strings

In the event that you need to redirect a URI that contains a query string, a separate
map block will be created to map the `$request_uri` against an re.escaped version of your
alias that contains the `?` character. Otherwise, when no query string is present, the
test is made against `$uri`, which has much more processing done with it (query string
removal, removal of unnecessary '/'s, and so forth).

### NGINX configuration

The resulting file (stored in `output/$(ALIAS_FILE)`) is ready to be included into
your nginx configuration file (in an http stanza). Once the map is created, use the
`ALIAS_MAP` variable in your processing.

    include /opt/web/output/alias_map.txt;

    server {
      listen       *:80 ssl;
      server_name  example.server;


        # Redirection logic
        if ( $redirect_uri ) {
            return 301 $redirect_uri;
        }

        location / {
            alias /opt/web/output;
        }
    }

This configuration uses the evil `if` statement, but it's concise.  If you have a better
approach, please create a pull request, and I'll add it to this doc (or replace it if it
makes more sense).

I've chosen to use a 301 redirect here, because I'm confident of the permanency.  During
testing, you may want to use a 302.

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/gaige/nginx_alias_map/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

Updating
--------

We use dependabot for updating dependencies, conventional commits for commit messages,
and github actions for release.

To generate a release:

1. `cz bump --dry-run [--increment patch]` to verify changes
2. `cz bump [--increment patch]` to finalize
3. `git push` to send code and `git push <tag>` to send the tag (or the less-safe `--tags`)


License
-------

This project is licensed under the MIT license.
