# nginx\_alias\_map

This Pelican plugin creates an nginx-compatible map between the final page locations
and prior locations, defined in the "Alias" attribute for any article or page.

Loosely based on [pelican-alias](https://github.com/Nitron/pelican-alias) by Chris Williams,
which itself was inspired by jekyll\_alias\_generator.

## Configuration

Add the directory to the base plugins directory to `PLUGIN_PATHS` in
`pelicanconf.py`, and then add `nginx_alias_map` to the `PLUGINS` list. For example,

    PLUGIN_PATHS = ["plugins"]
    PLUGINS = ['nginx_alias_map']

Definable parameters (with defaults in brackets) allow some configuration of the output
of the plugin.
There are two definable parameters, one from Chris's code (`ALIAS\_DELIMITER`), which
defines the delimiter for multiple aliases for the same item; and `ALIAS\_FILE`, which
defines the final name of the output file containing the map; and 

    ALIAS_DELIMITER : Delimeter between multiple aliases for the same item [","]
    ALIAS_FILE : Name of map file to be placed in `output` ['alias_map.txt']
    ALIAS_MAP : Name of the map used in the alias file ['redirect_uri']

### NGINX configuration

The resulting file (stored in `output/$(ALIAS\_FILE)`) is ready to be included into
your nginx configuration file.  Once the map is created, use the `ALIAS_MAP` variable
in your processing.

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
approach, please create a pull request and I'll add it to this doc (or replace it if it
makes more sense).

I've chosen to use a 301 redirect here, because I'm confident of the permanency.  During
testing, you may want to use a 302.
