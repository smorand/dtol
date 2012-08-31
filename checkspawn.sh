#!/bin/bash

ls src/public/images/spawns/ | while read a; do echo "select '${a/.png/}' as n, sum(c) from (select count(*) as c from dt_objects where name = '${a/.png/}' union select count(*) as c from dt_characters where name = '${a/.png/}') a;" | mysql -udtol -pdtol -Ddtol -N; done | grep 0 | grep -v '^fond-' | sed 's/ *0$//'

