# Utilise une image officielle Node.js comme image de base
FROM node:20-alpine

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY package.json package-lock.json* ./

# Installe les dépendances
RUN npm install

# Copie le reste de l'application
COPY . .

# Expose le port utilisé par Vite
EXPOSE 5173

# Commande pour démarrer l'application
CMD ["npm", "run", "dev"]
