# NRPE-Py

## Project description
NRPE Nagios plugin implemented in Python (with SSL support & authentication).

Works as a standalone web server with (or without) SSL support (see mod_gv.py.sample file) + token based authentication.

It is basically a backdoor, therefore be very careful with what you are allowing to be invoked (see mod_gv.py.sample file -> self.apps variable).


### High level design overview
![High level design overview](https://raw.githubusercontent.com/vbeskrovny/NRPE-Py/main/NRPE-Py-HL-Design.png "High level design overview")



## Installation process
* Clone the repo
* Rename .sample files
* Place files according to the description (see below)
* Generate auth_token(s): `ps | sha512sum` (trim to the desired length)
* Configure and remove all "SETUP" comments (see below)
* check_by_curl.sh and check_by_curl_insecure.sh should be in plugins directory of your Nagios installation (i.e. Nagios server)
* Enjoy :)
 
PS: you might need to install tornado libs - `pip3 install tornado`



## Files
* [app.py](https://github.com/vbeskrovny/NRPE-Py/blob/main/app.py) = main application (to be executed by nrpe-py.conf from supervisord)
* [check_by_curl_insecure.sh.sample](https://github.com/vbeskrovny/NRPE-Py/blob/main/check_by_curl_insecure.sh.sample) (nagios server plugin, to be placed in /usr/lib/nagios/plugins or whatever directory you define for the plugins)
* [check_by_curl.sh.sample](https://github.com/vbeskrovny/NRPE-Py/blob/main/check_by_curl.sh.sample) (nagios server plugin, to be placed in /usr/lib/nagios/plugins or whatever directory you define for the plugins)
* [mod_gv.py.sample](https://github.com/vbeskrovny/NRPE-Py/blob/main/mod_gv.py.sample) = application configuration (should be in the same directory as app.py)
* [nrpe-py.conf.sample](https://github.com/vbeskrovny/NRPE-Py/blob/main/nrpe-py.conf.sample) = supervisord service file (to be placed in /etc/supervisor/conf.d)


## Nagios host section:
```
define service {                                                                                                                                                               
    use                     generic-service
    host_name               YOUR_HOSTNAME
    service_description     NRPE-Py
    check_command           check_nrpe
}


define service {                                                                                                                                                               
    use                     generic-service
    host_name               YOUR_HOSTNAME
    service_description     HDD root
    check_command           check_by_curl!check_disk!w=10%&c=5%&p=/
}
```

## Nagios commands section:
```
define command {
    command_name        check_by_curl
    command_line        $USER1$/check_by_curl.sh "00000000000000000000000000000000" "https://$HOSTADDRESS$:NRPE_PY_PORT/exec?cmd=$ARG1$&$ARG2$" <--- SETUP !!! ---> check self.auth_tokens in mod_gv.py
}


define command {
    command_name        check_by_curl_insecure
    command_line        $USER1$/check_by_curl_insecure.sh "00000000000000000000000000000000" "https://$HOSTADDRESS$:NRPE_PY_PORT/exec?cmd=$ARG1$&$ARG2$" <--- SETUP !!! ---> check self.auth_tokens in mod_gv.py
}


define command {
    command_name        check_nrpe
    command_line        $USER1$/check_http -S -H $HOSTADDRESS$ -u /status -p NRPE_PY_PORT -s "+OK" <--- SETUP !!! ---> check self.http_port in mod_gv.py
}
```