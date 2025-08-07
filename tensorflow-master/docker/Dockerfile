FROM centos:7.3.1611
MAINTAINER jscho <anabasis01@gmail.com>

ENV SPLUNK_PRODUCT splunk
ENV SPLUNK_VERSION 7.3.1
ENV SPLUNK_BUILD bd63e13aa157
ENV SPLUNK_FILENAME splunk-${SPLUNK_VERSION}-${SPLUNK_BUILD}-Linux-x86_64.tgz
#wget -O splunk-7.3.0-657388c7a488-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=7.3.0&product=splunk&filename=splunk-7.3.0-657388c7a488-Linux-x86_64.tgz&wget=true'
#wget -O splunk-7.3.1-bd63e13aa157-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=7.3.1&product=splunk&filename=splunk-7.3.1-bd63e13aa157-Linux-x86_64.tgz&wget=true'

ENV SPLUNK_HOME /opt/splunk
ENV SPLUNK_GROUP root
ENV SPLUNK_USER root
ENV SPLUNK_BACKUP_DEFAULT_ETC /var/opt/splunk

RUN echo ${SPLUNK_VERSION} \
    && echo ${SPLUNK_BUILD} \
    && echo ${SPLUNK_FILENAME}

WORKDIR /opt

# add splunk:splunk user
#RUN groupadd -r ${SPLUNK_GROUP} \
#    && useradd -r -m -g ${SPLUNK_GROUP} ${SPLUNK_USER} \
#    && echo groupadd -r ${SPLUNK_GROUP} \
#    && echo useradd -r -m -g ${SPLUNK_GROUP} ${SPLUNK_USER}

RUN cd /opt
#RUN yum install -y wget sudo tar dos2unix
RUN yum install -y wget sudo tar net-tools dos2unix \
    && wget -O splunk-7.3.1-bd63e13aa157-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=7.3.1&product=splunk&filename=splunk-7.3.1-bd63e13aa157-Linux-x86_64.tgz&wget=true'

#COPY ${SPLUNK_FILENAME} /opt/${SPLUNK_FILENAME}
RUN chmod +x /opt/${SPLUNK_FILENAME}

RUN tar xvf ${SPLUNK_FILENAME} \
&& rm -rf ${SPLUNK_FILENAME} \
&& yes | cp -f /opt/splunk/etc/splunk-launch.conf.default /opt/splunk/etc/splunk-launch.conf \
&& echo -ne "\nOPTIMISTIC_ABOUT_FILE_LOCKING = 1" >> /opt/splunk/etc/splunk-launch.conf \
&& chmod u+x /etc/sudoers \
#&& echo -ne "\nsplunk  ALL=(ALL)       ALL" >> /etc/sudoers \
&& chmod u-x /etc/sudoers \
&& mkdir -p /var/opt/splunk \
&& cp -R ${SPLUNK_HOME}/etc ${SPLUNK_BACKUP_DEFAULT_ETC} \
&& rm -fR ${SPLUNK_HOME}/etc \
&& chown -R ${SPLUNK_USER}:${SPLUNK_GROUP} ${SPLUNK_BACKUP_DEFAULT_ETC} \
&& chown -R ${SPLUNK_USER}:${SPLUNK_GROUP} ${SPLUNK_HOME}

WORKDIR /opt/splunk

COPY entrypoint.sh /sbin/entrypoint.sh
RUN chmod +x /sbin/entrypoint.sh

# Copy new license
#COPY ./Splunk_Enterprise_Q3FY17.lic /var/opt/splunk/etc/licenses/download-trial/Splunk_Enterprise_Q3FY17.lic
#COPY Splunk.License /opt/splunk/etc/licenses/Splunk.License

# Ports Splunk Web, Splunk Daemon, KVStore, Splunk Indexing Port, Network Input, HTTP Event Collector
EXPOSE 8000/tcp 8089/tcp 8191/tcp 9997/tcp 1514 8088/tcp

# Configurations folder, var folder for everything (indexes, logs, kvstore)
#VOLUME [ "/opt/splunk/etc", "/opt/splunk/var" ]
#VOLUME /opt/splunk/etc

#ENTRYPOINT ["/sbin/entrypoint.sh"]
#CMD ["start-service"]

RUN dos2unix /sbin/entrypoint.sh start-service
