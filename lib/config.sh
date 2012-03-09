#!/usr/bin/env bash

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
            echo "Auto Setting JAVA_HOME"
            if [ -d '/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home' ] ; then
                export JAVA_HOME='/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home'
                export JAVA_CLASSES='/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Classes'
            fi
        fi

        echo "Detecting JBOSS_HOME"
        if [ -n JBOSS_HOME ]; then
            echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
            if [ -d  '/opt/local/share/jboss-5.1.0.GA' ] ; then
                export JBOSS_HOME='/opt/local/share/jboss-5.1.0.GA'
            else
                echo "jboss-5.1.0.GA not found"
                echo "consider installing under /opt/local/share"
                exit 1
            fi
        fi

        if [ ! -f  '/opt/local/sbin/cronolog' ] ; then
            echo "Please install cronolog using macports"
            exit 1
        fi
        
        CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_CLASSES}/classes.jar"

    ;;
        
    Redhat)
        echo
        
        
        CLASSPATH="${JBOSS_HOME}/bin/run.jar:${JAVA_HOME}/lib/tools.jar"
    
    ;;
    
    Ubuntu)

        echo "Detecting JAVA_HOME"
        if [ -n JAVA_HOME ]; then
            echo "Auto Setting JAVA_HOME"
            if [ -d '/usr/lib/jvm/java-6-openjdk' ] ; then
                export JAVA_HOME='/usr/lib/jvm/java-6-openjdk'
            fi
        fi

        echo "Detecting JBOSS_HOME"
        if [ -n JBOSS_HOME ]; then
            echo "Auto Setting JBOSS_HOME for jboss-5.1.0.GA"
            if [ -d  '/opt/local/share/jboss-5.1.0.GA' ] ; then
                export JBOSS_HOME='/opt/local/share/jboss-5.1.0.GA'
            else
                echo "jboss-5.1.0.GA not found"
                echo "consider installing under /opt/local/share"
                exit 1
            fi
        fi

        if [ ! -f  '/usr/sbin/cronolog' ] ; then
            echo "Please install cronolog"
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
    

# Setup of standard variables and settings.

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
