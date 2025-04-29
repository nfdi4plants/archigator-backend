# archigator
Archigator offers users a simple way to publish ARCs from gitlab to an Invenio repository


# Getting started
Create the environment file below, and setup the software via docker compose file.


# Env-File

archigator.env file

```
# Archigator Settings

# Admin Api Access
ARCHIGATOR_USERNAME=archigator
ARCHIGATOR_PASSWORD=
ARCHIGATOR_URL=https://archigator.nfdi4plants.org
# Secret for Gitlab API access (for ie. Gitlab Badge creation)
ARCHIGATOR_SECRET=
ARCHIGATOR_PUBLICATION_SERVER=https://archive.nfdi4plants.org
ARCHIGATOR_PUBLISHER=DataPLANT

# Invenio Settings
INVENIO_API_TOKEN=
INVENIO_USERNAME=invenio@nfdi4plants.org
INVENIO_API_URL=https://archive.nfdi4plants.org
INVENIO_COMMUNITY_ID=

# Gitlab Settings
GITLAB_API_TOKEN=
GITLAB_API_URL=https://git.nfdi4plants.org
GITLAB_URL=https://git.nfdi4plants.org
GITLAB_SECRET=

# let archigator send an email, if a user 
EMAIL_ENABLED=True
EMAIL_SERVER=
EMAIL_USERNAME=
EMAIL_SENDER=
EMAIL_PORT=
EMAIL_PASSWORD=
# send to mail address (can be a list comma separated)
CURATOR_MAIL=

# Oauth Settings
OAUTH_REALM=dataplant
OAUTH_URL=https://auth.nfdi4plants.org/realms/dataplant
OAUTH_DOMAIN=auth.nfdi4plants.org
OAUTH_API_AUDIENCE=archigator
OAUTH_ISSUER=https://auth.nfdi4plants.org/realms/dataplant
OAUTH_ALGORITHM=RS256


```


# Docker compose file


```
version: "3.9"
services:
  archigator-frontend:
    image: ghcr.io/nfdi4plants/archigator-frontend:main
    ports:
      - 80:80
    container_name: archigator-frontend
    networks:
      - archigator-network

  archigator-backend:
    image: ghcr.io/nfdi4plants/archigator-backend:main
    ports:
      - 8000:8000
    container_name: archigator-backend
    env_file:
      - ./archigator.env
    networks:
      - archigator-network

networks:
  archigator-network:

```
