#!/bin/bash

echo -e '\nInstallModule.sh Begin\n';

npm install -g npm@9.5.0;
npm install --force;

npm install redux@4.2.1
npm install react-redux@8.0.5
npm install react-router-dom@6.9.0
npm install react-spring@9.7.1
npm install redux-thunk@2.4.2

echo -e '\nInstallModule.sh Success\n';
