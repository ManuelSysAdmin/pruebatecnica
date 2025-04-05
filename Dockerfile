# Usamos nginx:alpine como imagen base
FROM nginx:alpine

# Copiamos el nuevo index a su ruta
COPY index.html /usr/share/nginx/html

# exponemos el puerto http 
EXPOSE 80

# arrancamos nginx
CMD ["nginx", "-g", "daemon off;"]
