FROM yuvipanda/simple-singleuser:v1

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pip ca-certificates git nginx-extras lua-cjson

RUN pip3 --no-cache-dir install jupyter requests-futures jupyterhub-dummyauthenticator pytest webargs requests gitpython toolz

RUN pip3 install --upgrade pip

RUN pip install git+https://github.com/data-8/nbinteract.git
RUN jupyter serverextension enable --py nbinteract
RUN jupyter nbextension install --py nbinteract
RUN jupyter nbextension enable --py nbinteract

CMD jupyterhub-singleuser --port=8888 --ip=0.0.0.0 --user=\"$JPY_USER\" --cookie-name=$JPY_COOKIE_NAME --base-url=$JPY_BASE_URL --hub-prefix=$JPY_HUB_PREFIX   --hub-api-url=$JPY_HUB_API_URL"
