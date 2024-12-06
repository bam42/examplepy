import os

flyway_script_path=os.path.realpath(f"{os.path.dirname(os.path.realpath(__file__))}/../infra/db")

docker_cmd = f"""\
docker run --network="host" \
  -v {flyway_script_path}/migrations:/flyway/sql:ro \
  --rm flyway/flyway:11.0 \
  migrate -user=flyway -password=flyway_pwd -connectRetries=10 \
  -url='jdbc:postgresql://localhost:5432/example' -locations=filesystem:/flyway/sql
"""

os.system(docker_cmd)
