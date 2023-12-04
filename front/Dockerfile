FROM node:14.16.0

WORKDIR /app
COPY package*.json /app
RUN npm install -g @vue/cli
RUN npm install @vue/compiler-sfc
RUN npm install @vitejs/plugin-vue
RUN npm install

# Bundle app source
COPY . /app

EXPOSE 8080

CMD [ "npm", "run", "serve"]