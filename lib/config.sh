#!/usr/bin/env bash
###############################################################################
#
# Author          : Charles Sibbald
# Email           : casibbald at gmail dot com
# Contributors    : Attila Faludi, Peter Moore
# License         : BSD
# Copyright (c) 2012 Origami Planes Ltd.
# All rights reserved, exluding that of external software or modules from 3rd
# Parties.
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

function get_seconds_since_epoch {
    perl -e "print time;"
}

#Setup some basic Variables
URI_PREFIX='file:'
if [ ! -n JBOSS_VERSION ]; then
    export SERVER_NAME='runtime/5.1.0'
elif [ JBOSS_VERSION=='5.1.0' ]; then
    export SERVER_NAME='runtime/5.1.0'
elif [ JBOSS_VERSION=='7.1.0' ]; then
    export SERVER_NAME='runtime/7.1.0'
fi

case $(uname) in

    Darwin)
        echo "Detecting JAVA_HOME"
        if [ -n JAVA_HOME ]; then
            if [ -d '/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home' ] ; then
                echo "Auto Setting JAVA_HOME"
                export JAVA_HOME='/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home'
                export JAVA_CLASSES='/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Classes'
            fi
        fi

        echo "Detecting JBOSS_HOME"
        if [ -n JBOSS_HOME ]; then
            if [ -d  '/opt/local/share/jboss-5.1.0.GA' ] ; then
                echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
                export JBOSS_HOME='/opt/local/share/jboss-5.1.0.GA'
            else
                echo "jboss-5.1.0.GA not found"
                echo "consider installing under /opt/local/share"
                exit 1
            fi
        fi

        if [ -f  '/opt/local/sbin/cronolog' ] ; then
            export CRONOLOG="/opt/local/sbin/cronolog"
        else
            echo "Please install cronolog using macports"
            exit 1
        fi
        
        CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_CLASSES}/classes.jar"

    ;;
        
    Linux)
        if [ -f "/usr/bin/lsb_release" ]; then
            REDHAT_VERSION=`lsb_release -ir`
            echo "Detected Red Hat Linux"
            echo "${REDHAT_VERSION}" 
            echo "Detecting JAVA_HOME"
            if [ -n JAVA_HOME ]; then
                echo "Auto Setting JAVA_HOME"
                if [ -d '/usr/java/latest/' ] ; then
                    export JAVA_HOME='/usr/java/latest'
                fi
            fi
    
            echo "Detecting JBOSS_HOME"
            if [ -n JBOSS_HOME ]; then
                if [ -d  '/usr/jboss/jboss-5.1.0.GA' ] ; then
                    echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
                    export JBOSS_HOME='/usr/jboss/jboss-5.1.0.GA'
                elif [ -d  '/opt/jboss/jboss-5.1.0.GA' ] ; then
                    echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
                    export JBOSS_HOME='/opt/jboss/jboss-5.1.0.GA'
                else
                    echo
                    echo "jboss-5.1.0.GA not found"
                    echo "Consider installing under /usr/jboss/jboss-5.1.0.GA"
                    echo "Many environments choose to install under /opt/jboss<version>,"
                    echo "and while this is the default location when using the JBoss"
                    echo "Installer, we have a preference for /usr/jboss/jboss-<version>"
                    echo "for the simple reason that the wrapper Abstracts away the need"
                    echo "to deploy files directly into the JBoss install, but in a safe"
                    echo "and customisable location, that allows the user of the wrapper"
                    echo "to make modifications without being concerned about potentially"
                    echo "corrupting or contaminating the original Jboss installation."
                    echo 
                    exit 1
                fi
            fi
    
            if [ -f '/usr/sbin/cronolog' ] ; then
                export CRONOLOG="/usr/sbin/cronolog"
            else
                echo "Please install cronolog, if this is not available in your RPM Repo"
                echo "an RPM can be found at the following URL: http://pkgs.repoforge.org/cronolog"
                exit 1
            fi
            
            CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_HOME}/lib/tools.jar"
        fi
    
    ;;
    
    Ubuntu)

        echo "Detecting JAVA_HOME"
        if [ -n JAVA_HOME ]; then
            if [ -d '/usr/lib/jvm/java-6-sun' ] ; then
                echo "Auto Setting JAVA_HOME"
                export JAVA_HOME='/usr/lib/jvm/java-6-sun'
            elif [ -d '/usr/lib/jvm/java-6-openjdk' ] ; then
                echo "Auto Setting JAVA_HOME"
                export JAVA_HOME='/usr/lib/jvm/java-6-openjdk'
            else [ -d '/usr/lib/jvm/default-java' ]
                echo "Auto Setting JAVA_HOME"
                export JAVA_HOME='/usr/lib/jvm/default-java'
            fi
        fi

        echo "Detecting JBOSS_HOME"
        if [ -n JBOSS_HOME ]; then
            if [ -d  '/usr/jboss/jboss-5.1.0.GA' ] ; then
                echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
                export JBOSS_HOME='/usr/jboss/jboss-5.1.0.GA'
            elif [ -d  '/opt/jboss/jboss-5.1.0.GA' ] ; then
                echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
                export JBOSS_HOME='/opt/jboss/jboss-5.1.0.GA'
            else
                echo
                echo "jboss-5.1.0.GA not found"
                echo "Consider installing under /usr/jboss/jboss-5.1.0.GA"
                echo "Many environments choose to install under /opt/jboss<version>,"
                echo "and while this is the default location when using the JBoss"
                echo "Installer, we have a preference for /usr/jboss/jboss-<version>"
                echo "for the simple reason that the wrapper Abstracts away the need"
                echo "to deploy files directly into the JBoss install, but in a safe"
                echo "and customisable location, that allows the user of the wrapper"
                echo "to make modifications without being concerned about potentially"
                echo "corrupting or contaminating the original Jboss installation."
                echo 
                exit 1
            fi
        fi

        if [ -f  '/usr/bin/cronolog' ] ; then
            export CRONOLOG="/usr/bin/cronolog"
        else
            echo "Please install cronolog using apt-get/aptitude"
            exit 1
        fi
        
        export CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_HOME}/lib/tools.jar"
        
    ;;

    Solaris)
        echo
    
        export CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_HOME}/lib/tools.jar"
    ;;
    
    bsd)
        echo
        
        export CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_HOME}/lib/tools.jar"
    ;;

esac  

#PREPEND_CLASSPATH=
#ListenAddress={T}appserver.listen.ip{/T}
#ListenPort={T}appserver.port{/T}
#JndiPort={T}jboss.jndi.port{/T}

# region and language to be set for default Java locale
#LOCALE_REGION={T}locale.region{/T}
#LOCALE_LANGUAGE={T}locale.lang{/T}

if [ -f ${DOMAIN_DIR}/environment/token/env.properties ]; then
    export ADDITIONAL_PROPERTIES="-P${DOMAIN_DIR}/environment/token/env.properties"
else
    export ADDITIONAL_PROPERTIES="-P${DOMAIN_DIR}/environment/default/default.env.properties"
fi

# Setup of standard variables and settings.

# This section sould really check for the existence of env.properties and that these are set, if not use defaults.
if [ -n JAVA_OPTS='' ]; then
    export JAVA_OPTIONS='-Xms128m -Xmx512m -XX:MaxPermSize=256m -Dorg.jboss.resolver.warning=true -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000 -Djava.endorsed.dirs=${JBOSS_HOME}/lib/endorsed'
else
    export JAVA_EXTENDED_OPTS='-Dorg.jboss.resolver.warning=true -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000 -Djava.endorsed.dirs=${JBOSS_HOME}/lib/endorsed'
    export JAVA_OPTIONS="${JAVA_OPTS} ${JAVA_EXTENDED_OPTS}" 
fi

if [ -n LD_LIBRARY_PATH='' ]; then
    export LD_LIBRARY_PATH=''
else
    export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}"
fi

if [ -n INTERFACE='' ]; then
    export INTERFACE='0.0.0.0'
else
    export INTERFACE="${INTERFACE}"
fi

export PIDFILE=pid
export NOHUP_OUT_DIR="${NOHUP_OUT_DIR:-logs}"


function get_wrapper_run_status {
    if [ -f "${PIDFILE}" ] ; then
        PID=`cat ${PIDFILE}`
        if [ -n "${PID}" ] ; then
            PID_STATUS=`ps -p "${PID}" |grep -v "PID"`
            if [ "${PID_STATUS}" = "" ] ; then
                PID_STATUS="0"
            else
                PID_STATUS="1"
            fi
            return "${PID_STATUS}"
        else
            echo "No PID found in ${PIDFILE}"
            return 3
        fi
    else
        echo "No pid file available."
        return 4
    fi
}

