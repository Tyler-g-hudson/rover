FROM mambaorg/micromamba

# The user and group.
ENV DEFAULT_GID 1000
ENV DEFAULT_UID 1000

# The location of the repository.
ENV ROVER_LOCATION /app
# The location that files are mounted to.
ENV MOUNT_LOCATION /tmp

# The following actions require root permissions:
USER root

# Install the dependencies for this project, held in environment.yml.
COPY ./environment.yml environment.yml
RUN micromamba install -y -n base -f environment.yml \
 && micromamba clean --all --yes \
 && rm environment.yml

RUN mkdir -p ${MOUNT_LOCATION} \
 && chmod -R 0755 ${MOUNT_LOCATION} \
 && mkdir -p ${ROVER_LOCATION} \
 && chmod -R 0755 ${ROVER_LOCATION}

# Give control to the default mamba user.
WORKDIR ${ROVER_LOCATION}
USER ${DEFAULT_USER}

# Copy the repository onto the image.
COPY ./rover ${ROVER_LOCATION}/rover
