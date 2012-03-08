#!/usr/bin/env bash

function get_seconds_since_epoch {
    perl -e "print time;"
}

#Setup some basic Variables
URI_PREFIX='file:'
SERVER_NAME=runtime
PID_FILE=pid
JAVA_OPTIONS=''
CLASSPATH=''
LD_LIBRARY_PATH=''

# Basic checks for dependencies
# /opt/local/sbin/cronolog

NOHUP_OUT_DIR="${NOHUP_OUT_DIR:-logs}"

case $(uname) in

    Darwin)
        echo "Detecting JAVA_HOME"
        if [ -n JAVA_HOME ]; then
            echo "Auto Setting JAVA_HOME"
            if [ -d '/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home' ] ; then
                export JAVA_HOME='/System/Library/Frameworks/JavaVM.framework/Versions/CurrentJDK/Home'
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

    ;;
        
    Redhat)
        echo
    
    ;;
    
    Ubuntu)
        echo
    
    ;;
    
esac  
    

