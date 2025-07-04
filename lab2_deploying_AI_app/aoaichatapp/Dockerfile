# Use the official Node.js image for building the app
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the application files
COPY . .

# Copy the .env file
COPY .env .env

# Build the application
RUN npm run build

# Use the official Nginx image for serving the app
FROM nginx:alpine AS production

# Copy the built files to the Nginx web server directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]