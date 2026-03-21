import importlib

def get_ingestion(system_list, file_path):
    for system_name in system_list:
        module = importlib.import_module(f'data_ingestion.system_{system_name.lower()}')
        ingestion_class = getattr(module, f'System{system_name.upper()}Ingestion')
        worker = ingestion_class(system_name, file_path)

        worker.run()

def main():
    system_list = ['jira','perforce','swarm']
    get_ingestion(system_list, 파일경로)

if __name__ ==  "__main__":
    main()