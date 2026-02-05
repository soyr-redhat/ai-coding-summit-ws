# Point to the Internal Registry
FROM image-registry.openshift-image-registry.svc:5000/redhat-ods-applications/pytorch:2025.1

USER 0

# 1. Bake in backup
RUN mkdir -p /opt/app-root/workshop
COPY mnist_sequential.ipynb /opt/app-root/workshop/
RUN chown -R 1001:0 /opt/app-root/workshop && chmod -R g+w /opt/app-root/workshop

# 2. The Entrypoint Script
RUN echo '#!/bin/bash' > /opt/app-root/bin/entrypoint.sh && \
    echo 'cd /opt/app-root/src' >> /opt/app-root/bin/entrypoint.sh && \
    # --- START CLONE LOGIC ---
    echo 'rm -rf workshop-code .temp-repo' >> /opt/app-root/bin/entrypoint.sh && \
    echo 'git clone https://github.com/soyr-redhat/ai-coding-summit-ws .temp-repo' >> /opt/app-root/bin/entrypoint.sh && \
    echo 'cp -f .temp-repo/mnist_sequential.ipynb .' >> /opt/app-root/bin/entrypoint.sh && \
    echo 'rm -rf .temp-repo' >> /opt/app-root/bin/entrypoint.sh && \
    # --- END CLONE LOGIC ---
    echo 'exec "$@"' >> /opt/app-root/bin/entrypoint.sh

RUN chmod +x /opt/app-root/bin/entrypoint.sh && \
    chown 1001:0 /opt/app-root/bin/entrypoint.sh

# 3. Set the Entrypoint
ENTRYPOINT ["/opt/app-root/bin/entrypoint.sh"]

# 4. Restore the default launch command
CMD ["start-notebook.sh"]

USER 1001
WORKDIR /opt/app-root/src