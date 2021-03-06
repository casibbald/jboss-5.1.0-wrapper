#!/usr/bin/env bash
###############################################################################
#
# Author          : Charles Sibbald
# Email           : casibbald at gmail dot com
# Contributors    : 
# License         : BSD
# Copyright (c) 2012 Origami Planes Ltd.
# All rights reserved, excluding that of external software or modules
# from 3rd Parties.
# Redistribution and use in source and binary forms are permitted
# provided that the above copyright notice and this paragraph are
# duplicated in all such forms and that any documentation,
# advertising materials, and other materials related to such
# distribution and use acknowledge that the software was developed
# by the <organization>.  The name of the
# University may not be used to endorse or promote products derived
# from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
###############################################################################
#set -x

set -eu
set -o pipefail

chmod +x ./src/lib/config.sh
COMMAND=$1
if [ $1 == '' ]; then
    echo "Please pass one of the following options: start | stop | kill"
    exit 1
fi

function get_seconds_since_epoch {
    perl -e "print time;"
}

# Normalise scripts running location.
if uname -s | grep CYG > /dev/null 2>&1 ; then
   DOMAIN_DIR=`cygpath -m -a .`
   URI_PREFIX="file:/"
else
   cd "$(dirname "${0}")"
   export DOMAIN_DIR="$(pwd)"
   URI_PREFIX="file:"
fi

. ./src/lib/config.sh


case "${COMMAND}" in
    start)

        # Clean up previous temp directories.
        echo "========================================================================="
        echo "   Cleaning up JBoss temporary directories in preparation for JVM Launch"
        echo "   This may take a while"
        echo
        for dir in data log tmp; do
            echo "   Cleaning out ${SERVER_NAME}/${dir}"
            rm -rf ${SERVER_NAME}/${dir}
        done;
        
        echo "======================================================================="
        echo "  JBOSS_HOME           : $JBOSS_HOME"
        echo "  JAVA_HOME            : $JAVA_HOME"
        echo "  DOMAIN_DIR           : $DOMAIN_DIR"
        echo "  NOHUP_OUT_DIR        : ${DOMAIN_DIR}/$NOHUP_OUT_DIR"
        echo "  RUNTIME_DIR          : $SERVER_NAME"
        echo "======================================================================="
        echo

        #python lib/configure.py
        PID_STATUS=get_wrapper_run_status
        if [ "$PID_STATUS" != "1" ];then
            (
            #Do not quote JAVA_OPTIONS
            nohup ${JAVA_HOME}/bin/java ${JAVA_OPTIONS} \
                  -classpath "${CLASSPATH}" \
                   org.jboss.Main \
                  -Djboss.server.base.url="${URI_PREFIX}${DOMAIN_DIR}" \
                  -Djboss.server.base.dir="${DOMAIN_DIR}" \
                  -Djboss.server.name="${SERVER_NAME}" \
                  -Djboss.server.apps="${DOMAIN_DIR}/apps" \
                  -Djboss.server.log.dir="${DOMAIN_DIR}/logs" \
                  -b "${INTERFACE}" \
                  -c "${SERVER_NAME}" &
            echo $! > $PIDFILE
            ) | "${CRONOLOG}" >/dev/null 2>&1 "${DOMAIN_DIR}/${NOHUP_OUT_DIR}/nohup.out_%Y%m%d_%H" --link="${DOMAIN_DIR}/${NOHUP_OUT_DIR}/nohup.out" &
        else
            echo "Jboss Container already running"
            exit 1
        fi
    ;;

    status)
        if [ get_wrapper_run_status == "0" ]; then
            echo "JBoss Container running"
            exit 0
        else
            echo "JBoss Container not running"
            exit 1
        fi
        
    ;;
    
    
    stop)
        JBOSS_BOOT_CLASSPATH="${JBOSS_HOME}/bin/shutdown.jar:${JBOSS_HOME}/client/jbossall-client.jar"
        CLASSPATH="${CLASSPATH}:${JBOSS_BOOT_CLASSPATH}"
        #Do not quote JAVA_OPTIONS
        ${JAVA_HOME}/bin/java ${JAVA_OPTIONS} -classpath "${CLASSPATH}" org.jboss.Shutdown "$@"

    ;;
 
    kill)
        PID_STATUS=get_wrapper_run_status
        PID=`cat ${PIDFILE}`
        if [ "$PID_STATUS" = "1" ] ; then
            echo " Killing JBoss at PID ${PID} ..."
            kill -9 ${PID}
            rm -f ${PIDFILE}
            exit 0
        else
            echo "PID file indicates PID ${PID}, is not running."
            exit 0
        fi


esac


