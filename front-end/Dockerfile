FROM node:20-alpine as build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g serve
EXPOSE 80
CMD [ "serve" , "-s" , "dist" , "-p" , "80"]
# CMD [ "npm" , "run" , "preview" ]