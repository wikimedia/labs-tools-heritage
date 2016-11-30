#!/bin/sh
yamllint $(find ./ -type d \( -path ./vendor -o -path ./node_modules \) -prune -o -name '*.yml' -print )
