# Use the official Bun image as the base
FROM oven/bun:1 as base
WORKDIR /usr/src/app

# Install dependencies into a temp directory for caching
FROM base AS install
RUN mkdir -p /temp/dev
COPY package.json bun.lockb /temp/dev/
RUN cd /temp/dev && bun install --frozen-lockfile

# Install with --production (exclude devDependencies)
RUN mkdir -p /temp/prod
COPY package.json bun.lockb /temp/prod/
RUN cd /temp/prod && bun install --frozen-lockfile --production

# Copy node_modules from temp directory
# Then copy all (non-ignored) project files into the image
FROM install AS prerelease
COPY --from=install /temp/dev/node_modules node_modules
COPY . .

# [Optional] tests & build
ENV NODE_ENV=production
RUN bun test
RUN bun run build

# Integrate Flask, Python, Nginx, and Redis requirements
RUN apt-get update && apt-get install -y nginx redis-server && apt-get clean
COPY ./backend /app/backend
RUN pip install flask gunicorn
RUN rm /etc/nginx/sites-enabled/default
COPY ./nginx.conf /etc/nginx/sites-available/app
RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

# Copy production dependencies and source code into final image
FROM base AS release
COPY --from=install /temp/prod/node_modules node_modules
COPY --from=prerelease /usr/src/app/index.ts .
COPY --from=prerelease /usr/src/app/package.json .

# Set the command to run the Flask app, Redis, and Nginx
CMD service nginx start && service redis-server start && cd backend && gunicorn app:app -b 0.0.0.0:8000

# Run the Bun.js app
USER bun
EXPOSE 3000/tcp
ENTRYPOINT [ "bun", "run", "index.ts" ]
