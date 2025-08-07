#!/bin/bash
set -e
# 윈도우는 /bin/sh

if [ "$1" = 'splunk' ]; then
  shift
  echo sudo -HEu ${SPLUNK_USER} ${SPLUNK_HOME}/bin/splunk "$@"
  sudo -HEu ${SPLUNK_USER} ${SPLUNK_HOME}/bin/splunk "$@"

elif [ "$1" = 'start-service' ]; then
  # If user changed SPLUNK_USER to root we want to change permission for SPLUNK_HOME
  if [[ "${SPLUNK_USER}:${SPLUNK_GROUP}" != "$(stat --format %U:%G ${SPLUNK_HOME})" ]]; then
    echo ########## chown -R ${SPLUNK_USER}:${SPLUNK_GROUP} ${SPLUNK_HOME}
    chown -R ${SPLUNK_USER}:${SPLUNK_GROUP} ${SPLUNK_HOME}
  fi

  # If version file exists already - this Splunk has been configured before
  __configured=false
  if [[ -f ${SPLUNK_HOME}/etc/splunk.version ]]; then
    __configured=true
  fi

  __license_ok=false
  # If these files are different override etc folder (possible that this is upgrade or first start cases)
  # Also override ownership of these files to splunk:splunk
  if ! $(cmp --silent /var/opt/splunk/etc/splunk.version ${SPLUNK_HOME}/etc/splunk.version); then
    cp -fR /var/opt/splunk/etc ${SPLUNK_HOME}
    chown -R ${SPLUNK_USER}:${SPLUNK_GROUP} ${SPLUNK_HOME}/etc
    #chown -R ${SPLUNK_USER}:${SPLUNK_GROUP} ${SPLUNK_HOME}/var
  else
    __license_ok=true
  fi

  if tty -s; then
    __license_ok=true
  fi
  if [[ "$SPLUNK_START_ARGS" == *"--accept-license"* ]]; then
    __license_ok=true
  fi

  echo __configured $__configured
  echo __license_ok $__license_ok

  if [[ $__license_ok == "false" ]]; then
    cat << EOF
Splunk Enterprise
==============
  Available Options:
      - Launch container in Interactive mode "-it" to review and accept
        end user license agreement
      - If you have reviewed and accepted the license, start container
        with the environment variable:
            SPLUNK_START_ARGS=--accept-license
  Usage:
    docker run -it splunk/splunk:7.3.0
    docker run --env SPLUNK_START_ARGS="--accept-license" splunk/splunk:7.3.0
EOF
    exit 1
  fi

  if [[ $__configured == "false" ]]; then
    echo $__configured == "false";
    # If we have not configured yet allow user to specify some commands which can be executed before we start Splunk for the first time
    if [[ -n ${SPLUNK_BEFORE_START_CMD} ]]; then
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk ${SPLUNK_BEFORE_START_CMD}"
      sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk ${SPLUNK_BEFORE_START_CMD}"
    fi
    for n in {1..30}; do
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk $(eval echo \$\{SPLUNK_BEFORE_START_CMD_${n}\})"
      if [[ -n $(eval echo \$\{SPLUNK_BEFORE_START_CMD_${n}\}) ]]; then
        sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk $(eval echo \$\{SPLUNK_BEFORE_START_CMD_${n}\})"
      else
        # We do not want to iterate all, if one in the sequence is not set
        break
      fi
    done
  fi

  echo sudo -HEu ${SPLUNK_USER} ${SPLUNK_HOME}/bin/splunk start ${SPLUNK_START_ARGS}
  echo trap "sudo -HEu ${SPLUNK_USER} ${SPLUNK_HOME}/bin/splunk stop" SIGINT SIGTERM EXIT

  sudo -HEu ${SPLUNK_USER} ${SPLUNK_HOME}/bin/splunk start ${SPLUNK_START_ARGS}
  trap "sudo -HEu ${SPLUNK_USER} ${SPLUNK_HOME}/bin/splunk stop" SIGINT SIGTERM EXIT

  # If this is first time we start this splunk instance
  if [[ $__configured == "false" ]]; then
    echo ########## __configured $__configured == "false";
    __restart_required=false

    # Setup deployment server
    if [[ ${SPLUNK_ENABLE_DEPLOY_SERVER} == "true" ]]; then
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk enable deploy-server -auth admin:changeme"
      sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk enable deploy-server -auth admin:changeme"
      __restart_required=true
    fi

    # Setup deployment client
    # http://docs.splunk.com/Documentation/Splunk/latest/Updating/Configuredeploymentclients
    if [[ -n ${SPLUNK_DEPLOYMENT_SERVER} ]]; then
      echo ########## SPLUNK_DEPLOYMENT_SERVER ${SPLUNK_DEPLOYMENT_SERVER};
      sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk set deploy-poll ${SPLUNK_DEPLOYMENT_SERVER} -auth admin:changeme"
      __restart_required=true
    fi

    if [[ "$__restart_required" == "true" ]]; then
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk restart"
      sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk restart"
    fi

    # Setup listening
    # http://docs.splunk.com/Documentation/Splunk/latest/Forwarding/Enableareceiver
    if [[ -n ${SPLUNK_ENABLE_LISTEN} ]]; then
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk enable listen ${SPLUNK_ENABLE_LISTEN} -auth admin:changeme ${SPLUNK_ENABLE_LISTEN_ARGS}"
      sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk enable listen ${SPLUNK_ENABLE_LISTEN} -auth admin:changeme ${SPLUNK_ENABLE_LISTEN_ARGS}"
    fi


    echo SPLUNK_FORWARD_SERVER : ${SPLUNK_FORWARD_SERVER}
    # Setup forwarding server
    # http://docs.splunk.com/Documentation/Splunk/latest/Forwarding/Deployanixdfmanually
    if [[ -n ${SPLUNK_FORWARD_SERVER} ]]; then
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add forward-server ${SPLUNK_FORWARD_SERVER} -auth admin:changeme ${SPLUNK_FORWARD_SERVER_ARGS}"
      sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add forward-server ${SPLUNK_FORWARD_SERVER} -auth admin:changeme ${SPLUNK_FORWARD_SERVER_ARGS}"
    fi

    for n in {1..10}; do
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add forward-server $(eval echo \$\{SPLUNK_FORWARD_SERVER_${n}\}) -auth admin:changeme $(eval echo \$\{SPLUNK_FORWARD_SERVER_${n}_ARGS\})"
      if [[ -n $(eval echo \$\{SPLUNK_FORWARD_SERVER_${n}\}) ]]; then
        sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add forward-server $(eval echo \$\{SPLUNK_FORWARD_SERVER_${n}\}) -auth admin:changeme $(eval echo \$\{SPLUNK_FORWARD_SERVER_${n}_ARGS\})"
      else
        # We do not want to iterate all, if one in the sequence is not set
        break
      fi
    done

    echo SPLUNK_ADD : ${SPLUNK_ADD}
    # Setup monitoring
    # http://docs.splunk.com/Documentation/Splunk/latest/Data/MonitorfilesanddirectoriesusingtheCLI
    # http://docs.splunk.com/Documentation/Splunk/latest/Data/Monitornetworkports
    if [[ -n ${SPLUNK_ADD} ]]; then
        echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add ${SPLUNK_ADD} -auth admin:changeme"
        sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add ${SPLUNK_ADD} -auth admin:changeme"
    fi
    for n in {1..30}; do
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add $(eval echo \$\{SPLUNK_ADD_${n}\}) -auth admin:changeme"
      if [[ -n $(eval echo \$\{SPLUNK_ADD_${n}\}) ]]; then
        sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk add $(eval echo \$\{SPLUNK_ADD_${n}\}) -auth admin:changeme"
      else
        # We do not want to iterate all, if one in the sequence is not set
        break
      fi
    done

    echo SPLUNK_CMD : ${SPLUNK_CMD}
    # Execute anything
    if [[ -n ${SPLUNK_CMD} ]]; then
        echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk ${SPLUNK_CMD}"
        sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk ${SPLUNK_CMD}"
    fi
    for n in {1..30}; do
      echo sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk $(eval echo \$\{SPLUNK_CMD_${n}\})"
      if [[ -n $(eval echo \$\{SPLUNK_CMD_${n}\}) ]]; then
        sudo -HEu ${SPLUNK_USER} sh -c "${SPLUNK_HOME}/bin/splunk $(eval echo \$\{SPLUNK_CMD_${n}\})"
      else
        # We do not want to iterate all, if one in the sequence is not set
        break
      fi
    done
  fi

  sudo -HEu ${SPLUNK_USER} tail -n 0 -f ${SPLUNK_HOME}/var/log/splunk/splunkd_stderr.log &
  echo sudo -HEu ${SPLUNK_USER} tail -n 0 -f ${SPLUNK_HOME}/var/log/splunk/splunkd_stderr.log &
  echo ############# SPLUNK MESSAGE END ###################
  wait
elif [ "$1" = 'splunk-bash' ]; then
  echo sudo -u ${SPLUNK_USER} /bin/bash --init-file ${SPLUNK_HOME}/bin/setSplunkEnv
  sudo -u ${SPLUNK_USER} /bin/bash --init-file ${SPLUNK_HOME}/bin/setSplunkEnv

else
  "$@"
fi
