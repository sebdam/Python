from datetime import datetime
from elasticsearch import Elasticsearch, NotFoundError

hosts = "https://lom.es.francecentral.azure.elastic-cloud.com"
api_key = "ejlkckZKc0JuMnFJUE92RE5YVnc6VjFCNHBOVmxRVkNGcjdUYTZ5d1Q5UQ=="
headers = {"Content-Type": "application/json", "Accept": "application/json"}

def create_new_index(client, index):
    resp = client.perform_request(
        "PUT",
        f"/{index}"
    )
    print(resp)

def force_merge_sub_indices(client, index, sub_indices_separator='-', sub_indices_part='*'):
    resp = client.perform_request(
        "POST",
        f"/{index}{sub_indices_separator}{sub_indices_part}/_forcemerge",
    )
    print(resp)

def reindex_sub_indices(client, index, sub_indices_separator = '-', sub_indices_part='*'):
    try:
        resp = client.reindex(
            source={"index": f"{index}{sub_indices_separator}{sub_indices_part}"},
            dest={
                "op_type": "create",
                "index": f"{index}"
            },
            conflicts="proceed",
            wait_for_completion = True
        )
        print(resp)
    except NotFoundError as e:
        print(f"Reindex error: {e.message} : {index}{sub_indices_separator}{sub_indices_part}")

def delete_sub_indices(client, index, sub_indices_separator='-', sub_indices_part='*'):
    resp = client.perform_request(
        "DELETE",
        f"/{index}{sub_indices_separator}{sub_indices_part}",
    )
    print(resp)

if __name__ == "__main__":
    current_month = 1 #datetime.now().month
    current_year = 2026 #datetime.now().year

    ernery_tracker_prod_indices = ["energy-tracker-prod-intraday","energy-tracker-prod-summary","energy-tracker-tick","lom"]

    client = Elasticsearch(hosts = hosts, api_key = api_key, headers = headers)

    for index in ernery_tracker_prod_indices:
        for_year = current_year if current_month>1 else current_year-1
        for_month = current_month-1 if current_month>1 else 12
        destindex = f"{index}-{for_year:04d}-{for_month:02d}" if index!="lom" else f"{index}-{for_year:04d}.{for_month:02d}"
        
        sub_indices_separator = '-' if index!="lom" else '.'

        print(f"==> Processing index: {destindex}")

        create_new_index(client, destindex)
        force_merge_sub_indices(client, destindex, sub_indices_separator)

        if(destindex.find("tick")>=0):
            for day in range(1,32):
                reindex_sub_indices(client, destindex, sub_indices_separator, f"{day:02d}")
        else:
            reindex_sub_indices(client, destindex, sub_indices_separator)
        
        delete_sub_indices(client, destindex, sub_indices_separator)