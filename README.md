# NRPE-Py

# Nagios host section:
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

# Nagios commands section:
```
define command {
    command_name        check_by_curl
    command_line        $USER1$/check_by_curl.sh "00000000000000000000000000000000" "https://$HOSTADDRESS$:NRPE_PY_PORT/exec?cmd=$ARG1$&$ARG2$"
}


define command {
    command_name        check_by_curl_insecure
    command_line        $USER1$/check_by_curl_insecure.sh "00000000000000000000000000000000" "https://$HOSTADDRESS$:NRPE_PY_PORT/exec?cmd=$ARG1$&$ARG2$"
}


define command {
    command_name        check_nrpe
    command_line        $USER1$/check_http -S -H $HOSTADDRESS$ -u /status -p NRPE_PY_PORT -s "+OK"
}
```