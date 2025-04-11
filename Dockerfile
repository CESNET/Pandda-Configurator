FROM oraclelinux:9

# Install required packages
RUN dnf install epel-release
RUN dnf install -y npm python3.9 python3.9-pip sshpass && \
    dnf clean all

# Create user and group
RUN groupadd -g 4200 pandda && \
    useradd -u 4201 -g 4200 pandda

# Setup ansible configuration
RUN mkdir -p /etc/ansible && \
    echo -e "[defaults]\nhost_key_checking = False" > /etc/ansible/ansible.cfg

# Copy application code
COPY app /web
COPY backend /backend
COPY pandda_playbooks /opt/pandda_playbooks
COPY ansible /opt/pandda_autodiscovery

# Set ownership for application files
RUN chown -R pandda:pandda /backend /web /opt/pandda_playbooks /opt/pandda_autodiscovery

# Install Node.js dependencies
WORKDIR /web
RUN npm install

# Setup Python virtual environment and install dependencies
WORKDIR /backend
RUN python3.9 -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt
RUN source venv/bin/activate && \
    ansible-galaxy collection install community.docker --force

RUN su - pandda -c 'source /backend/venv/bin/activate && ansible-galaxy collection install community.docker --force'

# Create startup scripts
RUN echo -e '#!/bin/bash\ncd /web\nnpm install\nnpm run dev' > /opt/start_pandda_webconf.sh && \
    echo -e '#!/bin/bash\ncd /backend\nsource venv/bin/activate\nflask --app pandda_webconf_server run --debug --host 0.0.0.0 --port 5001' > /opt/start_pandda_webconf_server.sh && \
    chmod +x /opt/start_pandda_webconf.sh /opt/start_pandda_webconf_server.sh

# Expose ports
EXPOSE 5000 5001

# Start services
CMD ["/bin/bash", "-c", "/opt/start_pandda_webconf.sh & /opt/start_pandda_webconf_server.sh & tail -f /dev/null"]
