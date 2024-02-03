# Use the official Nginx base image
FROM nginx:latest

# Copy custom nginx.conf to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80
EXPOSE 443
EXPOSE 8000

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
