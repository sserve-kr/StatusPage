FROM python:3.11.1

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade wheel

# use pipenv
RUN pip install pipenv

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Copy source code (./backend) to working directory
COPY ./backend ./
COPY ./docker-entrypoint.sh ./

# Expose port 5000
EXPOSE 5000

RUN chmod +x ./docker-entrypoint.sh

# Run the app
CMD ["./docker-entrypoint.sh"]
