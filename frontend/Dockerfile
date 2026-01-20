FROM nginx:alpine

# Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# Копируем nginx.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Копируем билд фронта
COPY frontend/dist/ /usr/share/nginx/html/

EXPOSE 80
