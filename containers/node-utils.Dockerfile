FROM node:22-alpine3.19

RUN apk add git

RUN git config --global user.email "version-bump@automation"
RUN git config --global user.name "version-bump-automation"
RUN git config --global --add safe.directory /project

RUN npm i -g \
  commit-and-tag-version@12.4.1 \
  tftest-to-junitxml@0.2.0
