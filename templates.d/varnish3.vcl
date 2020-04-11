# This is a basic VCL configuration file for varnish.  See the vcl(7)
# man page for details on VCL syntax and semantics.
# 
# Default backend definition.  Set this to point to your content
# server.
# 
vcl 4.0;

backend default {
  .host = "127.0.0.1";
  .port = "8080";
}

sub vcl_recv {

 # Remove any Google Analytics based cookies
  set req.http.Cookie = regsuball(req.http.Cookie, "__utm.=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "_ga=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "_gat=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "utmctr=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "utmcmd.=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "utmccn.=[^;]+(; )?", "");

  # Remove Optimizely Cookies
  set req.http.Cookie = regsuball(req.http.Cookie, "optim.=[^;]+(; )?", "");
  # Remove Gauges Cookies
  set req.http.Cookie = regsuball(req.http.Cookie, "_gau.=[^;]+(; )?", "");

  # Remove a ";" prefix in the cookie if present
  set req.http.Cookie = regsuball(req.http.Cookie, "^;\s*", "");

  # Are there cookies left with only spaces or that are empty?
  if (req.http.cookie ~ "^\s*$") {
    unset req.http.cookie;
  }

   if (req.restarts == 0) {
    if (req.http.x-forwarded-for) {
      set req.http.X-Forwarded-For =
        req.http.X-Forwarded-For + ", " + client.ip;
      } else {
        set req.http.X-Forwarded-For = client.ip;
      }
  }

  if (req.method != "GET" &&
      req.method != "HEAD" &&
      req.method != "PUT" &&
      req.method != "POST" &&
      req.method != "TRACE" &&
      req.method != "OPTIONS" &&
      req.method != "DELETE") {
        /* Non-RFC2616 or CONNECT which is weird. */
        return (pipe);
   }
   if (req.method != "GET" && req.method != "HEAD") {
        /* We only deal with GET and HEAD by default */
      return (pass);
  }

  if ( (req.http.host ~ "^(?i)smashing_ssl_one.tutorials.eoms") && req.http.X-Forwarded-Proto !~ "(?i)https") {
	set req.http.x-redir = "https://" + req.http.host + req.url;
	return (synth(750, ""));
  }
 return (hash);
}

# handles redirecting from http to https
sub vcl_synth {
  if (resp.status == 750) {
    set resp.status = 301;
    set resp.http.Location = req.http.x-redir;
    return(deliver);
  }
}

sub vcl_backend_response {
  set beresp.ttl = 10s;
  set beresp.grace = 1h;
}

sub vcl_deliver {
  if (obj.hits > 0) { # Add debug header to see if it's a HIT/MISS and the number of hits, disable when not needed
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }
} 
