FROM mambaorg/micromamba

# The user and group.
ENV DEFAULT_GID 1000
ENV DEFAULT_UID 1000

# The location of the repository.
ENV ROVER_LOCATION /app
# The location that files are mounted to.
ENV MOUNT_LOCATION /mnt/rover

# The following actions require root permissions:
USER root

# Copy the repository onto the image.
COPY --chown=${DEFAULT_UID}:${DEFAULT_GID} ./rover ${ROVER_LOCATION}/rover
COPY --chown=${DEFAULT_UID}:${DEFAULT_GID} ./environment.yml ${ROVER_LOCATION}

# Install the dependencies for this project, held in environment.yml.
WORKDIR ${ROVER_LOCATION}
RUN micromamba install -y -n base -f environment.yml \
 && micromamba clean --all --yes \
 && rm environment.yml

# Make the mount directory and set the default user to own it.
RUN mkdir ${MOUNT_LOCATION} \
 && chown -R ${DEFAULT_UID}:${DEFAULT_GID} /mnt \
 && chmod 777 ${MOUNT_LOCATION}

# Give control to the default mamba user.
USER ${DEFAULT_USER}