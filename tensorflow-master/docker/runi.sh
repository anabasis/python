export SPLUNK_CONTAINER_NAME="splunk"

winpty \
docker \
  run \
  --interactive \
  --tty \
  --name ${SPLUNK_CONTAINER_NAME} \
  --hostname splunk.localdomain \
  --env "SPLUNK_USER=root" \
  --env "SPLUNK_START_ARGS=--accept-license  --seed-passwd welcome!1 " \
  --publish 18000:8000 \
  --publish 18089:8089 \
  splunk/splunk:latest;

  # docker \
  #   run \
  #   --interactive \
  #   --tty \
  #   --volume /Users/chojunseung/Workings/Containers/splunk/splunk730_app:/opt/splunk/etc/apps \
  #   --name ${SPLUNK_CONTAINER_NAME} \
  #   --hostname splunk.localdomain \
  #   --env "SPLUNK_USER=root" \
  #   --env "SPLUNK_START_ARGS=--accept-license  --seed-passwd welcome!1 " \
  #   --publish 18000:8000 \
  #   --publish 18089:8089 \
  #   splunk/splunk:latest;
