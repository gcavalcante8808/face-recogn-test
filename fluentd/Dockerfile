# fluentd/Dockerfile
FROM fluent/fluentd:v0.14-debian
RUN gem install fluent-plugin-elasticsearch --no-rdoc --no-ri
RUN gem install fluent-plugin-multi-format-parser
COPY fluent.conf /fluentd/etc/fluent.conf
