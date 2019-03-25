# fluentd/Dockerfile
FROM fluent/fluentd:v1.3.2-debian
RUN gem install fluent-plugin-elasticsearch --no-rdoc --no-ri
RUN gem install fluent-plugin-multi-format-parser --no-rdoc --no-ri
RUN gem install fluent-plugin-rewrite-tag-filter --no-rdoc --no-ri
COPY fluent.conf /fluentd/etc/fluent.conf
