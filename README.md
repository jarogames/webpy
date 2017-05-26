# WEB Python interface


## web01

- change the port to what you want

- GET ... files and inline options 

-POST ... functionality for forms.


## web02_re

- everything is redirected

- only one directory goes to WD

- heavy argparse


### apache2 reverse-proxy

I think it was like:
`https://httpd.apache.org/docs/2.4/howto/reverse_proxy.html` or maybe also `https://www.digitalocean.com/community/tutorials/how-to-use-apache-as-a-reverse-proxy-with-mod_proxy-on-debian-8`


*with the restricted proxy, it is possible to send the traffic to
local port and redirect from there*

`a2enmod  proxy  proxy_balancer  proxy_http`

edit *conf*

restart `systemctl restaret apache2`

