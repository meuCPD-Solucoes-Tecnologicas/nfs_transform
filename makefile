PATH_ZIP = log
FILENAME = $(shell date +%Y_%m_%d_%H_%M_%S)log.zip
TARGET_FOLDER= /home/$(USER)/Documentos
generate:
	python ./nfs_complementares.py NFS/Originais NFS/Complementares NFS/Base

generate_and_send:
	python  ./nfs_complementares.py --envio-producao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

generate_and_homo:
	python  ./nfs_complementares.py --envio-homologacao NFS/Originais NFS/Complementares NFS/Base 2921 42596 

limpeza:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*

limpeza-logs-and-zip:
	zip -r $(FILENAME) $(PATH_ZIP)
	mv  $(FILENAME) $(TARGET_FOLDER)
	rm -r ./log/*
	
	

limpeza-geral:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*
	rm -rf ./log/*
	
	