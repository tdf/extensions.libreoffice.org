/* This is the default varnish cache server configuration.
   Note that it is Ansible generated.
*/

vcl 4.0;
import directors;
import std;
#import cookie;
#import header;

/* Configure zope clients as backends */

backend client127_0_0_1_8081 {
    .host = "127.0.0.1";
    .port = "8081";
    .connect_timeout = 0.4s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout = 60s;
    .probe = {
        .url = "/";
        .timeout = 1s;
        .interval = 5s;
        .window = 5;
        .threshold = 2;
        .initial = 1;
    }
}
backend client127_0_0_1_8082 {
    .host = "127.0.0.1";
    .port = "8082";
    .connect_timeout = 0.4s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout = 60s;
    .probe = {
        .url = "/";
        .timeout = 1s;
        .interval = 5s;
        .window = 5;
        .threshold = 2;
        .initial = 1;
    }
}
backend client127_0_0_1_8083 {
    .host = "127.0.0.1";
    .port = "8083";
    .connect_timeout = 0.4s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout = 60s;
    .probe = {
        .url = "/";
        .timeout = 1s;
        .interval = 5s;
        .window = 5;
        .threshold = 2;
        .initial = 1;
    }
}
backend client127_0_0_1_8084 {
    .host = "127.0.0.1";
    .port = "8084";
    .connect_timeout = 0.4s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout = 60s;
    .probe = {
        .url = "/";
        .timeout = 1s;
        .interval = 5s;
        .window = 5;
        .threshold = 2;
        .initial = 1;
    }
}

/* Only allow PURGE from localhost */
acl purge_allowed {
    "localhost";
    "127.0.0.1";
    /* Just in case the purge host is not in the same machine */
    /* Do not forget to add its IP */
}

sub vcl_init {
  # Use hash() director with sticky sessions
  new cluster = directors.hash();

  cluster.add_backend(client127_0_0_1_8081, 1);
  cluster.add_backend(client127_0_0_1_8082, 1);
  cluster.add_backend(client127_0_0_1_8083, 1);
  cluster.add_backend(client127_0_0_1_8084, 1);
}

sub vcl_recv {
#  cookie.parse(req.http.cookie);
#  if (cookie.get("sticky")) {
#    set req.http.sticky = cookie.get("sticky");
#    } else {
#    # The cookies will have floats in them.
#    set req.http.sticky = std.random(1, 100);
#  }

  # Use hash() director with sticky sessions
  # set req.backend_hint = cluster.backend(req.http.sticky);
  set req.backend_hint = cluster.backend(req.url);

  # Sanitize compression handling
  if (req.http.Accept-Encoding) {
      if (req.url ~ "\.(jpg|png|gif|gz|tgz|bz2|tbz|mp3|ogg)$") {
          # No point in compressing these
          unset req.http.Accept-Encoding;
      } elsif (req.http.Accept-Encoding ~ "gzip") {
          set req.http.Accept-Encoding = "gzip";
      } elsif (req.http.Accept-Encoding ~ "deflate" && req.http.user-agent !~ "MSIE") {
          set req.http.Accept-Encoding = "deflate";
      } else {
          # unknown algorithm
          unset req.http.Accept-Encoding;
      }
  }

  # Handle special requests
  if (req.method != "GET" && req.method != "HEAD") {
     # POST, Logins and edits
     if (req.method == "POST" || req.method == "PATCH" || req.method == "DELETE") {
         return(pass);
     }
     /* Purge allowed only from some hosts */
     if (req.method == "PURGE") {
         if (client.ip ~ purge_allowed) {
            return(purge);
         } else {
            return(synth(403, "Purge not allowed from this host. Access denied."));
         }
     }
  }

  /* Do not cache AJAX requests */
  if (req.http.X-Requested-With == "XMLHttpRequest") {
      return(pass);
  }

  # Sanitize cookies so they do not needlessly destroy cacheability for anonymous pages
  if (req.http.Cookie) {
      set req.http.Cookie = ";" + req.http.Cookie;
      set req.http.Cookie = regsuball(req.http.Cookie, "; +", ";");
      set req.http.Cookie = regsuball(req.http.Cookie, ";(sticky|I18N_LANGUAGE|statusmessages|__ac|_ZopeId|__cp|beaker\.session|authomatic|serverid)=", "; \1=");
      set req.http.Cookie = regsuball(req.http.Cookie, ";[^ ][^;]*", "");
      set req.http.Cookie = regsuball(req.http.Cookie, "^[; ]+|[; ]+$", "");

      if (req.http.Cookie == "") {
          unset req.http.Cookie;
      }
  }

  # Annotate request with X-Anonymous header if anonymous
  if (!(req.http.Cookie && req.http.Cookie ~ "__ac(|_(name|password|persistent))=")) {
      set req.http.X-Anonymous = "True";
  }

  # Keep auth/anon variants apart if "Vary: X-Anonymous" is in the response
  if (!(req.http.Authorization || req.http.Cookie ~ "(^|.*; )__ac=")) {
      set req.http.X-Anonymous = "True";
  }

  return(hash);

}

sub vcl_pipe {
    /* This is not necessary if you do not do any request rewriting. */
    set req.http.connection = "close";
}

sub vcl_hit {
    if (!obj.ttl > 0s) {
        return(pass);
    }
}

sub vcl_miss {
    if (req.method == "PURGE") {
        return (synth(404, "Not in cache miss"));
    }

}

sub vcl_backend_response {

    # Don't allow static files to set cookies.
    # (?i) denotes case insensitive in PCRE (perl compatible regular expressions).
    # make sure you edit both and keep them equal.
    if (bereq.url ~ "(?i)\.(pdf|asc|dat|txt|doc|xls|ppt|tgz|png|gif|jpeg|jpg|ico|swf|css|js)(\?.*)?$") {
      unset beresp.http.set-cookie;
    }

    /* commented */
       /*if (!obj.ttl > 0s) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - not cacheable)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return(deliver);
       }*/

    if (beresp.http.Set-Cookie) {
        set beresp.http.X-Varnish-Action = "FETCH (pass - response sets cookie)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return(deliver);
    }
    if (beresp.http.Cache-Control ~ "(private|no-cache|no-store)") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - cache control disallows)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return(deliver);
    }
    if (beresp.http.Authorization && !beresp.http.Cache-Control ~ "public") {
        set beresp.http.X-Varnish-Action = "FETCH (pass - authorized and no public cache control)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return(deliver);
    }

    if (beresp.http.X-Anonymous && !beresp.http.Cache-Control) {
        set beresp.http.X-Varnish-Action = "FETCH (override - backend not setting cache control)";
        set beresp.ttl = 600s;
        return (deliver);
    }

    if (!beresp.http.Cache-Control) {
        set beresp.http.X-Varnish-Action = "FETCH (override - backend not setting cache control)";
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return (deliver);
    }

    set beresp.http.X-Varnish-Action = "FETCH (insert)";

    set beresp.grace = 120s;

    return (deliver);
}

sub vcl_hash {
    hash_data(req.url);
    hash_data(req.http.host);

    if (req.http.Accept-Encoding ~ "gzip") {
        hash_data("gzip");
    }
    else if (req.http.Accept-Encoding ~ "deflate") {
        hash_data("deflate");
    }

      /* With PAM this is no longer needed
      if (req.http.cookie ~ "I18N_LANGUAGE") {
          hash_data(regsub( req.http.Cookie, "^.*?I18N_LANGUAGE=([^;]*?);*.*$", "\1" ) );
      }
      */

}

sub vcl_deliver {
#  if (req.http.sticky) {
#    header.append(resp.http.Set-Cookie, "sticky=" + req.http.sticky + ";   Expires=" + cookie.format_rfc1123(now, 60m));
#  }

  # Mark the HIT or the MISS in a custom header
  if (obj.hits > 0) {
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }
}

sub vcl_synth {
    set resp.http.Content-Type = "text/html; charset=utf-8";
    synthetic(std.fileread("${buildout:directory}/etc/varnish/maintenance.html"));

    return (deliver);
}

sub vcl_backend_error {
    set beresp.http.Content-Type = "text/html; charset=utf-8";
    synthetic(std.fileread("${buildout:directory}/etc/varnish/maintenance.html"));

    return (deliver);
}
 
