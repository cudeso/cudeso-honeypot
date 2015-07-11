By default dionaea logs to a sqlite file /var/lib/dionaea/logsql.sqlite.

The sqlite logstash module needs an ID-column to keep track of the data.

The patch logsql.py adds an ID field and keeps its updated with every dionaea connection.
